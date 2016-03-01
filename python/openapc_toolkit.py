#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import codecs
import json
import re
import urllib2
import xml.etree.ElementTree as ET

try:
    import chardet
except ImportError:
    print ("WARNING: 3rd party module 'chardet' not found - character " +
           "encoding guessing will not work")
           
# regex for detecing DOIs
DOI_RE = re.compile("^(((https?://)?dx.doi.org/)|(doi:))?(?P<doi>10\.[0-9]+(\.[0-9]+)*\/\S+)")

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
        return {k: unicode(v, "utf-8") for (k, v) in row.iteritems()}

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
        line = u",".join(row) + u"\r\n"
        line = self.encoder.encode(line)
        self.outfile.write(line)
        
    def write_rows(self, rows):
        if self.has_header:
            self._write_row(self._prepare_row(rows.pop(0), False))
        for row in rows:
            self._write_row(self._prepare_row(row, True))
            
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
        
def is_wellformed_DOI(doi_string):
    doi_match = DOI_RE.match(doi_string.strip())
    if doi_match is not None:
        return True
    return False
 
def analyze_csv_file(file_path, line_limit=None):
    try:
        csv_file = open(file_path, "r")
    except IOError as ioe:
        error_msg = "Error: could not open file '{}': {}".format(file_path,
                                                                 ioe.strerror)
        return {"success": False, "error_msg": error_msg}
        
    data = {}
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
    _cr_schema_1_0 = 'xmlns="http://www.crossref.org/xschema/1.0"'
    _cr_schema_1_1 = 'xmlns="http://www.crossref.org/xschema/1.1"'
    xpaths = {
        "publisher": ".//cr_qr:crm-item[@name='publisher-name']",
        "journal_full_title": ".//cr_x:journal_metadata//cr_x:full_title",
        "issn": ".//cr_x:journal_metadata//cr_x:issn",
        "issn_print": ".//cr_x:journal_metadata//" +
                      "cr_x:issn[@media_type='print']",
        "issn_electronic": ".//cr_x:journal_metadata//" +
                           "cr_x:issn[@media_type='electronic']",
        "license_ref": ".//ai:license_ref"}
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
        # Detect crossref namespace - older entries might still have version 1.0
        if _cr_schema_1_1 in content_string:
            ns = {"cr_qr": "http://www.crossref.org/qrschema/3.0",
                  "cr_x": "http://www.crossref.org/xschema/1.1",
                  "ai": "http://www.crossref.org/AccessIndicators.xsd"}
        elif _cr_schema_1_0 in content_string:
            ns = {"cr_qr": "http://www.crossref.org/qrschema/3.0",
                  "cr_x": "http://www.crossref.org/xschema/1.0",
                  "ai": "http://www.crossref.org/AccessIndicators.xsd"}
        else:
            ret_value['success'] = False
            error_msg = ("Parse Error: Unable to detect CrossRef XML " +
                        "Namespace - neither '{}' nor '{}' found in query " +
                        "result!").format(_cr_schema_1_0, _cr_schema_1_1)
            ret_value['error_msg'] = error_msg
            return ret_value
        root = ET.fromstring(content_string)
        crossref_data = {}
        
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
        "euro": ["apc", "kosten", "euro", "eur"],
        "period": ["period", "jahr"],
        "is_hybrid": ["is_hybrid"],
        "publisher": ["publisher"],
        "journal_full_title": ["journal_full_title", "journal"],
        "issn": ["issn"],
        "issn_print": ["issn_print"],
        "issn_electronic": ["issn_electronic"],
        "license_ref": ["license_ref"],
        "indexed_in_crossref": ["indexed_in_crossref"],
        "pmid": ["pmid"],
        "pmcid": ["pmcid"],
        "ut": ["ut"],
        "url": ["url"],
        "doaj": ["doaj"]
    }
    for key, whitelist in column_names.iteritems():
        if column_name.lower() in whitelist:
            return key
    return None
    
def print_b(text):
    print "\033[94m" + text + "\033[0m"
    
def print_g(text):
    print "\033[92m" + text + "\033[0m"
    
def print_r(text):
    print "\033[91m" + text + "\033[0m"

def print_y(text):
    print "\033[93m" + text + "\033[0m"
