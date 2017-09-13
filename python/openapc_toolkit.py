#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import codecs
from collections import OrderedDict
import json
import locale
import logging
from logging.handlers import MemoryHandler
import re
import ssl
import sys
import urllib2
import xml.etree.ElementTree as ET

try:
    import chardet
except ImportError:
    chardet = None
    print ("WARNING: 3rd party module 'chardet' not found - character " +
           "encoding guessing will not work")

# regex for detecing DOIs
DOI_RE = re.compile("^(((https?://)?(dx.)?doi.org/)|(doi:))?(?P<doi>10\.[0-9]+(\.[0-9]+)*\/\S+)", re.IGNORECASE)
# regex for detecting shortDOIs
SHORTDOI_RE = re.compile("^(https?://)?(dx.)?doi.org/(?P<shortdoi>[a-z0-9]+)$", re.IGNORECASE)

ISSN_RE = re.compile("^(?P<first_part>\d{4})-?(?P<second_part>\d{3})(?P<check_digit>[\dxX])$")

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

class UnicodeDictReader(object):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.DictReader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return {unicode(k, "utf-8"): unicode(v, "utf-8") for (k, v) in row.iteritems()}

    def __iter__(self):
        return self

class OpenAPCUnicodeWriter(object):
    """
    A customized CSV Writer.

    A custom CSV writer. Encodes output in Unicode and can be configured to
    follow the open APC CSV quotation standards. A quote mask can also be
    provided to enable or disable value quotation in distinct CSV columns.

    Attributes:
        quotemask: A quotemask is a list of boolean values which should have
                   the same length as the number of columns in the csv file.
                   On writing, the truth values in the codemask will determine
                   if the values in the according column will be quoted. If no
                   quotemask is provided, every field will be quoted.
        openapc_quote_rules: Determines if the special openapc quote rules
                             should be applied, meaning that the keywords
                             NA, TRUE and FALSE will never be quoted. This
                             always takes precedence over a quotemask.
        has_header: Determines if the csv file has a header. If that's the case,
                    The values in the first row will all be quoted regardless
                    of any quotemask.
    """

    def __init__(self, f, quotemask=None, openapc_quote_rules=True, has_header=True):
        self.outfile = f
        self.quotemask = quotemask
        self.openapc_quote_rules = openapc_quote_rules
        self.has_header = has_header
        self.encoder = codecs.getincrementalencoder("utf-8")()

    def _prepare_row(self, row, use_quotemask):
        for index in range(len(row)):
            if self.openapc_quote_rules and row[index] in [u"TRUE", u"FALSE", u"NA"]:
                # Never quote these keywords
                continue
            if not use_quotemask or not self.quotemask:
                # Always quote without a quotemask
                row[index] = u'"' + row[index] + u'"'
                continue
            if index < len(self.quotemask):
                if self.quotemask[index]:
                    row[index] = u'"' + row[index] + u'"'
        return row

    def _write_row(self, row):
        line = u",".join(row) + u"\n"
        line = self.encoder.encode(line)
        self.outfile.write(line)

    def write_rows(self, rows):
        if self.has_header:
            self._write_row(self._prepare_row(rows.pop(0), False))
        for row in rows:
            self._write_row(self._prepare_row(row, True))

class DOAJOfflineAnalysis(object):

    def __init__(self, doaj_csv_file):
        self.doaj_issn_map = {}
        self.doaj_eissn_map = {}

        handle = open(doaj_csv_file, "r")
        reader = UnicodeDictReader(handle)
        for line in reader:
            journal_title = line["Journal title"]
            issn = line["Journal ISSN (print version)"]
            eissn = line["Journal EISSN (online version)"]
            if issn:
                self.doaj_issn_map[issn] = journal_title
            if eissn:
                self.doaj_eissn_map[eissn] = journal_title

    def lookup(self, any_issn):
        if any_issn in self.doaj_issn_map:
            return self.doaj_issn_map[any_issn]
        elif any_issn in self.doaj_eissn_map:
            return self.doaj_eissn_map[any_issn]
        else:
            return None


class CSVAnalysisResult(object):

    def __init__(self, blanks, dialect, has_header, enc, enc_conf):
        self.blanks = blanks
        self.dialect = dialect
        self.has_header = has_header
        self.enc = enc
        self.enc_conf = enc_conf

    def __str__(self):
        ret = "*****CSV file analysis*****\n"
        if self.dialect is not None:
            quote_consts = ["QUOTE_ALL", "QUOTE_MINIMAL", "QUOTE_NONE",
                            "QUOTE_NONNUMERIC"]
            quoting = self.dialect.quoting
            for const in quote_consts:
            # Seems hacky. Is there a more pythonic way to determine a
            # member const by its value?
                if hasattr(csv, const) and getattr(csv, const) == self.dialect.quoting:
                    quoting = const
            ret += ("CSV dialect sniffing:\ndelimiter => {dlm}\ndoublequote " +
                    "=> {dbq}\nescapechar => {esc}\nquotechar => {quc}\nquoting " +
                    "=> {quo}\nskip initial space => {sis}\n\n").format(
                        dlm=self.dialect.delimiter,
                        dbq=self.dialect.doublequote,
                        esc=self.dialect.escapechar,
                        quc=self.dialect.quotechar,
                        quo=quoting,
                        sis=self.dialect.skipinitialspace)

        if self.has_header:
            ret += "CSV file seems to have a header.\n\n"
        else:
            ret += "CSV file doesn't seem to have a header.\n\n"


        if self.blanks:
            ret += "Found " + str(self.blanks) + " empty lines in CSV file.\n\n"
        if self.enc:
            ret += ("Educated guessing of file character encoding: {} with " +
                    "a confidence of {}%\n").format(
                        self.enc,
                        int(self.enc_conf * 100))
        ret += "***************************"
        return ret

