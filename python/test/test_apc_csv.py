import pytest
from csv import DictReader

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
    (["GeoScienceWorld"], ["Mineralogical Society of America"]),
    (["International Scientific Literature"], ["International Scientific Information, Inc."]),
    (["Georg Thieme Verlag KG"], ["Thieme Publishing Group"]),
    (["Schattauer GmbH"], ["Georg Thieme Verlag KG"]), # Schattauer bought up by Thieme (1/1/2017)
    (["Johns Hopkins University Press"], ["Project Muse"])
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
    "1654-6628": ["Co-Action Publishing", "Informa UK Limited", "SNF Swedish Nutrition Foundation"], # Food & Nutrition Research (print)
    "1654-661X": ["Co-Action Publishing", "Informa UK Limited", "SNF Swedish Nutrition Foundation"], # Food & Nutrition Research (electronic)
    "0038-0261": ["Wiley-Blackwell", "SAGE Publications"], # The Sociological Review
    "2162-2531": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # "Molecular Therapy-Nucleic Acids"
    "0009-9236": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics
    "1532-6535": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics (electronic)
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
    "0148-396X": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"], # Neurosurgery
    "2047-217X": ["Springer Nature", "Oxford University Press (OUP)"], # GigaScience
    "0007-0912": ["Oxford University Press (OUP)", "Elsevier BV"], # British Journal of Anaesthesia
    "0003-598X": ["Antiquity Publications", "Cambridge University Press (CUP)"], # Antiquity
    "1745-1744": ["Antiquity Publications", "Cambridge University Press (CUP)"], # Antiquity (electronic)
    "0818-9641": ["Nature Publishing Group", "Springer Nature", "Wiley-Blackwell"], # Immunology and Cell Biology
    "1758-2652": ["International AIDS Society", "Wiley-Blackwell"], # Journal of the International AIDS Society
    "1097-3958": ["Springer Nature", "Wiley-Blackwell"], # Journal of Surfactants and Detergents
    "1558-9293": ["Springer Nature", "Wiley-Blackwell"], # Journal of Surfactants and Detergents (electronic)
    "1526-9914": ["Multimed Inc.", "Wiley-Blackwell"], # Journal of Applied Clinical Medical Physics
    "1559-2448": ["International Food and Agribusiness Management Association", "Wageningen Academic Publishers"], # International Food and Agribusiness Management Review
    "1076-1551": ["The Feinstein Institute for Medical Research (North Shore LIJ Research Institute)", "Springer Nature"], # Molecular Medicine
    "1555-4309": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Contrast Media & Molecular Imaging
    "2049-1115": ["HAU, Journal of Ethnographic Theory", "University of Chicago Press"], # HAU: Journal of Ethnographic Theory
    "0197-6729": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Journal of Advanced Transportation
    "0094-8276": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # "Geophysical Research Letters"
    "8755-1209": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Reviews of Geophysics
    "0161-0457": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Scanning
    "2169-9380": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Space Physics
    "1542-7390": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Space Weather
    "2169-897X": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Atmospheres
    "1525-2027": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Geochemistry, Geophysics, Geosystems
    "2328-4277": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Earth's Future
    "1942-2466": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Advances in Modeling Earth Systems
    "0043-1397": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Water Resources Research
    "0886-6236": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Global Biogeochemical Cycles
    "2169-9003": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Earth Surface
    "2169-9275": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Oceans
    "0002-9165": ["American Society for Nutrition", "Oxford University Press (OUP)"], # American Journal of Clinical Nutrition
    "1938-3207": ["American Society for Nutrition", "Oxford University Press (OUP)"], # American Journal of Clinical Nutrition (electronic)
    "0741-5400": ["Society for Leukocyte Biology", "Wiley-Blackwell"], # Journal of Leukocyte Biology
    "2168-0450": ["Botanical Society of America", "Wiley-Blackwell"], # Applications in Plant Sciences
    "1010-4283": ["Springer Science + Business Media", "Springer Nature", "SAGE Publications"], # Tumor Biology
    "1423-0380": ["Springer Science + Business Media", "Springer Nature", "SAGE Publications"], # Tumor Biology (electronic)
    "1530-9932": ["American Association of Pharmaceutical Scientists (AAPS)", "Springer Nature"], # AAPS PharmSciTech
    "1869-6716": ["Springer Science + Business Media", "Oxford University Press (OUP)"], # Translational Behavioral Medicine
    "0883-6612": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Annals of Behavioral Medicine
    "1532-4796": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Annals of Behavioral Medicine (electronic)
    "0013-0095": ["Wiley-Blackwell", "Informa UK Limited"], #Economic Geography
    "2157-6564": ["Alphamed Press", "Wiley-Blackwell"], # STEM CELLS Translational Medicine
    "0002-9122": ["Botanical Society of America", "Wiley-Blackwell"], # American Journal of Botany
    "1537-2197": ["Botanical Society of America", "Wiley-Blackwell"], # American Journal of Botany (electronic)
    "0024-6115": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Proceedings of the London Mathematical Society
    "0160-5682": ["Nature Publishing Group", "Springer Nature", "Informa UK Limited"], # Journal of the Operational Research Society
    "1476-9360": ["Nature Publishing Group", "Springer Nature", "Informa UK Limited"], # Journal of the Operational Research Society (electronic)
    "1078-0998": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"], # Inflammatory Bowel Diseases
    "1869-6716": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Translational Behavioral Medicine
    "1613-9860": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Translational Behavioral Medicine (electronic)
    "0883-8305": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Paleoceanography
    "1076-2787": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Complexity
    "2333-5084": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Earth and Space Science
    "2041-8213": ["IOP Publishing", "American Astronomical Society"], # The Astrophysical Journal
    "0024-6107": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Journal of the London Mathematical Society
    "2169-9313": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Solid Earth
    "0022-3166": ["American Society for Nutrition", "Oxford University Press (OUP)"],# Journal of Nutrition
    "1541-6100": ["American Society for Nutrition", "Oxford University Press (OUP)"], # Journal of Nutrition (electronic)
    "1651-2235": ["Co-Action Publishing", "Informa UK Limited"], # Microbial Ecology in Health & Disease
    "2575-1433": ["HAU, Journal of Ethnographic Theory", "University of Chicago Press"], # HAU: Journal of Ethnographic Theory
    "2222-1751": ["Springer Nature", "Informa UK Limited"], # Emerging Microbes & Infections
    "0013-0133": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # The Economic Journal
    "1358-3883": ["Informa UK Limited", "Springer Nature"], # Tertiary Education and Management
    "1573-1936": ["Informa UK Limited", "Springer Nature"], # Tertiary Education and Management (electronic)
    "1559-8608": ["Informa UK Limited", "Springer Nature"], # Journal of Statistical Theory and Practice
    "1559-8616": ["Informa UK Limited", "Springer Nature"], # Journal of Statistical Theory and Practice (electronic)
    "2199-8531": ["Springer Nature", "MDPI AG"], # Journal of Open Innovation: Technology, Market, and Complexity
    "1939-4551": ["Springer Nature", "Elsevier BV"], # World Allergy Organization Journal
    "1015-8987": ["S. Karger AG", "Cell Physiol Biochem Press GmbH and Co KG"], # Cellular Physiology and Biochemistry
    "1421-9778": ["S. Karger AG", "Cell Physiol Biochem Press GmbH and Co KG"], # Cellular Physiology and Biochemistry (electronic)
    "2052-4986": ["Oxford University Press (OUP)", "Wiley-Blackwell"] # Transactions of the London Mathematical Society
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
    "1445-5781", # Reproductive Medicine and Biology, Gold OA since 2017
    "2522-0144", # Research in the Mathematical Sciences, Hybrid since 2018
    "1574-7891", # Molecular Oncology, Gold OA since 2/2017
    "1749-5016", # Social Cognitive and Affective Neuroscience, Gold OA since 2017
    "0161-0457", # Scanning, Gold OA since 2017
    "2300-3235", # Bulletin of the Veterinary Institute in Puławy, Gold OA since 2016
    "1461-1457", # International Journal of Neuropsychopharmacology, Gold OA since 2015,
    "1010-4283", # Tumor Biology, Gold OA since 2017
    "2363-9555", # Research in Number Theory, Hybrid since 2018
    "2212-9790", # Maritime Studies, Hybrid since 2018
    "2041-4978", # Journal of Micropalaeontology, OA since 1/2018
    "2157-6564", # STEM CELLS Translational Medicine, OA since 2017
    "1539-1663", # Vadose Zone Journal, OA since 1/2018,
    "1997-6690", # Journal für Gynäkologische Endokrinologie/Österreich, hybrid since 4/2017 (erroneously listed in the DOAJ)
    "1023-6090", # Journal für Urologie und Urogynäkologie/Österreich, hybrid since 4/2017 (erroneously listed in the DOAJ)
    "1998-7773", # Journal für Klinische Endokrinologie und Stoffwechsel, hybrid since 4/2017 (erroneously listed in the DOAJ)
    "2412-8260" # Journal für Mineralstoffwechsel & Muskuloskelettale Erkrankungen, hybrid since 4/2017 (erroneously listed in the DOAJ)
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

