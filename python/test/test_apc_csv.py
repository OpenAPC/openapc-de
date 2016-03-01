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
    def test_row(self, row):
        assert len(row) == 17
        assert row['doaj'] in ["TRUE", "FALSE"]
        assert row['indexed_in_crossref'] in ["TRUE", "FALSE"]
        assert row['is_hybrid'] in ["TRUE", "FALSE"]
        assert oat.is_wellformed_DOI(row['doi']) or row['doi'] == "NA"
        if row['doi'] == "NA":
            assert has_value(row['publisher'])
            assert has_value(row['journal_full_title'])
            assert has_value(row['issn'])
            assert has_value(row['url'])

    def test_doi_duplicates(self, row):
        doi = row["doi"]
        if doi and doi != "NA":
            doi_list.remove(doi)
            assert doi not in doi_list
          