class ANSIColorFormatter(logging.Formatter):
    """
    A simple logging formatter using ANSI codes to colorize messages
    """
    FORMATS = {
        logging.ERROR: "\033[91m%(levelname)s: %(message)s\033[0m",
        logging.WARNING: "\033[93m%(levelname)s: %(message)s\033[0m",
        logging.INFO: "\033[94m%(levelname)s: %(message)s\033[0m",
        "DEFAULT": "%(levelname)s: %(message)s"
    }

    def format(self, record):
        self._fmt = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
        return logging.Formatter.format(self, record)

class BufferedErrorHandler(MemoryHandler):
    """
    A modified MemoryHandler without automatic flushing.

    This handler serves the simple purpose of buffering error and critical
    log messages so that they can be shown to the user in collected form when
    the enrichment process has finished.
    """
    def __init__(self, target):
        MemoryHandler.__init__(self, 100000, target=target)
        self.setLevel(logging.ERROR)

    def shouldFlush(self, record):
        return False
        
class NoRedirection(urllib2.HTTPErrorProcessor):
    """
    A dummy processor to suppress HTTP redirection.
    
    This handler serves the simple purpose of stopping redirection for
    easy extraction of shortDOI redirect targets.
    """
    def http_response(self, request, response):
        return response

    https_response = http_response

def get_normalised_DOI(doi_string):
    doi_string = doi_string.strip()
    doi_match = DOI_RE.match(doi_string)
    if doi_match:
        doi = doi_match.groupdict()["doi"]
        return doi.lower()
    shortdoi_match = SHORTDOI_RE.match(doi_string)
    if shortdoi_match:
        # Extract redirect URL to obtain original DOI
        shortdoi = shortdoi_match.groupdict()["shortdoi"]
        url = "https://doi.org/" + shortdoi
        opener = urllib2.build_opener(NoRedirection)
        try:
            res = opener.open(url)
            if res.code == 301:
                doi_match = DOI_RE.match(res.headers["Location"])
                if doi_match:
                    doi = doi_match.groupdict()["doi"]
                    return doi.lower()
            return None
        except (urllib2.HTTPError, urllib2.URLError):
            return None
    return None

def is_wellformed_ISSN(issn_string):
    issn_match = ISSN_RE.match(issn_string)
    if issn_match is not None:
        return True
    return False

def is_valid_ISSN(issn_string):
    issn_match = ISSN_RE.match(issn_string)
    match_dict = issn_match.groupdict()
    check_digit = match_dict["check_digit"]
    if check_digit in ["X", "x"]:
        check_digit = 10
    else:
        check_digit = int(check_digit)
    digits = match_dict["first_part"] + match_dict["second_part"]
    factor = 8
    total = 0
    for digit in digits:
        total += int(digit) * factor
        factor -= 1
    mod = total % 11
    if mod == 0 and check_digit == 0:
        return True
    else:
        if 11 - mod == check_digit:
            return True
    return False


def analyze_csv_file(file_path, line_limit=None):
    try:
        csv_file = open(file_path, "r")
    except IOError as ioe:
        error_msg = "Error: could not open file '{}': {}".format(file_path,
                                                                 ioe.strerror)
        return {"success": False, "error_msg": error_msg}

    content = ""

    blanks = 0
    lines_processed = 0
    for line in csv_file:
        if line.strip(): # omit blank lines
            content += line
            lines_processed += 1
            if line_limit and lines_processed > line_limit:
                break
        else:
            blanks += 1

    if chardet:
        chardet_result = chardet.detect(content)
        enc = chardet_result["encoding"]
        enc_conf = chardet_result["confidence"]
    else:
        enc = None
        enc_conf = None

    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(content)
        has_header = sniffer.has_header(content)
    except csv.Error as csve:
        error_msg = ("Error: An error occured while analyzing the file: '" +
                     csve.message + "'. Maybe it is no valid CSV file?")
        return {"success": False, "error_msg": error_msg}
    result = CSVAnalysisResult(blanks, dialect, has_header, enc, enc_conf)
    csv_file.close()
    return {"success": True, "data": result}

def get_csv_file_content(file_name, enc=None, force_header=False):
    result = analyze_csv_file(file_name, 500)
    if result["success"]:
        csv_analysis = result["data"]
        print csv_analysis
    else:
        print result["error_msg"]
        sys.exit()

    if enc is None:
        enc = csv_analysis.enc

    if enc is None:
        print ("Error: No encoding given for CSV file and automated " +
               "detection failed. Please set the encoding manually via the " +
               "--enc argument")
        sys.exit()

    dialect = csv_analysis.dialect

    csv_file = open(file_name, "r")

    content = []
    reader = UnicodeReader(csv_file, dialect=dialect, encoding=enc)
    header = []
    if csv_analysis.has_header or force_header:
        header.append(reader.next())
    for row in reader:
        content.append(row)
    csv_file.close()
    return (header, content)

