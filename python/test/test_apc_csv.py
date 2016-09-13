import pytest

import openapc_toolkit as oat

# A whitelist for denoting publisher identity (Possible consequence of business buy outs or fusions)
# If one publisher name is stored in the left list of an entry and another in the right one,
# they will not be treated as different by the name_consistency test.
PUBLISHER_IDENTITY = [
    (["Springer Nature"], ["Nature Publishing Group", "Springer Science + Business Media"]),
    (["Springer Science + Business Media"], ["BioMed Central", "American Vacuum Society"]),
    (["Wiley-Blackwell"], ["EMBO"]),
    (["Pion Ltd"], ["SAGE Publications"])
]


# A whitelist for denoting changes in journal ownership.
JOURNAL_OWNER_CHANGED = {
    "1744-8069": ["SAGE Publications", "Springer Science + Business Media"]
}

class RowObject(object):
    """
    A minimal container class to store contextual information along with csv rows.
    """
    def __init__(self, file_name, line_number, row):
        self.file_name = file_name
        self.line_number = line_number
        self.row = row

doi_duplicate_list = []
apc_data = []

for file_name in ["data/apc_de.csv", "data/offsetting/offsetting.csv"]:
    csv_file = open(file_name, "r")
    reader = oat.UnicodeDictReader(csv_file)
    line = 2
    for row in reader:
        apc_data.append(RowObject(file_name, line, row))
        doi_duplicate_list.append(row["doi"])
        line += 1
    csv_file.close()

def has_value(field):
    return len(field) > 0 and field != "NA"

def in_whitelist(issn, first_publisher, second_publisher):
    for entry in PUBLISHER_IDENTITY:
        if first_publisher in entry[0] and second_publisher in entry[1]:
            return True
        if first_publisher in entry[1] and second_publisher in entry[0]:
            return True
    if issn in JOURNAL_OWNER_CHANGED:
        return (first_publisher in JOURNAL_OWNER_CHANGED[issn] and
                second_publisher in JOURNAL_OWNER_CHANGED[issn])
    return False

def check_line_length(row_object):
    __tracebackhide__ = True
    if len(row_object.row) != 17:
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        pytest.fail(line_str + 'Row must consist of exactly 17 items')

def check_optional_fields(row_object):
    __tracebackhide__ = True
    row = row_object.row
    if row['doi'] == "NA":
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        if not has_value(row['publisher']):
            pytest.fail(line_str + 'if no DOI is given, the column ' +
                        '"publisher" must not be empty')
        if not has_value(row['journal_full_title']):
            pytest.fail(line_str + 'if no DOI is given, the column ' +
                        '"journal_full_title" must not be empty')
        if not has_value(row['issn']):
            pytest.fail(line_str + 'if no DOI is given, the column "issn" ' +
                        'must not be empty')
        if not has_value(row['url']):
            pytest.fail(line_str + 'if no DOI is given, the column "url" ' +
                        'must not be empty')

def check_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if row['doaj'] not in ["TRUE", "FALSE"]:
        pytest.fail(line_str + 'value in row "doaj" must either be TRUE or FALSE')
    if row['indexed_in_crossref'] not in ["TRUE", "FALSE"]:
        pytest.fail(line_str + 'value in row "indexed_in_crossref" must either be TRUE or FALSE')
    if row['is_hybrid'] not in ["TRUE", "FALSE"]:
        pytest.fail(line_str + 'value in row "is_hybrid" must either be TRUE or FALSE')
    if not oat.is_wellformed_DOI(row['doi']) and not row['doi'] == "NA":
        pytest.fail(line_str + 'value in row "doi" must either be NA or represent a valid DOI')

def check_issns(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    for issn_column in [row["issn"], row["issn_print"], row["issn_electronic"]]:
        if issn_column != "NA":
            issn_strings = issn_column.split(";")
            for issn in issn_strings:
                if not oat.is_wellformed_ISSN(issn):
                    pytest.fail(line_str + 'value "' + issn + '" is not a ' +
                                'well-formed ISSN')
                if not oat.is_valid_ISSN(issn):
                    pytest.fail(line_str + 'value "' + issn + '" is no valid ' +
                                'ISSN (check digit mismatch)')

def check_for_doi_duplicates(row_object):
    __tracebackhide__ = True
    doi = row_object.row["doi"]
    if doi and doi != "NA":
        doi_duplicate_list.remove(doi)
        if doi in doi_duplicate_list:
            line_str = '{}, line {}: '.format(row_object.file_name,
                                              row_object.line_number)
            pytest.fail(line_str + 'Duplicate: DOI "' + doi + '" was ' +
                        'encountered more than one time')

def check_name_consistency(row_object):
    __tracebackhide__ = True
    row = row_object.row
    issn = row["issn"] if has_value(row["issn"]) else None
    issn_p = row["issn_print"] if has_value(row["issn_print"]) else None
    issn_e = row["issn_electronic"] if has_value(row["issn_electronic"]) else None
    journal = row["journal_full_title"]
    publ = row["publisher"]
    hybrid = row["is_hybrid"]
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    msg = (u'' + line_str + 'Two entries share a common {}ISSN ({}), but the ' +
           '{} differs ("{}" vs "{}")')
    for other_row_object in apc_data:
        other_row = other_row_object.row
        other_publ = other_row["publisher"]
        other_journal = other_row["journal_full_title"]
        other_hybrid = other_row["is_hybrid"]
        if issn is not None and other_row["issn"] == issn:
            if not other_publ == publ and not in_whitelist(issn, publ, other_publ):
                ret = msg.format("", issn, "publisher name", publ, other_publ)
                pytest.fail(ret)
            if not other_journal == journal:
                ret = msg.format("", issn, "journal title", journal, other_journal)
                pytest.fail(ret)
            if not other_hybrid == hybrid:
                ret = msg.format("", issn, "hybrid status", hybrid, other_hybrid)
                pytest.fail(ret)
        elif issn_p is not None and other_row["issn_print"] == issn_p:
            if not other_publ == publ and not in_whitelist(issn, publ, other_publ):
                ret = msg.format("Print ", issn_p, "publisher name", publ, other_publ)
                pytest.fail(ret)
            if not other_journal == journal:
                ret = msg.format("Print ", issn_p, "journal title", journal, other_journal)
                pytest.fail(ret)
            if not other_hybrid == hybrid:
                ret = msg.format("Print", issn_p, "hybrid status", hybrid, other_hybrid)
                pytest.fail(ret)
        elif issn_e is not None and other_row["issn_electronic"] == issn_e:
            if not other_publ == publ and not in_whitelist(issn, publ, other_publ):
                ret = msg.format("Electronic ", issn_e, "publisher name", publ, other_publ)
                pytest.fail(ret)
            if not other_journal == journal:
                ret = msg.format("Electronic ", issn_e, "journal title", journal, other_journal)
                pytest.fail(ret)
            if not other_hybrid == hybrid:
                ret = msg.format("Electronic", issn_e, "hybrid status", hybrid, other_hybrid)
                pytest.fail(ret)

@pytest.mark.parametrize("row_object", apc_data)
class TestAPCRows(object):

    # Set of tests to run on every single row
    def test_row_format(self, row_object):
        check_line_length(row_object)
        check_field_content(row_object)
        check_optional_fields(row_object)
        check_issns(row_object)

    def test_doi_duplicates(self, row_object):
        check_for_doi_duplicates(row_object)

    def test_name_consistency(self, row_object):
        check_name_consistency(row_object)
