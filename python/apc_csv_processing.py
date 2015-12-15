#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
from collections import OrderedDict
from copy import copy
import cStringIO
import csv
import datetime
import json
import locale
import re
import sys
import urllib2
import xml.etree.ElementTree as ET

try:
    import chardet
except ImportError:
    print ("WARNING: 3rd party module 'chardet' not found - character " +
           "encoding guessing will not work")

# These classes were adopted from
# https://docs.python.org/2/library/csv.html#examples
class UTF8Recoder(object):
    """
    Iterator that reads an encoded stream and reencodes the input
    to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter(object):
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

class CSVColumn(object):

    def __init__(self, column_type, mandatory, index=None, column_name=""):
        self.column_type = column_type
        self.mandatory = mandatory
        self.index = index
        self.column_name = column_name


ARG_HELP_STRINGS = {
    "csv_file": "CSV file containing your APC data. It must contain at least " +
                "the 4 mandatory columns defined by the OpenAPC data schema: " +
                "institution, doi, period and euro (in no particular order).",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "locale": "Set the locale context used by the script. You might want to " +
              "set this if your system locale differs from the locale the " +
              "CSV file was created in (Example: Using en_US as your system " +
              "locale might become a problem if the file contains numeric " +
              "values with ',' as decimal point character)",
    "headers": "Ignore any CSV headers (if present) and try to determine " +
               "relevant columns heuristically.",
    "institution": "Manually identify the 'institution' column if the script " +
                   "fails to detect it automatically. The value is the " +
                   "numerical column index in the CSV file, with the " +
                   "leftmost column being 0.",
    "period": "Manually identify the 'period' column if the script fails to " +
              "detect it automatically. The value is the numerical column " +
              "index in the CSV file, with the leftmost column being 0.",
    "doi": "Manually identify the 'doi' column if the script fails to " +
           "detect it automatically. The value is the numerical column index " +
           "in the CSV file, with the leftmost column being 0.",
    "euro": "Manually identify the 'euro' column if the script fails to " +
            "detect it automatically. The value is the numerical column " +
            "index in the CSV file, with the leftmost column being 0.",
    "publisher": "Manually identify the 'publisher' column if the script " +
                 "fails to detect it automatically. The value is the " +
                 "numerical column index in the CSV file, with the leftmost " +
                 "column being 0. This is an optional column, identifying it " +
                 "is required if there are articles without a DOI in the file.",
    "journal_full_title": "Manually identify the 'journal_full_title' column " +
                          "if the script fails to detect it automatically. " +
                          "The value is the numerical column index in the " +
                          "CSV file, with the leftmost column being 0. This " +
                          "is an optional column, identifying it is required " +
                          "if there are articles without a DOI in the file."
}

# regex for detecing DOIs
DOI_RE = re.compile("^((https?://dx.doi.org/)|(doi:))?(?P<doi>10\.[0-9]+(\.[0-9]+)*\/\S+)")

def get_column_type_from_whitelist(column_name):
    """
    Identify a CSV column type by looking up the name in a whitelist.
    
    Args:
        column_name: Name of a CSV column, usually extracted from the header.
    Returns:
        An APC-normed column type (as a string) if the column name was found in
        a whitelist, None otherwise.
    """
    column_names = {
        "institution": ["institution"],
        "doi": ["doi"],
        "euro": ["apc", "kosten", "euro"],
        "period": ["period", "jahr"],
        "publisher": ["publisher"],
        "journal_full_title": ["journal_full_title", "journal"]
    }
    for key, whitelist in column_names.iteritems():
        if column_name.lower() in whitelist:
            return key
    return None

def get_metadata_from_crossref(doi_string):
    """
    Take a DOI and extract metadata relevant to OpenAPC from crossref.

    This method looks up a DOI in crossref and returns all metadata fields
    relevant to OpenAPC (publisher, journal_full_title, issn, issn_print,
    ssn_electronic, license_ref).

    Args:
        doi_string: A string representing a doi. 'Pure' form (10.xxx),
        DOI Handbook notation (doi:10.xxx) or crossref-style
        (http://dx.doi.org/10.xxx) are all acceptable.
    Returns:
        A dict with a key 'success'. If data extraction was successful,
        'success' will be True and the dict will have a second entry 'data'
        which contains the extracted metadata as another dict:

        {'publisher': 'MDPI AG',
         'journal_full_title': 'Chemosensors',
         [...]
        }
        The dict will contain all keys in question, those where no data could
        be retreived will have a None value.

        If data extraction failed, 'success' will be False and the dict will
        contain a second entry 'error_msg' with a string value
        stating the reason.
    """
    doi_match = DOI_RE.match(doi_string.strip())
    if not doi_match:
        error_msg = u"Parse Error: '{}' is no valid DOI".format(doi_string)
        return {"success": False, "error_msg": error_msg}
    doi = doi_match.groupdict()["doi"]
    url = 'http://data.crossref.org/' + doi
    headers = {"Accept": "application/vnd.crossref.unixsd+xml"}
    req = urllib2.Request(url, None, headers)
    ret_value = {'success': True}
    try:
        response = urllib2.urlopen(req)
        content_string = response.read()
        ns = {"cr_qr": "http://www.crossref.org/qrschema/3.0",
              "cr_x": "http://www.crossref.org/xschema/1.1",
              "ai": "http://www.crossref.org/AccessIndicators.xsd"}
        root = ET.fromstring(content_string)
        crossref_data = {}
        xpaths = {
            "publisher": ".//cr_qr:crm-item[@name='publisher-name']",
            "journal_full_title": ".//cr_x:journal_metadata//cr_x:full_title",
            "issn": ".//cr_x:journal_metadata//cr_x:issn",
            "issn_print": ".//cr_x:journal_metadata//" +
                          "cr_x:issn[@media_type='print']",
            "issn_electronic": ".//cr_x:journal_metadata//" +
                               "cr_x:issn[@media_type='electronic']",
            "license_ref": ".//ai:license_ref"
        }
        for elem, path in xpaths.iteritems():
            result = root.findall(path, ns)
            if result:
                crossref_data[elem] = result[0].text
            else:
                crossref_data[elem] = None
        ret_value['data'] = crossref_data
    except urllib2.HTTPError as httpe:
        ret_value['success'] = False
        code = str(httpe.getcode())
        ret_value['error_msg'] = "HTTPError: {} - {}".format(code, httpe.reason)
    return ret_value

def get_metadata_from_pubmed(doi):
    if not DOI_RE.match(doi.strip()):
        return {"success": False,
                "error_msg": u"Parse Error: '{}' is no valid DOI".format(doi)
               }
    url = "http://www.ebi.ac.uk/europepmc/webservices/rest/search?query=doi:"
    url += doi
    req = urllib2.Request(url)
    ret_value = {'success': True}
    try:
        response = urllib2.urlopen(req)
        content_string = response.read()
        root = ET.fromstring(content_string)
        pubmed_data = {}
        xpaths = {
            "pmid": ".//resultList/result/pmid",
            "pmcid": ".//resultList/result/pmcid",
        }
        for elem, path in xpaths.iteritems():
            result = root.findall(path)
            if result:
                pubmed_data[elem] = result[0].text
            else:
                pubmed_data[elem] = None
        ret_value['data'] = pubmed_data
    except urllib2.HTTPError as httpe:
        ret_value['success'] = False
        code = str(httpe.getcode())
        ret_value['error_msg'] = "HTTPError: {} - {}".format(code, httpe.reason)
    return ret_value
    
def lookup_journal_in_doaj(issn):
    """
    Take an ISSN and check if the corresponding journal exists in DOAJ.
    
    This method looks up an ISSN in the Directory of Open Access Journals
    (DOAJ, https://doaj.org). This is a simple existence check and will not
    return any additional metadata (except for the journal title).
    It is also important to note that there is no additional effort to test
    the validity of the given ISSN - if a negative result is returned, the ISSN
    might be invalid, but it might also belong to a journal which is not
    registered in DOAJ.
    
    Args:
        issn: A string representing an issn
     Returns:
        A dict with a key 'data_received'. If data was received from DOAJ,
        this key will have the value True and the dict will have a second
        entry 'data' which contains the lookup result:
        
        {'in_doaj': True,
         'title': 'Frontiers in Human Neuroscience',
        }
        or
        {'in_doaj': False}

        If data extraction failed, 'data_received' will be False and the dict
        will contain a second entry 'error_msg' with a string value
        stating the reason.   
    """
    headers = {"Accept": "application/json"}
    ret_value = {'data_received': True}
    url = "https://doaj.org/api/v1/search/journals/issn:" + issn
    req = urllib2.Request(url, None, headers)
    try:
        response = urllib2.urlopen(req)
        content_string = response.read()
        json_dict = json.loads(content_string)
        ret_data = {}
        if "results" in json_dict and len(json_dict["results"]) > 0:
            ret_data["in_doaj"] = True
            # Try to extract the journal title - useful for error correction
            journal = json_dict["results"][0]
            try:
                ret_data["title"] = journal["bibjson"]["title"]
            except KeyError:
                ret_data["title"] = ""
        else:
            ret_data["in_doaj"] = False
        ret_value['data'] = ret_data
    except urllib2.HTTPError as httpe:
        ret_value['data_received'] = False
        code = str(httpe.getcode())
        ret_value['error_msg'] = "HTTPError: {} - {}".format(code, httpe.reason)
    except ValueError as ve:
        ret_value['data_received'] = False
        msg = "ValueError while parsing JSON: {}"
        ret_value['error_msg'] = msg.format(ve.message)
    return ret_value
        

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-i", "--ignore-header", action="store_true",
                        help=ARG_HELP_STRINGS["headers"])
    parser.add_argument("-institution", "--institution_column", type=int,
                        help=ARG_HELP_STRINGS["institution"])
    parser.add_argument("-period", "--period_column", type=int,
                        help=ARG_HELP_STRINGS["period"])
    parser.add_argument("-doi", "--doi_column", type=int,
                        help=ARG_HELP_STRINGS["doi"])
    parser.add_argument("-euro", "--euro_column", type=int,
                        help=ARG_HELP_STRINGS["euro"])
    parser.add_argument("-publisher", "--publisher_column", type=int,
                        help=ARG_HELP_STRINGS["publisher"])
    parser.add_argument("-journal_full_title", "--journal_full_title_column",
                        type=int, help=ARG_HELP_STRINGS["journal_full_title"])

    args = parser.parse_args()
    enc = None # CSV file encoding

    if args.locale:
        norm = locale.normalize(args.locale)
        if norm != args.locale:
            print "locale '{}' not found, normalized to '{}'".format(
                args.locale, norm)
        try:
            loc = locale.setlocale(locale.LC_ALL, norm)
            print "Using locale", loc
        except locale.Error as loce:
            print "Setting locale to " + norm + " failed: " + loce.message
            sys.exit()

    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            print ("Encoding '{}' found in Python's codec collection " +
                   "as '{}'").format(args.encoding, codec.name)
            enc = args.encoding
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()

    try:
        csv_file = open(args.csv_file, "r")
    except IOError as ioe:
        print "Error: could not open file", args.csv_file, ":", ioe.strerror
        sys.exit()

    print "    *** Analyzing file '" + args.csv_file + "' ***\n"
    content = ""

    blanks = 0
    for line in csv_file:
        if line.strip(): # omit blank lines
            content += line
        else:
            blanks += 1
    if blanks:
        print "Found " + str(blanks) + " empty lines in CSV file."

    if chardet and enc is None:
        chardet_result = chardet.detect(content)
        enc = chardet_result["encoding"]
        print ("Educated guessing of file character encoding: {enc} with " +
               "a confidence of {conf}%").format(
                   enc=enc,
                   conf=int(chardet_result["confidence"] * 100))

    if enc is None:
        print ("Error: No encoding given for CSV file and automated " +
               "detection failed. Please set the encoding manually via the " +
               "--enc argument")
        sys.exit()

    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(content)
        has_header = sniffer.has_header(content)
    except csv.Error as csve:
        print ("Error: An error occured while analyzing the file: " +
               csve.message + ". Maybe it is no valid CSV file?")
        sys.exit()

    if dialect is not None:
        quote_consts = ["QUOTE_ALL", "QUOTE_MINIMAL", "QUOTE_NONE",
                        "QUOTE_NONNUMERIC"]
        quoting = dialect.quoting
        for const in quote_consts:
            # Seems hacky. Is there a more pythonic way to determine a
            # member const by its value?
            if hasattr(csv, const) and getattr(csv, const) == dialect.quoting:
                quoting = const
        print ("CSV dialect sniffing:\ndelimiter => {dlm}\ndoublequote " +
               "=> {dbq}\nescapechar => {esc}\nquotechar => {quc}\nquoting " +
               "=> {quo}\nskip initial space => {sis}").format(
                   dlm=dialect.delimiter,
                   dbq=dialect.doublequote,
                   esc=dialect.escapechar,
                   quc=dialect.quotechar,
                   quo=quoting,
                   sis=dialect.skipinitialspace)

    if has_header:
        print "\nCSV file seems to have a header."
    else:
        print "\nCSV file doesn't seem to have a header."

    csv_file.seek(0)
    reader = UnicodeReader(csv_file, dialect=dialect, encoding=enc)
    
    first_row = reader.next()
    num_columns = len(first_row)
    print "\nCSV file has {} columns.".format(num_columns)
    
    csv_file.seek(0)
    reader = UnicodeReader(csv_file, dialect=dialect, encoding=enc)

    column_map = {
        "institution": CSVColumn("institution", True, args.institution_column),
        "period": CSVColumn("period", True, args.period_column),
        "euro": CSVColumn("euro", True, args.euro_column),
        "doi": CSVColumn("doi", True, args.doi_column),
        "publisher": CSVColumn("publisher", False, args.publisher_column),
        "journal_full_title": CSVColumn("journal_full_title", False,
                                        args.journal_full_title_column)
    }
    
    # This list will store info about additional (unknown) columns found in 
    # the CSV file as CSVColumn objects. 
    additional_columns = []
    
    csv_columns = OrderedDict([
        ("institution", "NA"),
        ("period", "NA"),
        ("euro", "NA"),
        ("doi", "NA"),
        ("is_hybrid", "NA"),
        ("publisher", "NA"),
        ("journal_full_title", "NA"),
        ("issn", "NA"),
        ("issn_print", "NA"),
        ("issn_electronic", "NA"),
        ("license_ref", "NA"),
        ("indexed_in_crossref", "NA"),
        ("pmid", "NA"),
        ("pmcid", "NA"),
        ("ut", "NA"),
        ("url", "NA"),
        ("doaj", "NA")
    ])

    
    header = None
    if has_header:
        for row in reader:
            if not row: # Skip empty lines
                continue
            header = row # First non-empty row should be the header
            if args.ignore_header:
                print "Skipping header analysis due to command line argument."
                break
            else:
                print "\n    *** Analyzing CSV header ***\n"
            for (index, item) in enumerate(header):
                column_type = get_column_type_from_whitelist(item)
                if column_type is not None and column_map[column_type].index is None:
                    column_map[column_type].index = index
                    column_map[column_type].column_name = item
                    print ("Found column named '{}' at index {}, " +
                           "assuming this to be the {} column.").format(
                               item, index, column_type)
            break


    print "\n    *** Starting heuristical analysis ***\n"
    for row in reader:
        if not row: # Skip empty lines
            # We analyze the first non-empty line, a possible header should
            # have been processed by now.
            continue
        column_candidates = {
            "doi": [],
            "period": [],
            "euro": []
        }
        for (index, entry) in enumerate(row):
            if index in [csvcolumn.index for csvcolumn in column_map.values()]:
                # Skip columns already assigned
                continue
            entry = entry.strip()
            # Search for a DOI
            if column_map['doi'].index is None:
                if DOI_RE.match(entry):
                    column_id = str(index)
                    # identify column either numerical or by column header
                    if header:
                        column_id += " ('" + header[index] + "')"
                    print ("The entry in column {} looks like a " +
                           "DOI: {}").format(column_id, entry)
                    column_candidates['doi'].append(index)
                    continue
            # Search for a potential year string
            if column_map['period'].index is None:
                try:
                    maybe_period = int(entry)
                    now = datetime.date.today().year
                    # Should be a wide enough margin
                    if maybe_period >= 2000 and maybe_period <= now + 2:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print ("The entry in column {} looks like a " +
                               "potential period: {}").format(column_id, entry)
                        column_candidates['period'].append(index)
                        continue
                except ValueError:
                    pass
            # Search for a potential monetary amount
            if column_map['euro'].index is None:
                try:
                    maybe_euro = locale.atof(entry)
                    # Are there APCs above 6000€ ??
                    if maybe_euro >= 10 and maybe_euro <= 6000:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print ("The entry in column {} looks like a " +
                               "potential euro amount: {}").format(column_id,
                                                                   entry)
                        column_candidates['euro'].append(index)
                        continue
                except ValueError:
                    pass
        for column_type, candidates in column_candidates.iteritems():
            if column_map[column_type].index is not None:
                continue
            if len(candidates) > 1:
                print ("Could not reliably identify the '" + column_type +
                       "' column - more than one possible candiate!")
            elif len(candidates) < 1:
                print "No candidate found for column '" + column_type + "'!"
            else:
                index = candidates.pop()
                column_map[column_type].index = index
                if header:
                    column_id = header[index]
                    column_map[column_type].column_name = column_id
                else:
                    column_id = index
                print ("Assuming column '{}' to be the '{}' " +
                       "column.").format(column_id, column_type)
                column_map[column_type].index = index
        break

    # Wrap up: Check if there any mandatory column types left which have not
    # yet been identified - we cannot continue in that case.
    unassigned = filter(lambda (k, v): v.mandatory and v.index is None,
                        column_map.iteritems())
    if unassigned:
        print ("ERROR: We cannot continue because not all mandatory " +
               "column types in the CSV file could be automatically " +
               "identified. There are 2 ways to fix this:")
        if not header:
            print ("1) Add a header row to your file and identify the " +
                   "column(s) by assigning them an appropiate column name.")
        else:
            print ("1) Identify the missing column(s) by assigning them " +
                   "a different column name in the CSV header (You can use " +
                   "the column name(s) mentioned in the message below)")
        print ("2) Use command line parameters when calling this script " +
               "to identify the missing columns (use -h for help) ")
        for item in unassigned:
            print "The {} column is still unidentified.".format(item[0])
        if header:
            print "The CSV header is:\n" + dialect.delimiter.join(header)
        sys.exit()

    print "\n    *** CSV file analysis summary ***\n"

    index_dict = {csvc.index: csvc for csvc in column_map.values()}
    
    for index in range(num_columns):
        column_name = ""
        if header:
            column_name = header[index]
        if index in index_dict:
            column = index_dict[index]
            mandatory = "mandatory" if column.mandatory else "optional"
            msg = "column number {} ({}) is the {} column '{}'"
            print msg.format(index, column_name, mandatory, column.column_type)
        else:
            msg = ("column number {} ({}) is an unknown column, it will be " +
                   "appended to the generated CSV file")
            print msg.format(index, column_name)
            if not column_name:
                # Use a generic name
                column_name = "unknown"
            while column_name in csv_columns:
                # TODO: Replace by a numerical, increasing suffix
                column_name += "_"
            csv_columns[column_name] = "NA"
            additional_columns.append(CSVColumn(column_name, False, index))
            

    print ""
    for column in column_map.values():
        if column.index is None:
            # Should all be optional...
            mandatory = "mandatory" if column.mandatory else "optional"
            msg = "The {} column '{}' could not be identified."
            print msg.format(mandatory, column.column_type)


    # Check for unassigned optional column types. We can continue but should
    # issue a warning as all entries will need a valid DOI in this case.
    unassigned = filter(lambda (k, v): not v.mandatory and v.index is None,
                        column_map.iteritems())
    if unassigned:
        print ("\nWARNING: Not all optional column types could be " +
               "identified. Metadata aggregation is still possible, but " +
               "every entry in the CSV file will need a valid DOI.")

    start = raw_input("\nStart metadata aggregation? (y/n):")
    while start not in ["y", "n"]:
        start = raw_input("Please type 'y' or 'n':")
    if start == "n":
        sys.exit()
        
    

    print "\n    *** Starting metadata aggregation ***\n"

    enriched_content = []

    csv_file.seek(0)
    reader = UnicodeReader(csv_file, dialect=dialect, encoding=enc)
    header_processed = False
    
    for row in reader:
        if not row:
            continue # skip empty lines
        if not header_processed:
            header_processed = True
            enriched_content.append(csv_columns.keys())
            if has_header:
                # If the CSV file has a header, we are currently there - skip it
                # to get to the first data row
                continue

        doi = row[column_map["doi"].index]

        current_row = copy(csv_columns)
        
        # Copy content of identified columns 
        for csv_column in column_map.values():
            if csv_column.index is not None:
                current_row[csv_column.column_type] = row[csv_column.index]
        
        # add unidentified fields to the row
        for column in additional_columns:
            field = row[column.index]
            current_row[column.column_type] = field
            
        # include crossref metadata
        crossref_result = get_metadata_from_crossref(doi)
        if crossref_result["success"]:
            print "Crossref: DOI resolved: " + doi
            current_row["indexed_in_crossref"] = "TRUE"
            data = crossref_result["data"]
            for key, value in data.iteritems():
                if value is not None:
                    current_row[key] = value
                else:
                    current_row[key] = "NA"
                    print (u"WARNING: Element '{}' not found in in response " +
                           "for doi {}.").format(key, doi)
        else:
            print ("Crossref: Error while trying to resolve DOI " + doi + ": " +
                   crossref_result["error_msg"])
            current_row["indexed_in_crossref"] = "FALSE"

        # include pubmed metadata
        pubmed_result = get_metadata_from_pubmed(doi)
        if pubmed_result["success"]:
            print "Pubmed: DOI resolved: " + doi
            data = pubmed_result["data"]
            for key, value in data.iteritems():
                if value is not None:
                    current_row[key] = value
                else:
                    current_row[key] = "NA"
                    print (u"WARNING: Element '{}' not found in in response " +
                           "for doi {}.").format(key, doi)
        else:
            print ("Pubmed: Error while trying to resolve DOI " + doi + ": " +
                   pubmed_result["error_msg"])
                   
        # lookup in DOAJ. try the EISSN first, then the ISSN
        if current_row["doaj"] != "TRUE":
            issns = []
            if current_row["issn_electronic"] != "NA":
                issns.append(current_row["issn_electronic"])
            if current_row["issn"] != "NA":
                issns.append(current_row["issn"])
            for issn in issns:
                doaj_res = lookup_journal_in_doaj(issn)
                if doaj_res["data_received"]:
                    if doaj_res["data"]["in_doaj"]:
                        msg = "DOAJ: Journal ISSN ({}) found in DOAJ ('{}')."
                        print msg.format(issn, doaj_res["data"]["title"])
                        current_row["doaj"] = "TRUE"
                        break
                    else:
                        msg = "DOAJ: Journal ISSN ({}) not found in DOAJ."
                        current_row["doaj"] = "FALSE"
                        print msg.format(issn)
                else:
                    msg = "DOAJ: Error while trying to look up ISSN {}: {}"
                    print msg.format(issn, doaj_res["error_msg"])
            

        enriched_content.append(current_row.values())

    csv_file.close()

    with open('out.csv', 'w') as out:
        if not dialect.escapechar:
            dialect.escapechar = "\\"
            print ("WARNING: Escaping needed while writing output file, but " +
                   "dialect does not specify an escape char - using '" +
                   dialect.escapechar + "'")
        writer = UnicodeWriter(out, dialect=dialect)
        writer.writerows(enriched_content)


if __name__ == '__main__':
    main()