def has_value(field):
    return len(field) > 0 and field != "NA"

def oai_harvest(basic_url, metadata_prefix=None, oai_set=None, processing=None, selective_harvest=False):
    """
    Harvest OpenAPC records via OAI-PMH
    """
    if selective_harvest:
        # create lists of all exisiting dois, pmids and urls
        keys = ["doi", "pmid", "url"]
        lists = {}
        for key in keys:
            lists[key] = []
        with open("../data/apc_de.csv", "r") as core_file:
            reader = UnicodeDictReader(core_file, encoding="utf-8")
            for line in reader:
                for key in keys:
                    if has_value(line[key]):
                        lists[key].append(line[key])
    collection_xpath = ".//oai_2_0:record//oai_2_0:metadata//intact:collection"
    token_xpath = ".//oai_2_0:resumptionToken"
    processing_regex = re.compile("'(?P<target>\w*?)':'(?P<generator>.*?)'")
    variable_regex = re.compile("%(\w*?)%")
    collection_content = OrderedDict([
        ("intact:institution", "institution"),
        ("intact:period", "period"),
        ("intact:euro", "euro"),
        ("intact:id_number[@type='doi']", "doi"),
        ("intact:is_hybrid", "is_hybrid"),
        ("intact:publisher", "publisher"),
        ("intact:journal_full_title", "journal_full_title"),
        ("intact:issn", "issn"),
        ("intact:licence", "license_ref"),
        ("intact:id_number[@type='pubmed']","pmid"),
        ("", "url"),
        ("intact:id_number[@type='local']", "local_id")
    ])
    #institution_xpath =
    namespaces = {
        "oai_2_0": "http://www.openarchives.org/OAI/2.0/",
        "intact": "http://intact-project.org"
    }
    url = basic_url + "?verb=ListRecords"
    if metadata_prefix:
        url += "&metadataPrefix=" + metadata_prefix
    if oai_set:
        url += "&set=" + oai_set
    if processing:
        match = processing_regex.match(processing)
        if match:
            groupdict = match.groupdict()
            target = groupdict["target"]
            generator = groupdict["generator"]
            variables = variable_regex.search(generator).groups()
        else:
            print_r("Error: Unable to parse processing instruction!")
            processing = None
    articles = [collection_content.values()] # use as header
    while url is not None:
        try:
            request = urllib2.Request(url)
            url = None
            response = urllib2.urlopen(request)
            content_string = response.read()
            root = ET.fromstring(content_string)
            collections = root.findall(collection_xpath, namespaces)
            counter = 0
            for collection in collections:
                article = OrderedDict()
                for xpath, elem in collection_content.iteritems():
                    result = collection.find(xpath, namespaces)
                    if result is not None and result.text is not None:
                        article[elem] = result.text
                    else:
                        article[elem] = "NA"
                if processing:
                    target_string = generator
                    for variable in variables:
                        target_string = target_string.replace("%" + variable + "%", article[variable])
                    article[target] = target_string
                if article["euro"] in ["NA", "0"]:
                    print_r("Article skipped, no APC amount found.")
                    continue
                elif selective_harvest:
                    key_found = False
                    for key in keys:
                        if article[key] in lists[key]:
                            print_r("Article skipped, " + key + " already in core data file.")
                            key_found = True
                            break
                    if key_found:
                        continue
                articles.append(article.values())
                counter += 1
            token = root.find(token_xpath, namespaces)
            if token is not None:
                url = basic_url + "?verb=ListRecords&resumptionToken=" + token.text
            print_g(str(counter) + " articles harvested.")
        except urllib2.HTTPError as httpe:
            code = str(httpe.getcode())
            print "HTTPError: {} - {}".format(code, httpe.reason)
        except urllib2.HTTPError as httpe:
            code = str(httpe.getcode())
            print "HTTPError: {} - {}".format(code, httpe.reason)
    with open("out.csv", "w") as f:
        writer = OpenAPCUnicodeWriter(f, openapc_quote_rules=True, has_header=True)
        writer.write_rows(articles)