UNUSED_FIELDS = ["institution", "period", "license_ref", "pmid", "pmcid", "ut"]
CORRECT_ROW_LENGTH = 18 - len(UNUSED_FIELDS)

ISSN_DICT_FIELDS = ["is_hybrid", "publisher", "journal_full_title", "issn_l"]

for file_name in ["data/apc_de.csv", "data/offsetting/offsetting.csv"]:
    with open(file_name, "r") as csv_file:
        reader = DictReader(csv_file)
        line = 2
        for row in reader:
            for field in UNUSED_FIELDS:
                del(row[field])
            test_apc = True
            if file_name == "data/offsetting/offsetting.csv":
                test_apc = False
            apc_data.append(RowObject(file_name, line, row, test_apc))
            doi_duplicate_list.append(row["doi"])
            
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
            line += 1

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
    if len(row_object.row) != CORRECT_ROW_LENGTH:
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
            for reduced_row in issn_dict[issn]:
                if reduced_row["issn_l"] != issn_l:
                    pytest.fail(msg.format("issn", issn, issn_l, reduced_row["issn_l"]))
        issn_p = row["issn_print"]
        if issn_p != "NA":
            for reduced_row in issn_p_dict[issn_p]:
                if reduced_row["issn_l"] != issn_l:
                    pytest.fail(msg.format("issn_p", issn_p, issn_l, reduced_row["issn_l"]))
        issn_e = row["issn_electronic"]
        if issn_e != "NA":
            for reduced_row in issn_e_dict[issn_e]:
                if reduced_row["issn_l"] != issn_l:
                    pytest.fail(msg.format("issn_e", issn_e, issn_l, reduced_row["issn_l"]))

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
    hybrid_status_changed = len({issn, issn_p, issn_e}.intersection(JOURNAL_HYBRID_STATUS_CHANGED)) > 0
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
            if other_hybrid != hybrid and not hybrid_status_changed:
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
            if other_hybrid != hybrid and not hybrid_status_changed:
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
            if other_hybrid != hybrid and not hybrid_status_changed:
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
