import datetime
import pytest

from pytest import fail
from csv import DictReader
from os.path import dirname, join
from sys import path
from urllib.parse import urlparse

from sortedcontainers import SortedList

APC_DATA = []
ARTICLE_AC_DATA = []
BPC_DATA = []
CONTRACTS_DATA = []

DATA_FILES = {
    "apc": {
        "file_path": "data/apc_de.csv",
        "is_ac_file_for": None,
        "unused_fields": ["license_ref", "pmid", "pmcid", "ut"],
        "target_file": APC_DATA,
        "row_length": 18,
        "has_doi": True,
        "has_issn": True,
        "has_isbn": False,
        "has_url": True,
        "has_group_ids": False,
        "doi_list": SortedList(),
    },
    "article_ac": {
        "file_path": "data/additional_costs.csv",
        "is_ac_file_for": ["apc", "ta"],
        "unused_fields": [],
        "target_file": ARTICLE_AC_DATA,
        "row_length": 9,
        "has_doi": True,
        "has_issn": False,
        "has_isbn": False,
        "has_url": False,
        "has_group_ids": False,
        "doi_list": SortedList(),
    },
    "ta": {
        "file_path": "data/transformative_agreements/transformative_agreements.csv",
        "is_ac_file_for": None,
        "unused_fields": ["license_ref", "pmid", "pmcid", "ut"],
        "target_file": APC_DATA,
        "row_length": 21,
        "has_doi": True,
        "has_issn": True,
        "has_isbn": False,
        "has_url": True,
        "has_group_ids": False,
        "doi_list": SortedList(),
    },
    "bpc": {
        "file_path": "data/bpc.csv",
        "is_ac_file_for": None,
        "unused_fields": ["license_ref"],
        "target_file": BPC_DATA,
        "row_length": 13,
        "has_doi": True,
        "has_issn": False,
        "has_isbn": True,
        "has_url": False,
        "has_group_ids": False,
        "doi_list": SortedList(),
    },
    "contracts": {
        "file_path": "data/transformative_agreements/contracts.csv",
        "is_ac_file_for": None,
        "unused_fields": [],
        "target_file": CONTRACTS_DATA,
        "row_length": 9,
        "has_doi": False,
        "has_issn": False,
        "has_isbn": False,
        "has_url": False,
        "has_group_ids": True,
        "doi_list": None,
    }
}

KNOWN_DUPLICATES = {
    "apc": {
        "unresolved_duplicates": {
            "file_path": "data/unresolved_duplicates.csv",
            "doi_list": [],
        },
        "apc_cofunding": {
            "file_path": "data/apc_cofunding.csv",
            "doi_list": [],
        },
    },
    "bpc": {
        "unresolved_bpc_duplicates": {
            "file_path": "data/unresolved_bpc_duplicates.csv",
            "doi_list": [],
        },
    }
}

CURRENT_YEAR = datetime.datetime.now().year
ISBNHANDLING = None

if __name__ == '__main__':
    path.append(dirname(path[0]))
    import openapc_toolkit as oat
    import mappings
    import whitelists as wl
    ISBNHANDLING = oat.ISBNHandling(temp_file_dir="../tempfiles")
    for data_file, metadata in DATA_FILES.items():
        metadata["file_path"] = join("..", "..", metadata["file_path"])
    for _, file_dict in KNOWN_DUPLICATES.items():
        for _, metadata in file_dict.items():
            metadata["file_path"] = join("..", "..", metadata["file_path"])

    def fail(msg):
        oat.print_r(msg)

else:
    path.append(join(path[0], "python"))
    import openapc_toolkit as oat
    import mappings
    from . import whitelists as wl
    ISBNHANDLING = oat.ISBNHandling(temp_file_dir="python/tempfiles")

class RowObject(object):
    """
    A minimal container class to store contextual information along with csv rows.
    """
    def __init__(self, file_name, line_number, row, origin):
        self.file_name = file_name
        self.line_number = line_number
        self.row = row
        self.origin = origin

def _get_isbn_group_publisher(isbn):
    if ISBNHANDLING.ISBN_SPLIT_RE.match(isbn):
        parts = isbn.split("-")
        group_and_publisher = parts[1:3]
        key = ("-").join(group_and_publisher)
        return key
    return None
    
