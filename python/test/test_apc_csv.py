import pytest
from pytest import fail

from csv import DictReader
from os.path import dirname, join
from sys import path

APC_DATA = []
BPC_DATA = []

DATA_FILES = {
    "apc": {
        "file_path": "data/apc_de.csv",
        "unused_fields": ["institution", "period", "license_ref", "pmid", "pmcid", "ut"],
        "target_file": APC_DATA,
        "row_length": 18,
        "has_issn": True,
        "has_isbn": False
    },
    "ta": {
        "file_path": "data/transformative_agreements/transformative_agreements.csv",
        "unused_fields": ["institution", "period", "license_ref", "pmid", "pmcid", "ut"],
        "target_file": APC_DATA,
        "row_length": 19,
        "has_issn": True,
        "has_isbn": False
    },
    "bpc": {
        "file_path": "data/bpc.csv",
        "unused_fields": ["institution", "period", "license_ref"],
        "target_file": BPC_DATA,
        "row_length": 13,
        "has_issn": False,
        "has_isbn": True
    }
}

ISBNHANDLING = None

if __name__ == '__main__':
    path.append(dirname(path[0]))
    import openapc_toolkit as oat
    import mappings
    import whitelists as wl
    ISBNHANDLING = oat.ISBNHandling("ISBNRangeFile.xml")
    for data_file, metadata in DATA_FILES.items():
        metadata["file_path"] = join("..", "..", metadata["file_path"])

    def fail(msg):
        oat.print_r(msg)

else:
    path.append(join(path[0], "python"))
    import openapc_toolkit as oat
    import mappings
    from . import whitelists as wl
    ISBNHANDLING = oat.ISBNHandling("python/test/ISBNRangeFile.xml")

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

doi_duplicate_list = []
isbn_duplicate_list = []
issn_dict = {}
issn_p_dict = {}
issn_e_dict = {}
issn_l_dict = {}

isbn_dict = {}

ISSN_DICT_FIELDS = ["is_hybrid", "publisher", "journal_full_title", "issn_l"]

for data_file, metadata in DATA_FILES.items():
    with open(metadata["file_path"], "r") as csv_file:
        reader = DictReader(csv_file)
        line = 2
        for row in reader:
            for field in metadata["unused_fields"]:
                del(row[field])
            metadata["target_file"].append(RowObject(metadata["file_path"], line, row, data_file))
            doi_duplicate_list.append(row["doi"])

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
                isbn_duplicate_list += isbn_list
            line += 1

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
            
def check_bpc_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if not oat.has_value(row['book_title']):
        fail(line_str + 'the column "book_title" must not be empty')
    if len(row['book_title']) != len(row['book_title'].strip()):
        fail(line_str + 'book title (' + row['book_title'] + ') has leading or trailing whitespaces')

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
        msg = line_str + "Two entries share a common {} ({}), but the issn_l differs ({} vs {})"
        issn = row["issn"]
        if issn != "NA":
            for reduced_row in issn_dict[issn]:
                if reduced_row["issn_l"] != issn_l:
                    fail(msg.format("issn", issn, issn_l, reduced_row["issn_l"]))
        issn_p = row["issn_print"]
        if issn_p != "NA":
            for reduced_row in issn_p_dict[issn_p]:
                if reduced_row["issn_l"] != issn_l:
                    fail(msg.format("issn_p", issn_p, issn_l, reduced_row["issn_l"]))
        issn_e = row["issn_electronic"]
        if issn_e != "NA":
            for reduced_row in issn_e_dict[issn_e]:
                if reduced_row["issn_l"] != issn_l:
                    fail(msg.format("issn_e", issn_e, issn_l, reduced_row["issn_l"]))

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
        doi_duplicate_list.remove(doi)
        if doi in doi_duplicate_list:
            line_str = '{}, line {}: '.format(row_object.file_name,
                                              row_object.line_number)
            fail(line_str + 'Duplicate: DOI "' + doi + '" was ' +
                        'encountered more than one time')

def check_for_isbn_duplicates(row_object):
    __tracebackhide__ = True
    isbn_list = []
    # prepare a deduplicated list
    for isbn_type in ["isbn", "isbn_print", "isbn_electronic"]:
        isbn = row_object.row[isbn_type]
        if oat.has_value(isbn) and isbn not in isbn_list and isbn not in wl.NON_DUPLICATE_ISBNS:
            isbn_list.append(isbn)
    for isbn in isbn_list:
        isbn_duplicate_list.remove(isbn)
        if isbn in isbn_duplicate_list:
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
    if "agreement" in row:
        agreement = row["agreement"]
        publisher = row["publisher"]
        if agreement in mappings.AGREEMENT_PUBLISHERS:
            if publisher not in mappings.AGREEMENT_PUBLISHERS[agreement]:
                msg = '"{}" is no valid publisher name for the agreement "{}"'
                ret = line_str + msg.format(publisher, agreement)
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
        check_name_consistency(row_object)
        check_ta_data(row_object)
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
