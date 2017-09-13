import pytest

from .. import openapc_toolkit as oat

# A whitelist for denoting publisher identity (Possible consequence of business buy outs or fusions)
# If one publisher name is stored in the left list of an entry and another in the right one,
# they will not be treated as different by the name_consistency test.
PUBLISHER_IDENTITY = [
    (["Springer Nature"], ["Nature Publishing Group", "Springer Science + Business Media"]),
    (["Springer Science + Business Media"], ["BioMed Central", "American Vacuum Society"]),
    (["Wiley-Blackwell"], ["EMBO"]),
    (["Pion Ltd"], ["SAGE Publications"]),
    (["Wiley-Blackwell"], ["American Association of Physicists in Medicine (AAPM)"]),
    (["Informa Healthcare"], ["Informa UK Limited"]), # Usage very inconsistent in crossref data
    (["GeoScienceWorld"], ["Mineralogical Society of America"])
]


# A whitelist for denoting changes in journal ownership.
JOURNAL_OWNER_CHANGED = {
    "1744-8069": ["SAGE Publications", "Springer Science + Business Media"],
    "1990-2573": ["European Optical Society", "Springer Nature"],
    "1755-7682": ["Springer Science + Business Media", "International Medical Publisher (Fundacion de Neurociencias)"], # International Archives of Medicine
    "2000-8198": ["Co-Action Publishing", "Informa UK Limited"], # European Journal of Psychotraumatology
    "0024-4066": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Biological Journal of the Linnean Society
    "0024-4074": ["Wiley-Blackwell", "Oxford University Press (OUP)"], #  Botanical Journal of the Linnean Society
    "1087-2981": ["Co-Action Publishing", "Informa UK Limited"], # Medical Education Online
    "1654-9716": ["Co-Action Publishing", "Informa UK Limited"], # Global Health Action (print)
    "1654-9880": ["Co-Action Publishing", "Informa UK Limited"], # Global Health Action
    "1176-9343": ["Libertas Academica, Ltd.", "SAGE Publications"], # Evolutionary Bioinformatics
    "1574-7891": ["Wiley-Blackwell", "Elsevier BV"], # Molecular Oncology
    "0020-7292": ["Wiley-Blackwell", "Elsevier BV"], # "International Journal of Gynecology & Obstetrics"
    "1525-0016": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # Molecular Therapy
    "2000-8198": ["Co-Action Publishing", "Informa UK Limited"], # European Journal of Psychotraumatology (print)
    "2000-8066": ["Co-Action Publishing", "Informa UK Limited"], # European Journal of Psychotraumatology
    "1600-0889": ["Co-Action Publishing", "Informa UK Limited"], # Tellus B
    "1654-6628": ["Co-Action Publishing", "Informa UK Limited"], # Food & Nutrition Research (print)
    "1654-661X": ["Co-Action Publishing", "Informa UK Limited"], # Food & Nutrition Research (electronic)
    "0038-0261": ["Wiley-Blackwell", "SAGE Publications"], # The Sociological Review
    "2162-2531": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # "Molecular Therapy-Nucleic Acids"
    "0009-9236": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics
    "1940-0829": ["Mongabay", "SAGE Publications"], # Tropical Conservation Science, acquired by SAGE in 08/2016
    "1600-0870": ["Co-Action Publishing", "Informa UK Limited"], # Tellus A
    "0963-6897": ["Cognizant Electronic Publishing", "SAGE Publications"], # Cell Transplantation
    "1555-3892": ["Cognizant Electronic Publishing", "SAGE Publications"], # Cell Transplantation (electronic)
    "0021-4922": ["Japan Society of Applied Physics", "IOP Publishing"], # Japanese Journal of Applied Physics
    "1347-4065": ["Japan Society of Applied Physics", "IOP Publishing"], # Japanese Journal of Applied Physics (electronic)
    "1445-5781": ["Springer Science + Business Media", "Wiley-Blackwell"], # Reproductive Medicine and Biology
    "1538-4357": ["American Astronomical Society", "IOP Publishing"], # The Astrophysical Journal
    "1461-4103": ["Maney Publishing", "Informa UK Limited"], # Environmental Archaeology
    "1749-6314": ["Maney Publishing", "Informa UK Limited"], # Environmental Archaeology (electronic)
    "0039-3630": ["Maney Publishing", "Informa UK Limited"], # Studies in Conservation
    "2047-0584": ["Maney Publishing", "Informa UK Limited"], # Studies in Conservation (electronic)
    "0148-396X": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"] # Neurosurgery
}

