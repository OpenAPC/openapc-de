# -*- coding: UTF-8 -*-

# A whitelist for denoting publisher identity (Possible consequence of business buy outs or fusions)
# If one publisher name is stored in the left list of an entry and another in the right one,
# they will not be treated as different by the name_consistency and check_isbns tests.
PUBLISHER_IDENTITY = [
    (["Springer Science + Business Media"], ["BioMed Central", "American Vacuum Society"]),
    (["Springer Nature"], ["Nature Publishing Group", "Springer Science + Business Media"]),
    (["Wiley-Blackwell"], ["EMBO"]),
    (["SAGE Publications"], ["Pion Ltd"]),
    (["Wiley-Blackwell"], ["American Association of Physicists in Medicine (AAPM)"]),
    (["Informa UK Limited"], ["Informa Healthcare"]), # Usage very inconsistent in crossref data
    (["Mineralogical Society of America"], ["GeoScienceWorld"]),
    (["International Scientific Literature"], ["International Scientific Information, Inc."]),
    (["Georg Thieme Verlag KG"], ["Thieme Publishing Group"]),
    (["Georg Thieme Verlag KG"], ["Schattauer GmbH"]), # Schattauer bought up by Thieme (1/1/2017)
    (["Johns Hopkins University Press"], ["Project Muse"]),
    (["Informa UK Limited"], ["Dove Medical Press Ltd."]), # DMP bought up by T&F in 2017
    (["Bristol University Press"], ["The Policy Press"]), # Policy Press is an imprint of BUP
    (["Anticancer Research USA Inc."], ["International Institute of Anticancer Research"]),
    (["Brandeis University Press"], ["Dartmouth College Press"]), # BUP and DCP were both part of the University Press of New England consortium, which was dissolved in 2018
    (["Böhlau"], ["Vandenhoeck & Ruprecht"]) # Böhlau acquired by V&R in 2017 
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
    "1878-0261": ["Wiley-Blackwell", "Elsevier BV"], # Molecular Oncology (electronic)
    "0020-7292": ["Wiley-Blackwell", "Elsevier BV"], # "International Journal of Gynecology & Obstetrics"
    "1525-0016": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # Molecular Therapy
    "2000-8198": ["Co-Action Publishing", "Informa UK Limited"], # European Journal of Psychotraumatology (print)
    "2000-8066": ["Co-Action Publishing", "Informa UK Limited"], # European Journal of Psychotraumatology
    "1600-0889": ["Co-Action Publishing", "Informa UK Limited"], # Tellus B
    "0280-6509": ["Co-Action Publishing", "Informa UK Limited"], # Tellus B (linking)
    "1654-6628": ["Co-Action Publishing", "Informa UK Limited", "SNF Swedish Nutrition Foundation"], # Food & Nutrition Research (print)
    "1654-661X": ["Co-Action Publishing", "Informa UK Limited", "SNF Swedish Nutrition Foundation"], # Food & Nutrition Research (electronic)
    "0038-0261": ["Wiley-Blackwell", "SAGE Publications"], # The Sociological Review
    "2162-2531": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # "Molecular Therapy-Nucleic Acids"
    "0009-9236": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics
    "1532-6535": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics (electronic)
    "1940-0829": ["Mongabay", "SAGE Publications"], # Tropical Conservation Science, acquired by SAGE in 08/2016
    "1600-0870": ["Co-Action Publishing", "Informa UK Limited"], # Tellus A
    "0280-6495": ["Co-Action Publishing", "Informa UK Limited"], # Tellus A (linking)
    "0963-6897": ["Cognizant Electronic Publishing", "SAGE Publications"], # Cell Transplantation
    "1555-3892": ["Cognizant Electronic Publishing", "SAGE Publications"], # Cell Transplantation (electronic)
    "0021-4922": ["Japan Society of Applied Physics", "IOP Publishing"], # Japanese Journal of Applied Physics
    "1347-4065": ["Japan Society of Applied Physics", "IOP Publishing"], # Japanese Journal of Applied Physics (electronic)
    "1445-5781": ["Springer Science + Business Media", "Wiley-Blackwell"], # Reproductive Medicine and Biology
    "1538-4357": ["American Astronomical Society", "IOP Publishing"], # The Astrophysical Journal
    "2041-8205": ["American Astronomical Society", "IOP Publishing"], # The Astrophysical Journal (linking)
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
    "1096-7508": ["International Food and Agribusiness Management Association", "Wageningen Academic Publishers"], # International Food and Agribusiness Management Review (linking)
    "1076-1551": ["The Feinstein Institute for Medical Research (North Shore LIJ Research Institute)", "Springer Nature"], # Molecular Medicine
    "1555-4309": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Contrast Media & Molecular Imaging
    "2049-1115": ["HAU, Journal of Ethnographic Theory", "University of Chicago Press"], # HAU: Journal of Ethnographic Theory
    "0197-6729": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Journal of Advanced Transportation
    "0094-8276": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # "Geophysical Research Letters"
    "1944-8007": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # "Geophysical Research Letters (electronic)"
    "8755-1209": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Reviews of Geophysics
    "1944-9208": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Reviews of Geophysics (linking)
    "0161-0457": ["Wiley-Blackwell", "Hindawi Publishing Corporation"], # Scanning
    "2169-9380": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Space Physics
    "2169-9402": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Space Physics (electronic)
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
    "2157-6580": ["Alphamed Press", "Wiley-Blackwell"], # STEM CELLS Translational Medicine (electronic)
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
    "2169-9356": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Solid Earth (electronic)
    "0022-3166": ["American Society for Nutrition", "Oxford University Press (OUP)"],# Journal of Nutrition
    "1541-6100": ["American Society for Nutrition", "Oxford University Press (OUP)"], # Journal of Nutrition (electronic)
    "1651-2235": ["Co-Action Publishing", "Informa UK Limited"], # Microbial Ecology in Health & Disease
    "0891-060X": ["Co-Action Publishing", "Informa UK Limited"], # Microbial Ecology in Health & Disease (linking)
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
    "2052-4986": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Transactions of the London Mathematical Society
    "2169-9097": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research JGR / E - Planets
    "0048-6604": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Radio Science
    "1747-0218": ["Informa UK Limited", "SAGE Publications"], # (The) Quarterly Journal of Experimental Psychology
    "1747-0226": ["Informa UK Limited", "SAGE Publications"], # (The) Quarterly Journal of Experimental Psychology (electronic)
    "1461-9571": ["Informa UK Limited", "Cambridge University Press (CUP)"], # European Journal of Archaeology
    "1741-2722": ["Informa UK Limited", "Cambridge University Press (CUP)"], # European Journal of Archaeology (electronic)
    "1179-1349": ["Dove Medical Press Ltd.", "Informa UK Limited"], # Clinical Epidemiology
    "1179-1322": ["Dove Medical Press Ltd.", "Informa UK Limited"], # Cancer Management and Research
    "1178-7090": ["Dove Med,ical Press Ltd.", "Informa UK Limited"], # Journal of Pain Research
    "1179-1608": ["Dove Medical Press Ltd.", "Informa UK Limited"], #  Nature and Science of Sleep
    "1178-2021": ["Dove Medical Press Ltd.", "Informa UK Limited"], # Neuropsychiatric Disease and Treatment
    "2155-384X": ["Springer Nature", "Ovid Technologies (Wolters Kluwer Health)"], # Clinical and Translational Gastroenterology
    "0009-921X": ["Springer Science + Business Media", "Springer Nature", "Ovid Technologies (Wolters Kluwer Health)"], # Clinical Orthopaedics and Related Research®
    "1179-5549": ["Libertas Academica, Ltd.", "SAGE Publications"], # Clinical Medicine Insights: Oncology
    "0141-8955": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Journal of Inherited Metabolic Disease
    "0261-3875": ["Wiley-Blackwell", "Cambridge University Press (CUP)"], # Legal Studies
    "1748-121X": ["Wiley-Blackwell", "Cambridge University Press (CUP)"], # Legal Studies (electronic)
    "2045-824X": ["Springer Science + Business Media", "Publiverse Online S.R.L"], # Vascular Cell
    "1869-4179": ["Springer Nature", "Walter de Gruyter GmbH"], # Raumforschung und Raumordnung
    "0034-0111": ["Springer Nature", "Walter de Gruyter GmbH"], # Raumforschung und Raumordnung (linking)
    "1552-5260": ["Elsevier BV", "Wiley-Blackwell"], # Alzheimer's & Dementia
    "1807-5932": ["FapUNIFESP (SciELO)", "Fundacao Faculdade de Medicina"], # Clinics
    "1617-9625": ["Springer Science + Business Media", "Springer Nature", "E.U. European Publishing"], #  Tobacco Induced Diseases, at EP since 2018
    "1878-7649": ["Elsevier BV", "Springer Nature"], # European Geriatric Medicine
    "0032-5791": ["Oxford University Press (OUP)", "Elsevier BV"], # Poultry Science
    "2050-490X": ["Springer Science + Business Media", "EDP Sciences"], # Regenerative Medicine Research
    "1438-3896": ["Springer Nature", "Wiley-Blackwell"], # Population Ecology
    "1438-390X": ["Springer Nature", "Wiley-Blackwell"], # Population Ecology (electronic)
    "1440-1711": ["Nature Publishing Group", "Springer Nature", "Wiley-Blackwell"], # Immunology and Cell Biology 
    "1616-5047": ["Elsevier BV", "Springer Nature"], # Mammalian Biology
    "0892-6638": ["FASEB", "Wiley-Blackwell"], # The FASEB Journal
    "1530-6860": ["FASEB", "Wiley-Blackwell"], # The FASEB Journal (electronic)
    "0935-1221": ["Schweizerbart", "Copernicus GmbH"], # European Journal of Mineralogy (linking)
    "2049-6958": ["Springer Nature", "PAGEPress Publications"], # Multidisciplinary Respiratory Medicine
    "1828-695X": ["Springer Nature", "PAGEPress Publications"], # Multidisciplinary Respiratory Medicine (linking)
    "0924-9338": ["Elsevier BV", "Royal College of Psychiatrists"], # European Psychiatry
    "1778-3585": ["Elsevier BV", "Royal College of Psychiatrists"], # European Psychiatry (electronic)
    "0090-5992": ["Informa UK Limited", "Cambridge University Press (CUP)"], # Nationalities Papers
    "1465-3923": ["Informa UK Limited", "Cambridge University Press (CUP)"], # Nationalities Papers (electronic)
    "1460-244X": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Proceedings of the London Mathematical Society
    "0860-021X": ["Index Copernicus", "Termedia Sp. z.o.o."], # Biology of Sport
    "1056-6171": ["Oxford University Press (OUP)", "Elsevier BV"], # Journal of Applied Poultry Research
    "1341-9145": ["Japanese Association of Industrial Health", "Wiley-Blackwell"], # Journal of Occupational Health
    "1348-9585": ["Japanese Association of Industrial Health", "Wiley-Blackwell"], # Journal of Occupational Health (electronic)
    "2059-7029": ["BMJ", "Elsevier BV"], # ESMO Open
    "2001-1326": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Clinical and Translational Medicine
    "2050-0068": ["Springer Nature", "Wiley-Blackwell"], # Clinical & Translational Immunology
    "1757-448X": ["IOS Press", "IMR Press"], #  Journal of Integrative Neuroscience
    "0219-6352": ["IOS Press", "IMR Press"], #  Journal of Integrative Neuroscience (linking)
    "1539-1663": ["Soil Science Society of America", "Wiley-Blackwell"], # Vadose Zone Journal
    "2352-8737": ["Elsevier BV", "Wiley-Blackwell"], # Alzheimer's & Dementia : Translational Research and Clinical Interventions
    "2414-6641": ["Universitaet Innsbruck - Innsbruck University Press", "University of Bern"], # Current Issues in Sport Science (CISS)
    "0003-021X": ["Springer Nature", "Wiley-Blackwell"], # Journal of the American Oil Chemists' Society
    "1558-9331": ["Springer Nature", "Wiley-Blackwell"], # Journal of the American Oil Chemists' Society (electronic)
    "1995-8692": ["Bern Open Publishing", "University of Bern"], # Journal of Eye Movement Research
    "2051-1426": ["Springer Nature", "BMJ"], # Journal for ImmunoTherapy of Cancer
    "1474-905X": ["Royal Society of Chemistry (RSC)", "Springer Nature"], # Photochemical & Photobiological Sciences
    "1474-9092": ["Royal Society of Chemistry (RSC)", "Springer Nature"], # Photochemical & Photobiological Sciences (electronic)
    "2245-0157": ["Aarhus University Library", "Det Kgl. Bibliotek/Royal Danish Library"], # Nordic Journal of Working Life Studies
    "0884-2914": ["Cambridge University Press (CUP)", "Springer Nature"], # Journal of Materials Research (JMR)
    "2044-5326": ["Cambridge University Press (CUP)", "Springer Nature"], # Journal of Materials Research (JMR) (electronic)
    "0884-1616": ["Cambridge University Press (CUP)", "Springer Nature"], # Journal of Materials Research (JMR) (linking)
    "0024-4201": ["Springer Nature", "Wiley-Blackwell"], # Lipids
    "1558-9307": ["Springer Nature", "Wiley-Blackwell"], # Lipids (electronic)
    "0021-9258": ["American Society for Biochemistry & Molecular Biology (ASBMB)", "Elsevier BV"], # Journal of Biological Chemistry
    "2160-1836": ["Genetics Society of America", "Oxford University Press (OUP)"], # G3: Genes|Genomes|Genetics
    "1661-8564": ["Springer Nature", "Frontiers Media SA"], # International Journal of Public Health (electronic)
    "1661-8556": ["Springer Nature", "Frontiers Media SA"], # International Journal of Public Health (linking)
    "2474-9842": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # BJS Open
    "1573-2665": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Journal of Inherited Metabolic Disease
    "2352-8729": ["Elsevier BV", "Wiley-Blackwell"], # Alzheimer's & Dementia: Diagnosis, Assessment & Disease Monitoring
    "1617-4011": ["Schweizerbart", "Copernicus GmbH"], # European Journal of Mineralogy 
    "0935-1221": ["Schweizerbart", "Copernicus GmbH"] # European Journal of Mineralogy (linking)
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
    "2412-8260", # Journal für Mineralstoffwechsel & Muskuloskelettale Erkrankungen, hybrid since 4/2017 (erroneously listed in the DOAJ)
    "1553-040X", # Geosphere, Gold OA since 01/2018
    "1366-9516", # Diversity and Distributions, Gold OA since 2019
    "1438-387X", # Helgoland Marine Research, Gold OA since 2016
    "1933-6950", # Channels
    "0264-1275", # Materials & Design, Gold OA since 2019
    "1934-8630", # Biointerphases. Seems to have flipped to hybrid after moving from Springer to AVS in 2013
    "1559-4106", # Biointerphases (electronic)
    "2043-8087", # Journal of Experimental Psychopathology
    "1083-3668", # Journal of Biomedical Optics, Gold OA since 1/2019
    "0160-4120", # Environment International, Gold OA since 1/2019
    "2053-3713", # Healthcare Technology Letters, Gold OA since 2017
    "2329-423X", # Neurophotonics, Gold OA since 1/2019
    "1388-2481", # Electrochemistry Communications, Gold OA since 1/2019
    "1869-4179", # Raumforschung und Raumordnung, Gold OA since 1/2019
    "0265-6736", # International Journal of Hyperthermia, Gold OA since 1/2019
    "1755-5930", # CNS Neuroscience & Therapeutics, Gold OA since 2019,
    "1756-8692", # International Journal of Climate Change Strategies and Management, Gold OA since 2018
    "1749-5024", # Social Cognitive and Affective Neuroscience, Gold OA since 2017
    "1464-6722", # Molecular Plant Pathology, GOLD OA since 2019
    "2162-3945", # Adipocyte, Gold OA since 09/2018
    "2045-1393", # International Journal of Hematologic Oncology, Gold OA since 2018 (?)
    "0032-5791", # Poultry Science, Gold OA since 2020
    "0960-9776", # The Breast, Gold OA since 2020
    "1662-811X", # Journal of Innate Immunity, Gold OA since 2019
    "1727-9232", # Corporate Ownership & Control, Gold OA since 2018
    "2165-5979", # Bioengineered, Gold OA since 2018 (?)
    "0287-4547", # Dental Materials Journal, Now Gold OA (2020), flipping unknown
    "1065-9471", # Human Brain Mapping, Gold OA since 2020
    "1664-2376", # Swiss Journal of Palaeontology, Gold OA since 2020
    "1661-8726", # Swiss Journal of Geosicences, Gold OA since 2020
    "2162-402X", # OncoImmunology, Gold OA since 2020
    "1053-8119", # NeuroImage, Gold OA since 2020
    "1049-8931", # International Journal of Methods in Psychiatric Research, Gold OA since 2020
    "0935-1221", # European Journal of Mineralogy, Gold OA since 2020 (moved to Copernicus)
    "0924-9338", # European Psychiatry, GOLD OA since 2020
    "1618-0240", # Engineering in Life Sciences, GOLD OA since 2020
    "1939-1404", # IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, Gold OA since 2020
    "0906-7590", # Ecography, Gold OA since 2020
    "1056-6171", # Journal of Applied Poultry Research, Gold OA since 2020
    "0005-9366", # Berliner und Münchener Tierärztliche Wochenschrift, Gold OA since July 2020
    "0950-2688", # Epidemiology and Infection, Gold OA since 2019
    "0969-9961", # Neurobiology of Disease, Gold OA since 2020
    "1753-318X", # Journal of Flood Risk Management, Gold OA since 2020
    "1949-0976", # Gut Microbes, Gold OA since 2020
    "0010-440X", # Comprehensive Psychiatry, Gold OA since 2019
    "1933-6896", # Prion, Gold OA since 2019
    "1757-448X", # Journal of Integrative Neuroscience, Gold OA since 2018,
    "0303-2434", # International Journal of Applied Earth Observation and Geoinformation, Gold OA since 2020
    "1350-4827", # Meteorological Applications, Gold OA since 2020
    "1751-8792", # IET Radar, Sonar & Navigation, Gold OA since 2021
    "1566-7367", # Catalysis Communications, Gold OA since 2021
    "0142-9418", # Polymer Testing, Gold OA since 2021
    "1025-6164", # Myrmecological News
    "1095-4244", # Wind Energy , Gold OA since 2021
    "2053-1591", # Materials Research Express, OA since 7/2020
    "1542-7390", # Space Weather
    "0021-9258", # Journal of Biological Chemistry, Gold OA since 2021
    "1661-8564", # International Journal of Public Health, Gold OA since 2021
    "1935-861X", # Brain Stimulation, Gold OA since 2020
    "1617-4011" # European Journal of Mineralogy, Gold OA since 2020
]

# A list of ISBNs which are exempt from the usual ISBN duplicate check. This is necessary for cases like
# multivolumed books where each volume has the same ISBN but is listed separately.
NON_DUPLICATE_ISBNS = [
    "978-3-205-79673-2", # Enzyklopädie der slowen. Kulturgeschichte in Kärnten, Vol 1-3
    "978-3-205-79545-2", # Erica Tietze-Conrat, Tagebücher, Vol 1 + 2,3
    "978-3-7065-5326-1" # Regesten zur Geschichte der Juden in Österreich, Vol 3-4
]


def publisher_identity(first_publisher, second_publisher):
    for entry in PUBLISHER_IDENTITY:
        if first_publisher in entry[0] and second_publisher in entry[1]:
            return True
        if first_publisher in entry[1] and second_publisher in entry[0]:
            return True
    return False

def in_whitelist(issn, first_publisher, second_publisher):
    if publisher_identity(first_publisher, second_publisher):
        return True
    if issn in JOURNAL_OWNER_CHANGED:
        return (first_publisher in JOURNAL_OWNER_CHANGED[issn] and
                second_publisher in JOURNAL_OWNER_CHANGED[issn])
    return False