def _normalize_url(url_string):
    parsed_url = urlparse(url_string.lower())
    stripped_url = parsed_url.netloc + parsed_url.path
    if parsed_url.query:
        stripped_url += "?" + parsed_url.query
    return stripped_url

global_doi_list = SortedList()
global_isbn_list = SortedList()
global_url_list = SortedList()

issn_dict = {}
issn_p_dict = {}
issn_e_dict = {}
issn_l_dict = {}
group_id_dict = {}
identifier_dict = {} # ESAC Ids

title_dict = {}

isbn_dict = {}

group_id_publisher_dict = {}

ISSN_DICT_FIELDS = ["is_hybrid", "publisher", "journal_full_title", "issn_l"]

for data_file, metadata in DATA_FILES.items():
    with open(metadata["file_path"], "r") as csv_file:
        reader = DictReader(csv_file)
        line = 2
        for row in reader:
            for field in metadata["unused_fields"]:
                del(row[field])
            metadata["target_file"].append(RowObject(metadata["file_path"], line, row, data_file))
            if metadata["has_doi"] and oat.has_value(row["doi"]):
                if metadata["is_ac_file_for"] is None:
                    global_doi_list.add(row["doi"])
                metadata["doi_list"].add(row["doi"])
            if metadata["has_url"] and oat.has_value(row["url"]):
                global_url_list.add(_normalize_url(row["url"]))
            if metadata["has_issn"]:
                reduced_row = {}
                for field in ISSN_DICT_FIELDS:
                    reduced_row[field] = row[field]
                issn = row["issn"]
                if oat.has_value(issn):
                    if issn not in issn_dict:
                        issn_dict[issn] = [reduced_row]
                    elif reduced_row not in issn_dict[issn]:
                        issn_dict[issn].append(reduced_row)
                issn_p = row["issn_print"]
                if oat.has_value(issn_p):
                    if issn_p not in issn_p_dict:
                        issn_p_dict[issn_p] = [reduced_row]
                    elif reduced_row not in issn_p_dict[issn_p]:
                        issn_p_dict[issn_p].append(reduced_row)
                issn_e = row["issn_electronic"]
                if oat.has_value(issn_e):
                    if issn_e not in issn_e_dict:
                        issn_e_dict[issn_e] = [reduced_row]
                    elif reduced_row not in issn_e_dict[issn_e]:
                        issn_e_dict[issn_e].append(reduced_row)
                issn_l = row["issn_l"]
                if oat.has_value(issn_l):
                    if issn_l not in issn_l_dict:
                        issn_l_dict[issn_l] = [reduced_row]
                    elif reduced_row not in issn_l_dict[issn_l]:
                        issn_l_dict[issn_l].append(reduced_row)

            if metadata["has_isbn"]:
                isbn = row["isbn"]
                if oat.has_value(isbn):
                    key = _get_isbn_group_publisher(isbn)
                    if key is not None:
                        publisher = row["publisher"]
                        if key not in isbn_dict:
                            isbn_dict[key] = [publisher]
                        elif publisher not in isbn_dict[key]:
                            isbn_dict[key].append(publisher)
                isbn_list = []
                for isbn in [row["isbn"], row["isbn_print"], row["isbn_electronic"]]:
                    # clear row-internal duplicates
                    if oat.has_value(isbn) and isbn not in isbn_list and isbn not in wl.NON_DUPLICATE_ISBNS:
                        isbn_list.append(isbn)
                for entry in isbn_list:
                    global_isbn_list.add(entry)
            if metadata["has_group_ids"]:
                if oat.has_value(row["group_id"]):
                    group_id = row["group_id"]
                    if group_id not in group_id_dict:
                        group_id_dict[group_id] = [row]
                    else:
                        group_id_dict[group_id].append(row)
                if oat.has_value("identifier"):
                    identifier = row["identifier"]
                    if identifier not in identifier_dict:
                        identifier_dict[identifier] = [row]
                    else:
                        identifier_dict[identifier].append(row)
            line += 1

for _, file_dict in KNOWN_DUPLICATES.items():
    for _, metadata in file_dict.items():
        with open(metadata["file_path"], "r") as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                if row["doi"] not in metadata["doi_list"]:
                    metadata["doi_list"].append(row["doi"])