# A whiltelist for denoting changes in journal full open access policy. ISSNs
# listed here will not be checked for equal "is_hybrid" status by the name_consistency
# test. Note that we make not further attempts in determining the correct hybrid
# status for any journal listed here (like trying to track a point of time were the
# policy change occured), it is up to the contributing institutions to deliver
# correct data in these cases.
JOURNAL_HYBRID_STATUS_CHANGED = [
    "2041-1723", # Nature Communications
    "1474-9718", # Aging Cell
    "1555-8932", # Genes & Nutrition
    "1756-1833", # BMJ (fully OA status disputed, "added value" content not OA)
    "1461-1457", # International Journal of Neuropsychopharmacology
    "1552-5783", # Investigative Opthalmology & Visual Science, OA since 01/2016
    "0001-4966", # The Journal of the Acoustical Society of America, archives hybrid and non-hybrid sub-journals
    "0887-0446", # Psychology & Health, status unclear -> Possible mistake in Konstanz U data
    "0066-4804", # Antimicrobial Agents and Chemotherapy -> delayed OA journal. Borderline case, needs further discussion
    "0022-1430", # Journal of Glaciology, Gold OA since 2016
    "1467-7644", # Plant Biotechnology Journal, Gold OA since 2016
    "2046-2069", # RSC Advances, Gold OA since 01/2017
    "2041-6520", # Chemical Science, Gold OA since 2015
    "0260-3055", # Annals of Glaciology, Gold OA since 2016
    "1744-5647", # Journal of Maps, Gold OA since 09/2016
    "1445-5781" # Reproductive Medicine and Biology, Gold OA since 2017
]

class RowObject(object):
    """
    A minimal container class to store contextual information along with csv rows.
    """
    def __init__(self, file_name, line_number, row, test_apc=True):
        self.file_name = file_name
        self.line_number = line_number
        self.row = row
        self.test_apc = test_apc

doi_duplicate_list = []
apc_data = []
issn_dict = {}
issn_p_dict = {}
issn_e_dict = {}

for file_name in ["data/apc_de.csv", "data/offsetting/offsetting.csv"]:
    csv_file = open(file_name, "r")
    reader = oat.UnicodeDictReader(csv_file)
    line = 2
    for row in reader:
        test_apc = True
        if file_name == "data/offsetting/offsetting.csv":
            test_apc = False
        apc_data.append(RowObject(file_name, line, row, test_apc))
        doi_duplicate_list.append(row["doi"])
        issn = row["issn"]
        if oat.has_value(issn):
            if issn not in issn_dict:
                issn_dict[issn] = [row]
            else:
                issn_dict[issn].append(row)
        issn_p = row["issn_print"]
        if oat.has_value(issn_p):
            if issn_p not in issn_p_dict:
                issn_p_dict[issn_p] = [row]
            else:
                issn_p_dict[issn_p].append(row)
        issn_e = row["issn_electronic"]
        if oat.has_value(issn_e):
            if issn_e not in issn_e_dict:
                issn_e_dict[issn_e] = [row]
            else:
                issn_e_dict[issn_e].append(row)
        line += 1
    csv_file.close()

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
    if len(row_object.row) != 18:
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        pytest.fail(line_str + 'Row must consist of exactly 18 items')

