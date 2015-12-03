#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
import cStringIO
import csv
import datetime
import json
import locale
import re
import sys
import urllib2

try:
    import chardet
except ImportError:
    print ("WARNING: 3rd party module 'chardet' not found - character " +
           "encoding guessing will not work")

# These classes were adopted from
# https://docs.python.org/2/library/csv.html#examples
class UTF8Recoder:
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

class UnicodeReader:
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

class UnicodeWriter:
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

ARG_HELP_STRINGS = {
    "csv_file": "CSV file containing your APC data. It should consist of 3 " +
                "columns at least: Year, DOI and APC Amount (in EURO).",
    "encoding": "The encoding of the apc file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "locale": "Set the locale context used by the script. You might want to " +
              "set this if your system locale differs from the locale the " +
              "CSV file was created in (Example: Using en_US as your system " +
              "locale might become a problem if the file contains numeric " +
              "values with ',' as decimal point character)",
    "headers": "Ignore any CSV headers (if present) and try to determine " +
               "relevant columns heuristically.",
    "year": "Manually identify the 'Year' column if the script fails to " +
            "detect it automatically. The value is the numerical column " +
            "index in the CSV file, with the leftmost column being 0.",
    "doi": "Manually identify the 'DOI' column if the script fails to detect " +
           "it automatically. The value is the numerical column index in the " +
           "CSV file, with the leftmost column being 0.",
    "apc": "Manually identify the 'apc' column if the script fails to detect " +
           "it automatically. The value is the numerical column index in the " +
           "CSV file, with the leftmost column being 0."
}

# regex for detecing DOIs
doi_re = re.compile("^10\.[0-9]+(\.[0-9]+)*\/\S+")

def get_column_type_from_whitelist(item):
    column_names = {
        "doi": ["doi"],
        "apc": ["apc", "kosten"],
        "year": ["jahr", "period"]
    }
    for key, whitelist in column_names.iteritems():
        if item.lower() in whitelist:
            return key
    return None