def check_line_length(row_object):
    __tracebackhide__ = True
    correct_length = DATA_FILES[row_object.origin]["row_length"]
    target_length = correct_length - len(DATA_FILES[row_object.origin]["unused_fields"])
    if len(row_object.row) != target_length:
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        fail(line_str + 'Row must consist of exactly ' + str(correct_length) + ' items')

def check_optional_identifier(row_object):
    __tracebackhide__ = True
    row = row_object.row
    if row['doi'] == "NA":
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        if not oat.has_value(row['url']):
            fail(line_str + 'if no DOI is given, the column "url" ' +
                        'must not be empty')

def check_common_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if not oat.has_value(row['institution']):
        fail(line_str + 'the column "institution" must not be empty')
    if not oat.has_value(row['period']):
        fail(line_str + 'the column "period" must not be empty')
    else:
        try:
            period_date = datetime.datetime.strptime(row['period'], "%Y")
            if period_date.year > CURRENT_YEAR + 10:
                msg = 'the date value in column "period" ("{}") is more than 10 years in the future'
                fail(line_str + msg.format(row["period"]))
            elif period_date.year < 1990:
                msg = 'the date value in column "period" ("{}") is earlier than 1990'
                fail(line_str + msg.format(row["period"]))
        except ValueError:
            msg = 'the value in column "period" ("{}") could not be parsed as a year value'
            fail(line_str + msg.format(row["period"]))
    if not oat.has_value(row['publisher']):
        fail(line_str + 'the column "publisher" must not be empty')
    if row['indexed_in_crossref'] not in ["TRUE", "FALSE"]:
        fail(line_str + 'value in row "indexed_in_crossref" must either be TRUE or FALSE')
    if not row['doi'] == "NA":
        doi_norm = oat.get_normalised_DOI(row['doi'])
        if doi_norm is None:
            fail(line_str + 'value in row "doi" must either be NA or represent a valid DOI')
        elif doi_norm != row['doi']:
            fail(line_str + 'value in row "doi" contains a valid DOI, but the format ' +
                                   'is not correct. It should be the simple DOI name, not ' +
                                   'handbook notation (doi:...) or a HTTP URI (http://dx.doi.org/...)')
    if len(row['publisher']) != len(row['publisher'].strip()):
        fail(line_str + 'publisher name (' + row['publisher'] + ') has leading or trailing whitespaces')  

def check_apc_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if not oat.has_value(row['journal_full_title']):
        fail(line_str + 'the column "journal_full_title" must not be empty')
    if len(row['journal_full_title']) != len(row['journal_full_title'].strip()):
        fail(line_str + 'journal title (' + row['journal_full_title'] + ') has leading or trailing whitespaces')
    if not oat.has_value(row['issn']):
        fail(line_str + 'the column "issn" must not be empty')
    if row['doaj'] not in ["TRUE", "FALSE"]:
        fail(line_str + 'value in row "doaj" must either be TRUE or FALSE')
    if row['is_hybrid'] not in ["TRUE", "FALSE"]:
        fail(line_str + 'value in row "is_hybrid" must either be TRUE or FALSE')
    
    if row_object.origin == "ta":
        if not oat.has_value(row['agreement']):
            fail(line_str + 'the column "agreement" must not be empty')
    if not row_object.origin == "ta":
        try:
            euro = float(row['euro'])
            if euro <= 0:
                fail(line_str + 'value in row "euro" (' + row['euro'] + ') must be larger than 0')
        except ValueError:
            fail(line_str + 'value in row "euro" (' + row['euro'] + ') is no valid number')

def check_ac_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if not oat.has_value(row['doi']):
        fail(line_str + 'the column "doi" must not be empty')
    cost_data_found = False
    for cost_field in ["colour charge", "cover charge", "page charge", "permission", "reprint", "submission fee", "payment fee", "other"]:
        if row[cost_field] is None:
            fail(line_str + 'cost field "' + cost_field + '" not found. The row is probably malformed')
            return
        if oat.has_value(row[cost_field]):
            try:
                euro = float(row[cost_field])
                if euro <= 0:
                    fail(line_str + 'value in row "' + cost_field + '" (' + row[cost_field] + ') must be larger than 0')
                else:
                    cost_data_found = True
            except ValueError:
                fail(line_str + 'value in row "' + cost_field + '" (' + row[cost_field] + ') is no valid number')
    if not cost_data_found:
        fail(line_str + 'no valid euro amount found in any cost column')