def check_optional_identifier(row_object):
    __tracebackhide__ = True
    row = row_object.row
    if row['doi'] == "NA":
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        if not oat.has_value(row['url']):
            pytest.fail(line_str + 'if no DOI is given, the column "url" ' +
                        'must not be empty')

def check_field_content(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    if not oat.has_value(row['publisher']):
        pytest.fail(line_str + 'the column "publisher" must not be empty')
    if not oat.has_value(row['journal_full_title']):
        pytest.fail(line_str + 'the column "journal_full_title" must not be empty')
    if not oat.has_value(row['issn']):
        pytest.fail(line_str + 'the column "issn" must not be empty')
    if row['doaj'] not in ["TRUE", "FALSE"]:
        pytest.fail(line_str + 'value in row "doaj" must either be TRUE or FALSE')
    if row['indexed_in_crossref'] not in ["TRUE", "FALSE"]:
        pytest.fail(line_str + 'value in row "indexed_in_crossref" must either be TRUE or FALSE')
    if row['is_hybrid'] not in ["TRUE", "FALSE"]:
        pytest.fail(line_str + 'value in row "is_hybrid" must either be TRUE or FALSE')
    if not row['doi'] == "NA":
        doi_norm = oat.get_normalised_DOI(row['doi'])
        if doi_norm is None:
            pytest.fail(line_str + 'value in row "doi" must either be NA or represent a valid DOI')
        if doi_norm != row['doi']:
            pytest.fail(line_str + 'value in row "doi" contains a valid DOI, but the format ' +
                                   'is not correct. It should be the simple DOI name, not ' +
                                   'handbook notation (doi:...) or a HTTP URI (http://dx.doi.org/...)')
    if len(row['publisher']) != len(row['publisher'].strip()):
        pytest.fail(line_str + 'publisher name (' + row['publisher'] + ') has leading or trailing whitespaces')
    if len(row['journal_full_title']) != len(row['journal_full_title'].strip()):
        pytest.fail(line_str + 'journal title (' + row['journal_full_title'] + ') has leading or trailing whitespaces')
    
    if row_object.test_apc:
        try:
            euro = float(row['euro'])
            if euro <= 0:
                pytest.fail(line_str + 'value in row "euro" (' + row['euro'] + ') must be larger than 0')
        except ValueError:
            pytest.fail(line_str + 'value in row "euro" (' + row['euro'] + ') is no valid number')



def check_issns(row_object):
    __tracebackhide__ = True
    row = row_object.row
    line_str = '{}, line {}: '.format(row_object.file_name, row_object.line_number)
    for issn_column in [row["issn"], row["issn_print"], row["issn_electronic"], row["issn_l"]]:
        if issn_column != "NA":
            if not oat.is_wellformed_ISSN(issn_column):
                pytest.fail(line_str + 'value "' + issn_column + '" is not a ' +
                            'well-formed ISSN')
            if not oat.is_valid_ISSN(issn_column):
                pytest.fail(line_str + 'value "' + issn_column + '" is no valid ' +
                            'ISSN (check digit mismatch)')
    issn_l = row["issn_l"]
    if issn_l != "NA":
        msg = line_str + "Two entries share a common {} ({}), but the issn_l differs ({} vs {})"
        issn = row["issn"]
        if issn != "NA":
            for row in issn_dict[issn]:
                if row["issn_l"] != issn_l:
                    pytest.fail(msg.format("issn", issn, issn_l, row["issn_l"]))
        issn_p = row["issn_print"]
        if issn_p != "NA":
            for row in issn_p_dict[issn_p]:
                if row["issn_l"] != issn_l:
                    pytest.fail(msg.format("issn_p", issn_p, issn_l, row["issn_l"]))
        issn_e = row["issn_electronic"]
        if issn_e != "NA":
            for row in issn_e_dict[issn_e]:
                if row["issn_l"] != issn_l:
                    pytest.fail(msg.format("issn_e", issn_e, issn_l, row["issn_l"]))

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

def check_hybrid_status(row_object):
    __tracebackhide__ = True
    doaj = row_object.row["doaj"]
    is_hybrid = row_object.row["is_hybrid"]
    issn = row_object.row["issn"]
    title = row_object.row["journal_full_title"]
    if doaj == "TRUE" and is_hybrid == "TRUE" and issn not in JOURNAL_HYBRID_STATUS_CHANGED:
        line_str = '{}, line {}: '.format(row_object.file_name,
                                          row_object.line_number)
        msg = 'Journal "{}" ({}) is listed in the DOAJ but is marked as hybrid (DOAJ only lists fully OA journals)'
        msg = msg.format(title, issn)
        pytest.fail(line_str + msg)

def check_name_consistency(row_object):
    __tracebackhide__ = True
    row = row_object.row
    issn = row["issn"] if oat.has_value(row["issn"]) else None
    issn_p = row["issn_print"] if oat.has_value(row["issn_print"]) else None
    issn_e = row["issn_electronic"] if oat.has_value(row["issn_electronic"]) else None
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
            if not other_publ == publ and not in_whitelist(issn, publ, other_publ):
                ret = msg.format("", issn, "publisher name", publ, other_publ)
                pytest.fail(ret)
            if not other_journal == journal:
                ret = msg.format("", issn, "journal title", journal, other_journal)
                pytest.fail(ret)
            if not other_hybrid == hybrid and issn not in JOURNAL_HYBRID_STATUS_CHANGED:
                ret = msg.format("", issn, "hybrid status", hybrid, other_hybrid)
                pytest.fail(ret)
    if issn_p is not None:
        same_issn_p_rows = issn_p_dict[issn_p]
        for other_row in same_issn_p_rows:
            other_publ = other_row["publisher"]
            other_journal = other_row["journal_full_title"]
            other_hybrid = other_row["is_hybrid"]
            if not other_publ == publ and not in_whitelist(issn_p, publ, other_publ):
                ret = msg.format("Print ", issn_p, "publisher name", publ, other_publ)
                pytest.fail(ret)
            if not other_journal == journal:
                ret = msg.format("Print ", issn_p, "journal title", journal, other_journal)
                pytest.fail(ret)
            if not other_hybrid == hybrid and issn not in JOURNAL_HYBRID_STATUS_CHANGED:
                ret = msg.format("Print ", issn_p, "hybrid status", hybrid, other_hybrid)
                pytest.fail(ret)
    if issn_e is not None:
        same_issn_e_rows = issn_e_dict[issn_e]
        for other_row in same_issn_e_rows:
            other_publ = other_row["publisher"]
            other_journal = other_row["journal_full_title"]
            other_hybrid = other_row["is_hybrid"]
            if not other_publ == publ and not in_whitelist(issn_e, publ, other_publ):
                ret = msg.format("Electronic ", issn_e, "publisher name", publ, other_publ)
                pytest.fail(ret)
            if not other_journal == journal:
                ret = msg.format("Electronic ", issn_e, "journal title", journal, other_journal)
                pytest.fail(ret)
            if not other_hybrid == hybrid and issn not in JOURNAL_HYBRID_STATUS_CHANGED:
                ret = msg.format("Electronic ", issn_e, "hybrid status", hybrid, other_hybrid)
                pytest.fail(ret)

@pytest.mark.parametrize("row_object", apc_data)
class TestAPCRows(object):

    # Set of tests to run on every single row
    def test_row_format(self, row_object):
        check_line_length(row_object)
        check_field_content(row_object)
        check_optional_identifier(row_object)
        check_issns(row_object)
        check_hybrid_status(row_object)

    def test_doi_duplicates(self, row_object):
        check_for_doi_duplicates(row_object)

    def test_name_consistency(self, row_object):
        check_name_consistency(row_object)