def get_metadata_from_crossref(doi):
    if not doi_re.match(doi.strip()):
        return {"success": False,
                "error_msg": "Parse Error: '{}' is no valid DOI".format(doi)
               }
    url = 'http://data.crossref.org/' + doi
    headers = {"Accept": "application/vnd.citationstyles.csl+json"}
    req = urllib2.Request(url, None, headers)
    ret_value = {'success': True}
    try:
        response = urllib2.urlopen(req)
        json_content = response.read()
        ret_value['data'] = json.loads(json_content)
    except urllib2.HTTPError as httpe:
        ret_value['success'] = False
        code = str(httpe.getcode())
        ret_value['error_msg'] = "HTTPError: {} - {}".format(code, httpe.reason)
    except ValueError as ve:
        ret_value['success'] = False
        ret_value['error_msg'] = "ValueError: " + ve.message
    return ret_value

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-i", "--ignore-header", action="store_true",
                        help=ARG_HELP_STRINGS["headers"])
    parser.add_argument("-year", "--year_column", type=int,
                        help=ARG_HELP_STRINGS["year"])
    parser.add_argument("-doi", "--doi_column", type=int,
                        help=ARG_HELP_STRINGS["doi"])
    parser.add_argument("-apc", "--apc_column", type=int,
                        help=ARG_HELP_STRINGS["apc"])

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

    column_map = {
        "year": None,
        "apc": None,
        "doi": None
    }

    if args.year_column is not None:
        column_map['year'] = args.year_column
    if args.apc_column is not None:
        column_map['apc'] = args.apc_column
    if args.doi_column is not None:
        column_map['doi'] = args.doi_column
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
                if column_type is not None and column_map[column_type] is None:
                    column_map[column_type] = index
                    print ("Found column named '{}' at index {}, " +
                           "assuming this to be the {} column.").format(
                               item, index, column_type)
            break
        unassigned = filter(lambda (k, v): v is None, column_map.iteritems())
        if not unassigned:
            print "All relevant columns have been identifed."
        else:
            for item in unassigned:
                print "The {} column is still unidentified.".format(item[0])


    print "\n    *** Starting heuristical analysis ***\n"
    for row in reader:
        if not row: # Skip empty lines
            # We analyze the first non-empty line, a possible header should
            # have been processed by now.
            continue
        column_candidates = {
            "doi": [],
            "year": [],
            "apc": []
        }
        for (index, entry) in enumerate(row):
            if index in column_map.values():
                # Skip columns already assigned
                continue
            entry = entry.strip()
            # Search for a DOI
            if column_map['doi'] is None:
                if doi_re.match(entry):
                    column_id = str(index)
                    # identify column either numerical or by column header
                    if header:
                        column_id += " ('" + header[index] + "')"
                    print ("The entry in column {} looks like a " +
                           "DOI: {}").format(column_id, entry)
                    column_candidates['doi'].append(index)
                    continue
            # Search for a potential year string
            if column_map['year'] is None:
                try:
                    maybe_year = int(entry)
                    now = datetime.date.today().year
                    # Should be a wide enough margin
                    if maybe_year >= 2000 and maybe_year <= now + 2:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print ("The entry in column {} looks like a " +
                               "potential year: {}").format(column_id, entry)
                        column_candidates['year'].append(index)
                        continue
                except ValueError:
                    pass
            # Search for a potential apc string
            if column_map['apc'] is None:
                try:
                    maybe_apc = locale.atof(entry)
                    # Are there APCs above 6000€ ??
                    if maybe_apc >= 10 and maybe_apc <= 6000:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print ("The entry in column {} looks like a " +
                               "potential apc amount: {}").format(column_id,
                                                                  entry)
                        column_candidates['apc'].append(index)
                        continue
                except ValueError:
                    pass
        for column_type, candidates in column_candidates.iteritems():
            if column_map[column_type] is not None:
                continue
            if len(candidates) > 1:
                print ("Could not reliably identify the '" + column_type +
                       "' column - more than one possible candiate!")
            elif len(candidates) < 1:
                print "No candidate found for column '" + column_type + "'!"
            else:
                index = candidates.pop()
                column_id = header[index] if header else str(index)
                print ("Assuming column '{}' to be the '{}' " +
                       "column.").format(column_id, column_type)
                column_map[column_type] = index
        break

    # Wrap up: Check if there any column types left which have not been
    # identified - we cannot continue in that case.

    unassigned = filter(lambda (k, v): v is None, column_map.iteritems())
    if unassigned:
        print ("Error: We cannot continue because not all necessary " +
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

    for (column_type, index) in column_map.iteritems():
        column = str(index)
        if header:
            column += " ('" + header[index] + "')"
        print ("The '{}' column is column number {}.").format(column_type,
                                                              column)

    print "\n    *** Starting metadata aggregation ***\n"

    enriched_content = []

    csv_file.seek(0)
    header_processed = False
    for row in reader:
        if not row:
            continue # skip empty lines
        if not header_processed:
            header_processed = True
            new_header = ["period", "doi", "apc", "type", "publisher",
                          "journal", "ISSN_1", "ISSN_2"]
            enriched_content.append(new_header)
            if has_header:
                # If the CSV file has a header, we are currently there - skip it
                # to get to the first data row
                continue
        doi = row[column_map["doi"]]
        apc = row[column_map["apc"]]
        year = row[column_map["year"]]
        extended_row = [year, doi, apc]

        crossref_result = get_metadata_from_crossref(doi)
        if crossref_result["success"]:
            data = crossref_result["data"]
            print "DOI resolved: " + doi
            crossref_fields = [data["type"], data["publisher"],
                               data["container-title"]]
            crossref_fields.append(data['ISSN'][0])
            if len(data['ISSN']) > 1:
                crossref_fields.append(data['ISSN'][1])
            else:
                crossref_fields.append("")
            extended_row += crossref_fields
        else:
            print ("Error while trying to resolve DOI " + doi + ": " +
                   crossref_result["error_msg"])
        enriched_content.append(extended_row)

    csv_file.close()

    with open('out.csv', 'w') as out:
        if not dialect.escapechar:
            dialect.escapechar = "\\"
            print ("WARNING: Escaping needed while writing output file, but " +
                   "dialect does not specify an escape char - using '" +
                   dialect.escapechar + "'")
        writer = UnicodeWriter(out, dialect=dialect)
        writer.writerows(enriched_content)