def check_ac_doi_links(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    ac_metadata = DATA_FILES[row_object.origin]
    target_files = ac_metadata["is_ac_file_for"]
    for target_file in target_files:
        if row["doi"] in DATA_FILES[target_file]["doi_list"]:
            break
    else:
        msg = line_str + 'DOI {} does not occur in any of the target primary data files ({})'
        fail(msg.format(row["doi"], ", ".join(target_files)))

def check_bpc_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if not oat.has_value(row['book_title']):
        fail(line_str + 'the column "book_title" must not be empty')
    if len(row['book_title']) != len(row['book_title'].strip()):
        fail(line_str + 'book title (' + row['book_title'] + ') has leading or trailing whitespaces')
    if row['backlist_oa'] not in ["TRUE", "FALSE"]:
        fail(line_str + 'value in row "backlist_oa" must either be TRUE or FALSE')
    if row['doab'] not in ["TRUE", "FALSE"]:
        fail(line_str + 'value in row "doab" must either be TRUE or FALSE')

def check_contract_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    for field in ["institution", "contract_name", "period_from", "period_to", "group_id"]:
        if not oat.has_value(row[field]):
            fail(line_str + 'the column "' + field + '" must not be empty')
    try:
        from_date = datetime.datetime.strptime(row['period_from'], "%Y")
        to_date = datetime.datetime.strptime(row['period_to'], "%Y")
        if to_date < from_date:
            msg = 'the to_period date {} occurs earlier than the from_period date {}'
            fail(line_str + msg.format(row["period_to"], row["period_from"]))
    except ValueError:
        msg = 'at least one period value (from/to) could not be parsed as a year value'
        fail(line_str + msg)
    #TODO: Check cost type against vocab?
    if oat.has_value(row["euro"]):
        try:
            euro = float(row["euro"])
        except ValueError:
            fail(line_str + 'contract euro value (' + row["euro"] + ') is no valid number')

def check_issns(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    for issn_column in [row["issn"], row["issn_print"], row["issn_electronic"], row["issn_l"]]:
        if issn_column != "NA":
            if not oat.is_wellformed_ISSN(issn_column):
                fail(line_str + 'value "' + issn_column + '" is not a ' +
                            'well-formed ISSN')
            elif not oat.is_valid_ISSN(issn_column):
                fail(line_str + 'value "' + issn_column + '" is no valid ' +
                            'ISSN (check digit mismatch)')
    issn_l = row["issn_l"]
    if issn_l != "NA":
        msg = line_str + "Two entries share a common {} ({}), but the {} differs ({} vs {})"
        issn = row["issn"]
        if issn != "NA":
            for reduced_row in issn_dict[issn]:
                if reduced_row["issn_l"] != issn_l:
                    fail(msg.format("issn", issn, "issn_l", issn_l, reduced_row["issn_l"]))
        issn_p = row["issn_print"]
        if issn_p != "NA":
            for reduced_row in issn_p_dict[issn_p]:
                if reduced_row["issn_l"] != issn_l:
                    fail(msg.format("issn_p", issn_p, "issn_l", issn_l, reduced_row["issn_l"]))
        issn_e = row["issn_electronic"]
        if issn_e != "NA":
            for reduced_row in issn_e_dict[issn_e]:
                if reduced_row["issn_l"] != issn_l:
                    fail(msg.format("issn_e", issn_e, "issn_l", issn_l, reduced_row["issn_l"]))
        title = reduced_row["journal_full_title"]
        if title not in title_dict:
            title_dict[title] = issn_l
        else:
            other_issn_l = title_dict[title]
            if other_issn_l != issn_l and not wl.is_ambiguous_title(title, issn_l, other_issn_l):
                fail(msg.format("journal_full_title", title, "issn_l", issn_l, other_issn_l))

def check_isbns(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    isbn = row["isbn"]
    publisher = row["publisher"]
    if not oat.has_value(isbn):
        fail(line_str + 'The isbn column may not be empty')
        return
    test_result = ISBNHANDLING.test_and_normalize_isbn(isbn)
    if not test_result["valid"]:
        error = ISBNHANDLING.ISBN_ERRORS[test_result["error_type"]]
        fail(line_str + 'The isbn is invalid: ' + error)
        return
    group_and_publisher = _get_isbn_group_publisher(isbn)
    for other_publisher in isbn_dict[group_and_publisher]:
        if other_publisher != publisher and not wl.publisher_identity(publisher, other_publisher):
            msg = line_str + ('Two book entries share a common group-publisher combination in ' +
                              'their ISBNs ({}), but the publisher name differs ("{}" vs "{}")')
            fail(msg.format(group_and_publisher, publisher, other_publisher))

def check_for_doi_duplicates(row_object):
    __tracebackhide__ = True
    doi = row_object.row["doi"]
    if doi and doi != "NA":
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        global_doi_list.remove(doi)
        if doi in global_doi_list:
            fail(line_str + 'Duplicate: DOI "' + doi + '" was ' +
                        'encountered more than one time')
        if row_object.origin in KNOWN_DUPLICATES:
            for dup_file_name, file_dict in KNOWN_DUPLICATES[row_object.origin].items():
                if doi in file_dict["doi_list"]:
                    msg = 'DOI "{}" is listed in {} and should not appear in {}'
                    msg = msg.format(doi, dup_file_name, DATA_FILES[row_object.origin]["file_path"])
                    fail(line_str + msg)

def check_for_url_duplicates(row_object):
    __tracebackhide__ = True
    url = row_object.row["url"]
    if url and url != "NA":
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        norm_url = _normalize_url(url)
        global_url_list.remove(norm_url)
        if norm_url in global_url_list:
            norm_string = " (Original form: '" + url + "')" if norm_url != url else ""
            fail(line_str + 'Duplicate: Normalized URL "' + norm_url + '" was ' +
                        'encountered more than one time' + norm_string)

def check_for_isbn_duplicates(row_object):
    __tracebackhide__ = True
    isbn_list = []
    # prepare a deduplicated list
    for isbn_type in ["isbn", "isbn_print", "isbn_electronic"]:
        isbn = row_object.row[isbn_type]
        if oat.has_value(isbn) and isbn not in isbn_list and isbn not in wl.NON_DUPLICATE_ISBNS:
            isbn_list.append(isbn)
    for isbn in isbn_list:
        global_isbn_list.remove(isbn)
        if isbn in global_isbn_list:
            line_str = '{}, line {}: '.format(row_object.file_name,
                                              row_object.line_number)
            fail(line_str + 'Duplicate: ISBN "' + isbn + '" was ' +
                 'encountered more than one time')

def check_hybrid_status(row_object):
    __tracebackhide__ = True
    doaj = row_object.row["doaj"]
    is_hybrid = row_object.row["is_hybrid"]
    issn = row_object.row["issn"]
    title = row_object.row["journal_full_title"]
    if doaj == "TRUE" and is_hybrid == "TRUE" and issn not in wl.JOURNAL_HYBRID_STATUS_CHANGED:
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        msg = 'Journal "{}" ({}) is listed in the DOAJ but is marked as hybrid (DOAJ only lists fully OA journals)'
        msg = msg.format(title, issn)
        fail(line_str + msg)

def check_contract_consistency(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    msg = (line_str + 'Two contract entries share a common {} ({}), but the ' +
           '{} differs ("{}" vs "{}")')
    group_id = row["group_id"]
    same_group_id_rows = group_id_dict[group_id]
    for other_row in same_group_id_rows:
        for field in ["institution", "contract_name", "identifier", "consortium"]:
            if row[field] != other_row[field]:
                msg = msg.format("group_id", group_id, field, row[field], other_row[field])
                fail(msg)
    identifier = row["identifier"]
    if oat.has_value(identifier):
        same_identifier_rows = identifier_dict[identifier]
        for other_row in same_identifier_rows:
            for field in ["contract_name", "consortium"]:
                if row[field] != other_row[field]:
                    msg = msg.format("identifier", identifier, field, row[field], other_row[field])
                    fail(msg)

def check_name_consistency(row_object):
    __tracebackhide__ = True
    row = row_object.row
    issn = row["issn"] if oat.has_value(row["issn"]) else None
    issn_p = row["issn_print"] if oat.has_value(row["issn_print"]) else None
    issn_e = row["issn_electronic"] if oat.has_value(row["issn_electronic"]) else None
    issn_l = row["issn_l"] if oat.has_value(row["issn_l"]) else None
    hybrid_status_changed = len({issn, issn_p, issn_e, issn_l}.intersection(wl.JOURNAL_HYBRID_STATUS_CHANGED)) > 0
    journal = row["journal_full_title"]
    publ = row["publisher"]
    hybrid = row["is_hybrid"]
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    msg = (u'' + line_str + 'Two entries share a common {}ISSN ({}), but the ' +
           '{} differs ("{}" vs "{}")')
    if issn is not None:
        same_issn_rows = issn_dict[issn]
        for other_row in same_issn_rows:
            other_publ = other_row["publisher"]
            other_journal = other_row["journal_full_title"]
            other_hybrid = other_row["is_hybrid"]
            if not other_publ == publ and not wl.in_whitelist(issn, publ, other_publ):
                ret = msg.format("", issn, "publisher name", publ, other_publ)
                fail(ret)
            if not other_journal == journal:
                ret = msg.format("", issn, "journal title", journal, other_journal)
                fail(ret)
            if other_hybrid != hybrid and not hybrid_status_changed:
                ret = msg.format("", issn, "hybrid status", hybrid, other_hybrid)
                fail(ret)
    if issn_p is not None:
        same_issn_p_rows = issn_p_dict[issn_p]
        for other_row in same_issn_p_rows:
            other_publ = other_row["publisher"]
            other_journal = other_row["journal_full_title"]
            other_hybrid = other_row["is_hybrid"]
            if not other_publ == publ and not wl.in_whitelist(issn_p, publ, other_publ):
                ret = msg.format("Print ", issn_p, "publisher name", publ, other_publ)
                fail(ret)
            if not other_journal == journal:
                ret = msg.format("Print ", issn_p, "journal title", journal, other_journal)
                fail(ret)
            if other_hybrid != hybrid and not hybrid_status_changed:
                ret = msg.format("Print ", issn_p, "hybrid status", hybrid, other_hybrid)
                fail(ret)
    if issn_e is not None:
        same_issn_e_rows = issn_e_dict[issn_e]
        for other_row in same_issn_e_rows:
            other_publ = other_row["publisher"]
            other_journal = other_row["journal_full_title"]
            other_hybrid = other_row["is_hybrid"]
            if not other_publ == publ and not wl.in_whitelist(issn_e, publ, other_publ):
                ret = msg.format("Electronic ", issn_e, "publisher name", publ, other_publ)
                fail(ret)
            if not other_journal == journal:
                ret = msg.format("Electronic ", issn_e, "journal title", journal, other_journal)
                fail(ret)
            if other_hybrid != hybrid and not hybrid_status_changed:
                ret = msg.format("Electronic ", issn_e, "hybrid status", hybrid, other_hybrid)
                fail(ret)
    if issn_l is not None:
        same_issn_l_rows = issn_l_dict[issn_l]
        for other_row in same_issn_l_rows:
            other_publ = other_row["publisher"]
            other_journal = other_row["journal_full_title"]
            other_hybrid = other_row["is_hybrid"]
            if not other_publ == publ and not wl.in_whitelist(issn_l, publ, other_publ):
                ret = msg.format("Linking ", issn_l, "publisher name", publ, other_publ)
                fail(ret)
            if not other_journal == journal:
                ret = msg.format("Linking ", issn_l, "journal title", journal, other_journal)
                fail(ret)
            if other_hybrid != hybrid and not hybrid_status_changed:
                ret = msg.format("Linking ", issn_l, "hybrid status", hybrid, other_hybrid)
                fail(ret)

def check_ta_data(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if row_object.origin == "ta":
        agreement = row["agreement"]
        publisher = row["publisher"]
        doi = row["doi"]
        if not oat.has_value(row["group_id"]):
            msg = 'missing group_id for agreement "{}" [{}]'
            ret = line_str + msg.format(agreement, doi)
            fail(ret)
        group_id = row["group_id"]
        if group_id not in group_id_dict:
            msg = 'group_id "{}" not found in contracts file [{}]'
            ret = line_str + msg.format(group_id, doi)
            fail(ret)
        publisher = mappings.AGREEMENT_PUBLISHER_MAP.get(publisher, publisher)
        if group_id not in group_id_publisher_dict:
            group_id_publisher_dict[group_id] = publisher
        elif group_id_publisher_dict[group_id] != publisher:
            msg = 'publisher mismatch found for group_id "{}": {} <> {} [{}]'
            ret = line_str + msg.format(group_id, publisher, group_id_publisher_dict[group_id], doi)
            fail(ret)

@pytest.mark.parametrize("row_object", APC_DATA)
class TestAPCRows(object):

    # Set of tests to run on all APC data
    def test_row_format(self, row_object):
        check_line_length(row_object)
        check_common_field_content(row_object)
        check_apc_field_content(row_object)
        check_optional_identifier(row_object)
        check_issns(row_object)
        check_hybrid_status(row_object)
        check_for_doi_duplicates(row_object)
        check_name_consistency(row_object)
        check_ta_data(row_object)

@pytest.mark.parametrize("row_object", BPC_DATA)
class TestBPCRows(object):

    # Set of tests to run on all BPC data
    def test_row_format(self, row_object):
        check_line_length(row_object)
        check_common_field_content(row_object)
        check_bpc_field_content(row_object)
        check_isbns(row_object)
        check_for_isbn_duplicates(row_object)
        check_for_doi_duplicates(row_object)

@pytest.mark.parametrize("row_object", ARTICLE_AC_DATA)
class TestAPCACRows(object):

    # Set of tests to run on all APC AC data
    def test_row_format(self, row_object):
        check_line_length(row_object)
        check_ac_field_content(row_object)
        check_ac_doi_links(row_object)

if __name__ == '__main__':
    oat.print_b(str(len(APC_DATA)) + " APC records collected, starting tests...")
    deciles = {round((len(APC_DATA)/10) * i): str(i * 10) + "%" for i in range(1, 10)}
    for num, row_object in enumerate(APC_DATA):
        if num in deciles:
            oat.print_b(deciles[num])
        check_line_length(row_object)
        check_common_field_content(row_object)
        check_apc_field_content(row_object)
        check_optional_identifier(row_object)
        check_issns(row_object)
        check_hybrid_status(row_object)
        check_for_doi_duplicates(row_object)
        check_for_url_duplicates(row_object)
        check_name_consistency(row_object)
        check_ta_data(row_object)
    oat.print_b(str(len(ARTICLE_AC_DATA)) + " APC AC records collected, starting tests...")
    deciles = {round((len(ARTICLE_AC_DATA)/10) * i): str(i * 10) + "%" for i in range(1, 10)}
    for num, row_object in enumerate(ARTICLE_AC_DATA):
        if num in deciles:
            oat.print_b(deciles[num])
        check_line_length(row_object)
        check_ac_field_content(row_object)
        check_ac_doi_links(row_object)
    oat.print_b(str(len(BPC_DATA)) + " BPC records collected, starting tests...")
    deciles = {round((len(BPC_DATA)/10) * i): str(i * 10) + "%" for i in range(1, 10)}
    for num, row_object in enumerate(BPC_DATA):
        if num in deciles:
            oat.print_b(deciles[num])
        check_line_length(row_object)
        check_common_field_content(row_object)
        check_bpc_field_content(row_object)
        check_isbns(row_object)
        check_for_isbn_duplicates(row_object)
        check_for_doi_duplicates(row_object)
    oat.print_b(str(len(CONTRACTS_DATA)) + " contract records collected, starting tests...")
    deciles = {round((len(CONTRACTS_DATA)/10) * i): str(i * 10) + "%" for i in range(1, 10)}
    for num, row_object in enumerate(CONTRACTS_DATA):
        if num in deciles:
            oat.print_b(deciles[num])
        check_line_length(row_object)
        check_contract_field_content(row_object)
        check_contract_consistency(row_object)