def get_metadata_from_crossref(doi_string):
    """
    Take a DOI and extract metadata relevant to OpenAPC from crossref.

    This method looks up a DOI in crossref and returns all metadata fields
    relevant to OpenAPC (publisher, journal_full_title, issn, issn_print,
    issn_electronic, license_ref) and the crossref prefix.

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
    xpaths = {
        ".//cr_qr:crm-item[@name='publisher-name']": "publisher",
        ".//cr_qr:crm-item[@name='prefix-name']": "prefix",
        ".//cr_1_0:journal_metadata//cr_1_0:full_title": "journal_full_title",
        ".//cr_1_1:journal_metadata//cr_1_1:full_title": "journal_full_title",
        ".//cr_1_0:journal_metadata//cr_1_0:issn": "issn",
        ".//cr_1_1:journal_metadata//cr_1_1:issn": "issn",
        ".//cr_1_0:journal_metadata//cr_1_0:issn[@media_type='print']": "issn_print",
        ".//cr_1_1:journal_metadata//cr_1_1:issn[@media_type='print']": "issn_print",
        ".//cr_1_0:journal_metadata//cr_1_0:issn[@media_type='electronic']": "issn_electronic",
        ".//cr_1_1:journal_metadata//cr_1_1:issn[@media_type='electronic']": "issn_electronic",
        ".//ai:license_ref": "license_ref"}
    namespaces = {
        "cr_qr": "http://www.crossref.org/qrschema/3.0",
        "cr_1_1": "http://www.crossref.org/xschema/1.1",
        "cr_1_0": "http://www.crossref.org/xschema/1.0",
        "ai": "http://www.crossref.org/AccessIndicators.xsd"}
    doi = get_normalised_DOI(doi_string)
    if doi is None:
        error_msg = u"Parse Error: '{}' is no valid DOI".format(doi_string)
        return {"success": False, "error_msg": error_msg}
    url = 'http://data.crossref.org/' + doi
    headers = {"Accept": "application/vnd.crossref.unixsd+xml"}
    req = urllib2.Request(url, None, headers)
    ret_value = {'success': True}
    try:
        response = urllib2.urlopen(req)
        content_string = response.read()
        root = ET.fromstring(content_string)
        doi_element = root.findall(".//cr_qr:doi", namespaces)
        doi_type = doi_element[0].attrib['type']
        if doi_type != "journal_article":
            msg = ("Unsupported DOI type '" + doi_type + "' (OpenAPC only " +
                   "supports journal articles)")
            raise ValueError(msg)
        crossref_data = {}
        for path, elem in xpaths.iteritems():
            if elem not in crossref_data:
                crossref_data[elem] = None
            result = root.findall(path, namespaces)
            if result:
                crossref_data[elem] = result[0].text
        ret_value['data'] = crossref_data
    except urllib2.HTTPError as httpe:
        ret_value['success'] = False
        code = str(httpe.getcode())
        ret_value['error_msg'] = "HTTPError: {} - {}".format(code, httpe.reason)
    except urllib2.URLError as urle:
        ret_value['success'] = False
        ret_value['error_msg'] = "URLError: {}".format(urle.reason)
    except ET.ParseError as etpe:
        ret_value['success'] = False
        ret_value['error_msg'] = "ElementTree ParseError: {}".format(str(etpe))
    except ValueError as ve:
        ret_value['success'] = False
        ret_value['error_msg'] = str(ve)
    return ret_value

def get_metadata_from_pubmed(doi_string):
    doi = get_normalised_DOI(doi_string)
    if doi is None:
        return {"success": False,
                "error_msg": u"Parse Error: '{}' is no valid DOI".format(doi_string)
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
    except urllib2.URLError as urle:
        ret_value['success'] = False
        ret_value['error_msg'] = "URLError: {}".format(urle.reason)
    return ret_value

def lookup_journal_in_doaj(issn, bypass_cert_verification=False):
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
        if bypass_cert_verification:
            empty_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            response = urllib2.urlopen(req, context=empty_context)
        else:
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

def process_row(row, row_num, column_map, num_required_columns,
                no_crossref_lookup=False, no_pubmed_lookup=False,
                no_doaj_lookup=False, doaj_offline_analysis=False,
                bypass_cert_verification=False):
    """
    Enrich a single row of data and reformat it according to Open APC standards.

    Take a csv row (a list) and a column mapping (a list of CSVColumn objects)
    and return an enriched and re-arranged version which conforms to the Open
    APC data schema.

    Args:
        row: A list of column values (as yielded by a UnicodeReader f.e.).
        row_num: The line number in the csv file, for logging purposes.
        column_map: An OrderedDict of CSVColumn Objects, mapping the row
                    cells to Open APC data schema fields.
        num_required_columns: An int describing the required length of the row
                              list. If not matched, an error is logged and the
                              row is returned unchanged.
        no_crossref_lookup: If true, no metadata will be imported from crossref.
        no_pubmed_lookup: If true, no_metadata will be imported from pubmed.
        no_doaj_lookup: If true, journals will not be checked for being
                        listended in the DOAJ (default).
        doaj_offline_analysis: If true, a local copy will be used for the DOAJ
                               lookup. Has no effect if no_doaj_lookup is set to
                               true.
        bypass_cert_verification: If true, certificate validation will be
                                  skipped when connecting to metadata
                                  providers via TLS.

     Returns:
        A list of values which represents the enriched and re-arranged variant
        of the input row. If no errors were logged during the process, this
        result will conform to the Open APC data schema.
    """
    MESSAGES = {
        "num_columns": u"Syntax: The number of values in this row (%s) " +
                       "differs from the number of columns (%s). Line left " +
                       "unchanged, the resulting CSV file will not be valid.",
        "locale": u"Error: Could not process the monetary value '%s' in " +
                  "column %s. This will usually have one of two reasons:\n1) " +
                  "The value does not represent a number.\n2) The value " +
                  "represents a number, but its format differs from your " +
                  "current system locale - the most common source of error " +
                  "will be the decimal mark (1234.56 vs 1234,56). Try using " +
                  "another locale with the -l option.",
        "unify": u"Normalisation: CrossRef-based {} changed from '{}' to '{}' " +
                 "to maintain consistency.",
        "doi_norm": u"Normalisation: DOI '{}' normalised to pure form ({}).",
        "springer_distinction": u"publisher 'Springer Nature' found " +
                                 "for a pre-2015 article - publisher " +
                                 "changed to '%s' based on prefix " +
                                 "discrimination ('%s')",
        "unknown_prefix": u"publisher 'Springer Nature' found for a " +
                           "pre-2015 article, but discrimination was " +
                           "not possible - unknown prefix ('%s')",
        "issn_hyphen_fix": u"Normalisation: Added hyphen to %s value (%s -> %s)"
    }

    if len(row) != num_required_columns:
        msg = "Line %s: " + MESSAGES["num_columns"]
        logging.error(msg, row_num, len(row), num_required_columns)
        return row

    doi = row[column_map["doi"].index]

    current_row = OrderedDict()
    # Copy content of identified columns
    for csv_column in column_map.values():
        if csv_column.column_type == "euro" and csv_column.index is not None:
            # special case for monetary values: Cast to float to ensure
            # the decimal point is a dot (instead of a comma)
            euro_value = row[csv_column.index]
            if len(euro_value) == 0:
                msg = "Line %s: Empty monetary value in column %s."
                logging.warning(msg, row_num, csv_column.index)
                current_row[csv_column.column_type] = "NA"
            else:
                try:
                    euro = locale.atof(euro_value)
                    if euro.is_integer():
                        euro = int(euro)
                    current_row[csv_column.column_type] = str(euro)
                except ValueError:
                    msg = "Line %s: " + MESSAGES["locale"]
                    logging.error(msg, row_num, euro_value, csv_column.index)
        else:
            if csv_column.index is not None and len(row[csv_column.index]) > 0:
                current_row[csv_column.column_type] = row[csv_column.index]
            else:
                current_row[csv_column.column_type] = "NA"

    if len(doi) == 0 or doi == 'NA':
        msg = ("Line %s: No DOI found, entry could not enriched with " +
               "Crossref or Pubmed metadata.")
        logging.warning(msg, row_num)
        current_row["indexed_in_crossref"] = "FALSE"
    else:
        # Normalise DOI
        norm_doi = get_normalised_DOI(doi)
        if norm_doi is not None and norm_doi != doi:
            current_row["doi"] = norm_doi
            msg = MESSAGES["doi_norm"].format(doi, norm_doi)
            logging.warning(msg)
            doi = norm_doi
        # include crossref metadata
        if not no_crossref_lookup:
            crossref_result = get_metadata_from_crossref(doi)
            while not crossref_result["success"] and crossref_result["error_msg"].startswith("HTTPError: 504"):
                # retry on gateway timeouts, crossref API is quite busy sometimes
                msg = "%s, retrying..."
                logging.warning(msg, crossref_result["error_msg"])
                crossref_result = get_metadata_from_crossref(doi)
            if crossref_result["success"]:
                logging.info("Crossref: DOI resolved: " + doi)
                current_row["indexed_in_crossref"] = "TRUE"
                data = crossref_result["data"]
                prefix = data.pop("prefix")
                for key, value in data.iteritems():
                    if value is not None:
                        if key == "journal_full_title":
                            unified_value = get_unified_journal_title(value)
                            if unified_value != value:
                                msg = MESSAGES["unify"].format("journal title",
                                                               value,
                                                               unified_value)
                                logging.warning(msg)
                            new_value = unified_value
                        elif key == "publisher":
                            unified_value = get_unified_publisher_name(value)
                            if unified_value != value:
                                msg = MESSAGES["unify"].format("publisher name",
                                                               value,
                                                               unified_value)
                                logging.warning(msg)
                            new_value = unified_value
                            # Treat Springer Nature special case: crossref erroneously
                            # reports publisher "Springer Nature" even for articles
                            # published before 2015 (publishers fusioned only then)
                            if int(current_row["period"]) < 2015 and new_value == "Springer Nature":
                                publisher = None
                                if prefix in ["Springer (Biomed Central Ltd.)", "Springer-Verlag", "Springer - Psychonomic Society"]:
                                    publisher = "Springer Science + Business Media"
                                elif prefix in ["Nature Publishing Group", "Nature Publishing Group - Macmillan Publishers"]:
                                    publisher = "Nature Publishing Group"
                                if publisher:
                                    msg = "Line %s: " + MESSAGES["springer_distinction"]
                                    logging.warning(msg, row_num, publisher, prefix)
                                    new_value = publisher
                                else:
                                    msg = "Line %s: " + MESSAGES["unknown_prefix"]
                                    logging.error(msg, row_num, prefix)
                        # Fix ISSNs without hyphen
                        elif key in ["issn", "issn_print", "issn_electronic"]:
                            new_value = value
                            if re.match("^\d{7}[\dxX]$", value):
                                new_value = value[:4] + "-" + value[4:]
                                msg = "Line %s: " + MESSAGES["issn_hyphen_fix"]
                                logging.warning(msg, row_num, key, value, new_value)
                        else:
                            new_value = value
                    else:
                        new_value = "NA"
                        msg = (u"WARNING: Element '%s' not found in in response for " +
                               "doi %s.")
                        logging.debug(msg, key, doi)
                    old_value = current_row[key]
                    current_row[key] = column_map[key].check_overwrite(old_value, new_value)
            else:
                msg = "Line %s: Crossref: Error while trying to resolve DOI %s: %s"
                logging.error(msg, row_num, doi, crossref_result["error_msg"])
                current_row["indexed_in_crossref"] = "FALSE"
        # include pubmed metadata
        if not no_pubmed_lookup:
            pubmed_result = get_metadata_from_pubmed(doi)
            if pubmed_result["success"]:
                logging.info("Pubmed: DOI resolved: " + doi)
                data = pubmed_result["data"]
                for key, value in data.iteritems():
                    if value is not None:
                        new_value = value
                    else:
                        new_value = "NA"
                        msg = (u"WARNING: Element %s not found in in response for " +
                               "doi %s.")
                        logging.debug(msg, key, doi)
                    old_value = current_row[key]
                    current_row[key] = column_map[key].check_overwrite(old_value, new_value)
            else:
                msg = "Line %s: Pubmed: Error while trying to resolve DOI %s: %s"
                logging.error(msg, row_num, doi, pubmed_result["error_msg"])

    # lookup in DOAJ. try the EISSN first, then ISSN and finally print ISSN
    if not no_doaj_lookup:
        issns = []
        new_value = "NA"
        if current_row["issn_electronic"] != "NA":
            issns.append(current_row["issn_electronic"])
        if current_row["issn"] != "NA":
            issns.append(current_row["issn"])
        if current_row["issn_print"] != "NA":
            issns.append(current_row["issn_print"])
        for issn in issns:
            # In some cases xref delievers ISSNs without a hyphen. Add it
            # temporarily to prevent the DOAJ lookup from failing.
            if re.match("^\d{7}[\dxX]$", issn):
                issn = issn[:4] + "-" + issn[4:]
            # look up in an offline copy of the DOAJ if requested...
            if doaj_offline_analysis:
                lookup_result = doaj_offline_analysis.lookup(issn)
                if lookup_result:
                    msg = (u"DOAJ: Journal ISSN (%s) found in DOAJ " +
                           "offline copy ('%s').")
                    logging.info(msg, issn, lookup_result)
                    new_value = "TRUE"
                    break
                else:
                    msg = (u"DOAJ: Journal ISSN (%s) not found in DOAJ " +
                           "offline copy.")
                    new_value = "FALSE"
                    logging.info(msg, issn)
            # ...or query the online API
            else:
                doaj_res = lookup_journal_in_doaj(issn, bypass_cert_verification)
                if doaj_res["data_received"]:
                    if doaj_res["data"]["in_doaj"]:
                        msg = u"DOAJ: Journal ISSN (%s) found in DOAJ ('%s')."
                        logging.info(msg, issn, doaj_res["data"]["title"])
                        new_value = "TRUE"
                        break
                    else:
                        msg = u"DOAJ: Journal ISSN (%s) not found in DOAJ."
                        logging.info(msg, issn)
                        new_value = "FALSE"
                else:
                    msg = (u"Line %s: DOAJ: Error while trying to look up " +
                           "ISSN %s: %s")
                    logging.error(msg, row_num, issn, doaj_res["error_msg"])
        old_value = current_row["doaj"]
        current_row["doaj"] = column_map["doaj"].check_overwrite(old_value,
                                                                 new_value)
    return current_row.values()


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
        "euro": ["apc", "kosten", "cost", "euro", "eur"],
        "period": ["period", "jahr"],
        "is_hybrid": ["is_hybrid", "is hybrid", "hybrid"],
        "publisher": ["publisher"],
        "journal_full_title": ["journal_full_title", "journal", "journal title", "journal full title", "journaltitle"],
        "issn": ["issn", "issn.1", "issn0"],
        "issn_print": ["issn_print"],
        "issn_electronic": ["issn_electronic"],
        "issn_l": ["issn_l"],
        "license_ref": ["licence", "license", "license_ref"],
        "indexed_in_crossref": ["indexed_in_crossref"],
        "pmid": ["pmid", "pubmed id"],
        "pmcid": ["pmcid", "pubmed central (pmc) id"],
        "ut": ["ut"],
        "url": ["url"],
        "doaj": ["doaj"]
    }
    for key, whitelist in column_names.iteritems():
        if column_name.lower() in whitelist:
            return key
    return None

def get_unified_publisher_name(publisher):
    """
    Unify certain publisher names via a mapping table.

    CrossRef data is sometimes inconsistent when it comes to publisher names,
    these cases can be solved by returning a unified name from a mapping table.

    Args:
        publisher: A publisher as it is returned from the CrossRef API.
    Returns:
        Either a unified name or the original name as a string
    """
    publisher_mappings = {
        "The Optical Society": "Optical Society of America (OSA)",
        "Impact Journals": "Impact Journals LLC",
        "American Society for Biochemistry &amp; Molecular Biology (ASBMB)": "American Society for Biochemistry & Molecular Biology (ASBMB)",
        "Institute of Electrical and Electronics Engineers (IEEE)": "Institute of Electrical & Electronics Engineers (IEEE)",
        "Cold Spring Harbor Laboratory": "Cold Spring Harbor Laboratory Press",
        "Institute of Electrical &amp; Electronics Engineers (IEEE)": "Institute of Electrical & Electronics Engineers (IEEE)",
        "Hindawi Limited": "Hindawi Publishing Corporation",
        "Oxford University Press": "Oxford University Press (OUP)",
        "Wiley": "Wiley-Blackwell"
    }
    return publisher_mappings.get(publisher, publisher)

def get_unified_journal_title(journal_full_title):
    """
    Unify certain journal titles via a mapping table.

    CrossRef data is sometimes inconsistent when it comes to journal titles,
    these cases can be solved by returning a unified name from a mapping table.

    Args:
        journal_full_title: A journal title as it is returned from the CrossRef API.
    Returns:
        Either a unified name or the original name as a string
    """
    journal_mappings = {
        "PLoS ONE": "PLOS ONE",
        "Phys. Chem. Chem. Phys.": "Physical Chemistry Chemical Physics",
        "J. Mater. Chem. A": "Journal of Materials Chemistry A",
        "J. Mater. Chem. B": "Journal of Materials Chemistry B",
        "PLoS Pathogens": "PLOS Pathogens",
        "PLoS Genetics": "PLOS Genetics",
        "PLoS Biology": "PLOS Biology",
        "PLoS Computational Biology": "PLOS Computational Biology",
        "PLoS Neglected Tropical Diseases": "PLOS Neglected Tropical Diseases",
        "Oncotarget": "OncoTarget",
        "Journal of Lipid Research": "The Journal of Lipid Research",
        "Plastic and Reconstructive Surgery Global Open": "Plastic and Reconstructive Surgery - Global Open",
        "RSC Adv.": "RSC Advances",
        "Zeitschrift für die neutestamentliche Wissenschaft": "Zeitschrift für die Neutestamentliche Wissenschaft und die Kunde der älteren Kirche",
        "Chem. Soc. Rev.": "Chemical Society Reviews",
        "Journal of Elections, Public Opinion and Parties": "Journal of Elections, Public Opinion & Parties",
        "Scientific Repor.": "Scientific Reports",
        "PAIN": "Pain",
        "Journal of the National Cancer Institute": "JNCI Journal of the National Cancer Institute",
        "G3&amp;#58; Genes|Genomes|Genetics": "G3: Genes|Genomes|Genetics",
        "Transactions of the Royal Society of Tropical Medicine and Hygiene": "Transactions of The Royal Society of Tropical Medicine and Hygiene",
        "Org. Biomol. Chem.": "Organic & Biomolecular Chemistry",
        "PLoS Medicine": "PLOS Medicine",
        "Org. Biomol. Chem.": "Organic & Biomolecular Chemistry",
        "AJP: Heart and Circulatory Physiology": "American Journal of Physiology - Heart and Circulatory Physiology",
        "Naturwissenschaften": "The Science of Nature",
        "Dalton Trans.": "Dalton Transactions",
        "Chem. Sci.": "Chemical Science",
        "J. Anal. At. Spectrom.": "Journal of Analytical Atomic Spectrometry",
        "Geospatial health": "Geospatial Health",
        "Journal of the European Optical Society-Rapid Publications": "Journal of the European Optical Society: Rapid Publications",
        "J. Mater. Chem. C": "Journal of Materials Chemistry C",
        "Chem. Commun.": "Chemical Communications",
        "Cognition and Emotion": "Cognition & Emotion",
        "Catal. Sci. Technol.": "Catalysis Science & Technology",
        "Journal of Epidemiology & Community Health": "Journal of Epidemiology and Community Health",
        "JRSM": "Journal of the Royal Society of Medicine",
        "Green Chem.": "Green Chemistry",
        "Stochastics and  Partial Differential Equations: Analysis and Computations": "Stochastics and Partial Differential Equations: Analysis and Computations",
        "Journal of Mass Communication & Journalism": "Journal of Mass Communication and Journalism",
        "Journal of Child and Adolescent Behavior": "Journal of Child and Adolescent Behaviour",
        "Journal of Otolaryngology - Head and Neck Surgery": "Journal of Otolaryngology - Head & Neck Surgery",
        "manuscripta mathematica": "Manuscripta Mathematica",
        "CPT Pharmacometrics Syst. Pharmacol.": "CPT: Pharmacometrics & Systems Pharmacology",
        "Taal en tongval": "Taal en Tongval",
        "Notfall +  Rettungsmedizin": "Notfall + Rettungsmedizin",
        "The Journal of Neuroscience": "Journal of Neuroscience",
        "British Editorial Society of Bone &amp; Joint Surgery": "British Editorial Society of Bone & Joint Surgery",
        "Proceedings of the Royal Society A: Mathematical, Physical and Engineering Science": "Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences",
        "The FEBS Journal": "FEBS Journal",
        "PLANT PHYSIOLOGY": "Plant Physiology",
        "IEEE Transactions on Ultrasonics, Ferroelectrics, and Frequency Control": "IEEE Transactions on Ultrasonics, Ferroelectrics and Frequency Control",
        "Cellular and Molecular Gastroenterology and Hepatology": "CMGH Cellular and Molecular Gastroenterology and Hepatology",
        "Tellus B: Chemical and Physical Meteorology": "Tellus B",
        "Natural Hazards and Earth System Science": "Natural Hazards and Earth System Sciences",
        "interactive Journal of Medical Research": "Interactive Journal of Medical Research",
        "EP Europace": "Europace",
        "Prostate Cancer and Prostatic Disease": "Prostate Cancer and Prostatic Diseases",
        "CARTILAGE": "Cartilage",
        "Annals of Clinical Biochemistry": "Annals of Clinical Biochemistry: An international journal of biochemistry and laboratory medicine",
        "JNCI: Journal of the National Cancer Institute": "JNCI Journal of the National Cancer Institute",
        "Journal of the National Cancer Institute": "JNCI Journal of the National Cancer Institute",
        "European Heart Journal – Cardiovascular Imaging": "European Heart Journal - Cardiovascular Imaging",
        "Transplantation": "Transplantation Journal",
        "SHOCK": "Shock",
        "Endocrine-Related Cancer": "Endocrine Related Cancer",
        "The American Journal of Tropical Medicine and Hygiene": "American Journal of Tropical Medicine and Hygiene",
        "American Journal of Physiology - Endocrinology And Metabolism": "AJP: Endocrinology and Metabolism",
        "Neurology - Neuroimmunology Neuroinflammation": "Neurology: Neuroimmunology & Neuroinflammation",
        "eneuro": "eNeuro",
        "The Journal of Experimental Biology": "Journal of Experimental Biology",
        "The Plant Cell Online": "The Plant Cell",
        "Journal of Agricultural, Biological, and Environmental Statistics": "Journal of Agricultural, Biological and Environmental Statistics",
        "PalZ": "Paläontologische Zeitschrift",
        "Lighting Research and Technology": "Lighting Research & Technology",
        "The Journal of Infectious Diseases": "Journal of Infectious Diseases",
        "Planning Practice and Research": "Planning Practice & Research",
        "Learning and Individual Differences": "Learning & Individual Differences",
        "Water Science and Technology": "Water Science & Technology",
        "Antimicrobial Resistance & Infection Control": "Antimicrobial Resistance and Infection Control",
        "MedChemComm": "Med. Chem. Commun.",
        "European Journal of Public Health": "The European Journal of Public Health",
        "Journal of Vacuum Science & Technology B, Nanotechnology and Microelectronics: Materials, Processing, Measurement, and Phenomena": "Journal of Vacuum Science & Technology B: Microelectronics and Nanometer Structures",
        "Briefings In Bioinformatics": "Briefings in Bioinformatics",
        "Notes and Records: the Royal Society journal of the history of science": "Notes and Records of the Royal Society",
        "Journal Of Logic And Computation": "Journal of Logic and Computation",
        "Health:: An Interdisciplinary Journal for the Social Study of Health, Illness and Medicine": "Health: An Interdisciplinary Journal for the Social Study of Health, Illness and Medicine",
        "INTERNATIONAL JOURNAL OF SYSTEMATIC AND EVOLUTIONARY MICROBIOLOGY": "International Journal of Systematic and Evolutionary Microbiology",
        "Protein Engineering Design and Selection": "Protein Engineering, Design and Selection",
        u"European Heart Journal – Cardiovascular Imaging": "European Heart Journal - Cardiovascular Imaging",
        "The Journals of Gerontology: Series A": "The Journals of Gerontology Series A: Biological Sciences and Medical Sciences",
        "MHR: Basic science of reproductive medicine": "Molecular Human Reproduction",
        "Research on Language and Social Interaction": "Research on Language & Social Interaction",
        "Psychology and Sexuality": "Psychology & Sexuality",
        "BJA: British Journal of Anaesthesia": "British Journal of Anaesthesia",
        "Journal of Development Studies": "The Journal of Development Studies",
        "Tellus A: Dynamic Meteorology and Oceanography": "Tellus A",
        "International journal of methods in psychiatric research": "International Journal of Methods in Psychiatric Research"
    }
    return journal_mappings.get(journal_full_title, journal_full_title)

def get_corrected_issn_l(issn_l):
    issn_l_corrections = {
        "0266-7061": "1367-4803", # "Bioinformatics". 1460-2059(issn_e) -> 0266-7061, but 1367-4803(issn_p) -> 1367-4803
        "1654-6628": "1654-661X"  # "Food & Nutrition Research". 1654-6628(issn_p) -> 1654-6628, but 1654-661X(issn_e) -> 1654-661X
    }
    return issn_l_corrections.get(issn_l, issn_l)

def print_b(text):
    print "\033[94m" + text + "\033[0m"

def print_g(text):
    print "\033[92m" + text + "\033[0m"

def print_r(text):
    print "\033[91m" + text + "\033[0m"

def print_y(text):
    print "\033[93m" + text + "\033[0m"
