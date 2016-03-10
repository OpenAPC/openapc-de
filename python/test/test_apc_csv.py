import pytest
import re

import openapc_toolkit as oat

csv_file = open("data/apc_de.csv", "r")
reader = oat.UnicodeDictReader(csv_file)
apc_data = []
doi_list = []
for row in reader:
    apc_data.append(row)
    doi_list.append(row["doi"])

def has_value(field):
    return len(field) > 0 and field != "NA"

@pytest.mark.parametrize("row", apc_data)
class TestAPCRows(object):
    
    # Set of tests to run on every single row
    def test_row_format(self, row):
        assert len(row) == 17, 'row must consist of exactly 17 items'
        assert row['doaj'] in ["TRUE", "FALSE"], 'value in row "doaj" must either be TRUE or FALSE'
        assert row['indexed_in_crossref'] in ["TRUE", "FALSE"], 'value in row "indexed_in_crossref" must either be TRUE or FALSE'
        assert row['is_hybrid'] in ["TRUE", "FALSE"], 'value in row "is_hybrid" must either be TRUE or FALSE'
        assert oat.is_wellformed_DOI(row['doi']) or row['doi'] == "NA", 'value in row "doi" must either be NA or represent a valid DOI'
        if row['doi'] == "NA":
            assert has_value(row['publisher']), 'if no DOI is given, the column "publisher" must not be empty'
            assert has_value(row['journal_full_title']), 'if no DOI is given, the column "journal_full_title" must not be empty'
            assert has_value(row['issn']), 'if no DOI is given, the column "issn" must not be empty'
            assert has_value(row['url']), 'if no DOI is given, the column "url" must not be empty'

    def test_doi_duplicates(self, row):
        doi = row["doi"]
        if doi and doi != "NA":
            doi_list.remove(doi)
            assert doi not in doi_list, 'Duplicate: A DOI was encountered more than one time'
            
    def test_name_consistency(self, row):
        issn = row["issn"] if has_value(row["issn"]) else None
        issn_p = row["issn_print"] if has_value(row["issn_print"]) else None
        issn_e = row["issn_electronic"] if has_value(row["issn_electronic"]) else None
        journal_full_title = row["journal_full_title"]
        publisher = row["publisher"]
        for other_row in apc_data:
            if issn is not None and other_row["issn"] == issn:
                assert other_row["publisher"] == publisher, 'Two entries share a common ISSN, but the publisher name differs'
                assert other_row["journal_full_title"] == journal_full_title, 'Two entries share a common ISSN, but the journal title differs'
            elif issn_p is not None and other_row["issn_print"] == issn_p:
                assert other_row["publisher"] == publisher, 'Two entries share a common Print ISSN, but the publisher name differs'
                assert other_row["journal_full_title"] == journal_full_title, 'Two entries share a common Print ISSN, but the journal title differs'
            elif issn_e is not None and other_row["issn_electronic"] == issn_e:
                assert other_row["publisher"] == publisher, 'Two entries share a common Electronic ISSN, but the publisher name differs'
                assert other_row["journal_full_title"] == journal_full_title, 'Two entries share a common Electronic ISSN, but the journal title differs'
