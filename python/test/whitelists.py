# -*- coding: UTF-8 -*-

# A whitelist for denoting publisher identity (Possible consequence of business buy outs or fusions)
# If one publisher name is stored in the left list of an entry and another in the right one,
# they will not be treated as different by the name_consistency and check_isbns tests.
PUBLISHER_IDENTITY = [
    (["Springer Science + Business Media"], ["BioMed Central", "American Vacuum Society"]),
    (["Springer Nature"], ["Nature Publishing Group", "Springer Science + Business Media"]),
    (["SAGE Publications"], ["Pion Ltd"]),
    (["Wiley-Blackwell"], ["American Association of Physicists in Medicine (AAPM)", "Hindawi Publishing Corporation"]),
    (["Informa UK Limited"], ["Informa Healthcare"]), # Usage very inconsistent in crossref data
    (["Mineralogical Society of America", "Geological Society of America"], ["GeoScienceWorld"]),
    (["International Scientific Literature"], ["International Scientific Information, Inc."]),
    (["Georg Thieme Verlag KG"], ["Thieme Publishing Group"]),
    (["Georg Thieme Verlag KG"], ["Schattauer GmbH"]), # Schattauer bought up by Thieme (1/1/2017)
    (["Johns Hopkins University Press"], ["Project Muse"]),
    (["Informa UK Limited"], ["Dove Medical Press Ltd."]), # DMP bought up by T&F in 2017
    (["Bristol University Press"], ["The Policy Press"]), # Policy Press is an imprint of BUP
    (["Anticancer Research USA Inc."], ["International Institute of Anticancer Research"]),
    (["Brandeis University Press"], ["Dartmouth College Press"]), # BUP and DCP were both part of the University Press of New England consortium, which was dissolved in 2018
    (["Böhlau"], ["Vandenhoeck & Ruprecht"]), # Böhlau acquired by V&R in 2017 
    (["Nomos Verlagsgesellschaft mbH & Co. KG"], ["Velbrück Wissenschaft"]), # Velbrück uses the Nomos eLibrary to publish its OA books
    (["Birkhäuser"], ["De Gruyter"]), # Birkhäuser is an imprint of De Gruyter
    (["OMICS Publishing Group"], ["Hilaris"]),
    (["Optical Society of America (OSA)"], ["Optica Publishing Group"]),
    (["Wiley-Blackwell"], ["British Institute of Radiology"]),
    (["jovis Verlag"], ["De Gruyter"]), # jovis is an imprint of De Gruyter
    (["Joule Inc."], ["CMA Impact Inc."]),
    (["CRC Press"], ["Routledge"]), # both imprints of T&F, both share a website and present their portfolio together
    (["edition text + kritik"], ["De Gruyter"]),
    (["Medknow"], ["Ovid Technologies (Wolters Kluwer Health)"]), # Medknow is an imprint of Wolters Kluwer
]


# A whitelist for denoting changes in journal ownership.
JOURNAL_OWNER_CHANGED = {
    "1744-8069": ["SAGE Publications", "Springer Science + Business Media"],
    "1990-2573": ["EDP Sciences", "European Optical Society", "Springer Nature"], # Journal of the European Optical Society: Rapid Publications
    "1755-7682": ["Springer Science + Business Media", "International Medical Publisher (Fundacion de Neurociencias)"], # International Archives of Medicine
    "2000-8198": ["Co-Action Publishing", "Informa UK Limited"], # European Journal of Psychotraumatology
    "0024-4066": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Biological Journal of the Linnean Society
    "1095-8312": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Biological Journal of the Linnean Society (electronic)
    "0024-4074": ["Wiley-Blackwell", "Oxford University Press (OUP)"], #  Botanical Journal of the Linnean Society
    "1095-8339": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Biological Journal of the Linnean Society (electronic)
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
    "1600-0889": ["Co-Action Publishing", "Informa UK Limited", "Stockholm University Press"], # Tellus B
    "0280-6509": ["Co-Action Publishing", "Informa UK Limited", "Stockholm University Press"], # Tellus B (linking)
    "1654-6628": ["Co-Action Publishing", "Informa UK Limited", "SNF Swedish Nutrition Foundation"], # Food & Nutrition Research (print)
    "1654-661X": ["Co-Action Publishing", "Informa UK Limited", "SNF Swedish Nutrition Foundation"], # Food & Nutrition Research (electronic)
    "0038-0261": ["Wiley-Blackwell", "SAGE Publications"], # The Sociological Review
    "2162-2531": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # "Molecular Therapy-Nucleic Acids"
    "0009-9236": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics
    "1532-6535": ["Nature Publishing Group", "Wiley-Blackwell"], # Clinical Pharmacology & Therapeutics (electronic)
    "1940-0829": ["Mongabay", "SAGE Publications"], # Tropical Conservation Science, acquired by SAGE in 08/2016
    "1600-0870": ["Co-Action Publishing", "Informa UK Limited", "Stockholm University Press"], # Tellus A
    "0280-6495": ["Co-Action Publishing", "Informa UK Limited", "Stockholm University Press"], # Tellus A (linking)
    "0963-6897": ["Cognizant Electronic Publishing", "SAGE Publications"], # Cell Transplantation
    "1555-3892": ["Cognizant Electronic Publishing", "SAGE Publications"], # Cell Transplantation (electronic)
    "0021-4922": ["Japan Society of Applied Physics", "IOP Publishing"], # Japanese Journal of Applied Physics
    "1347-4065": ["Japan Society of Applied Physics", "IOP Publishing"], # Japanese Journal of Applied Physics (electronic)
    "1445-5781": ["Springer Science + Business Media", "Wiley-Blackwell"], # Reproductive Medicine and Biology
    "1447-0578": ["Springer Science + Business Media", "Wiley-Blackwell"], # Reproductive Medicine and Biology (electronic)
    "1538-4357": ["American Astronomical Society", "IOP Publishing"], # The Astrophysical Journal
    "2041-8205": ["American Astronomical Society", "IOP Publishing"], # The Astrophysical Journal (linking)
    "1461-4103": ["Maney Publishing", "Informa UK Limited"], # Environmental Archaeology
    "1749-6314": ["Maney Publishing", "Informa UK Limited"], # Environmental Archaeology (electronic)
    "0039-3630": ["Maney Publishing", "Informa UK Limited"], # Studies in Conservation
    "2047-0584": ["Maney Publishing", "Informa UK Limited"], # Studies in Conservation (electronic)
    "0148-396X": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"], # Neurosurgery
    "1524-4040": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"], # Neurosurgery (electronic)
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
    "1528-3658": ["The Feinstein Institute for Medical Research (North Shore LIJ Research Institute)", "Springer Nature"], # Molecular Medicine 
    "1076-1551": ["The Feinstein Institute for Medical Research (North Shore LIJ Research Institute)", "Springer Nature"], # Molecular Medicine (linking)
    "2049-1115": ["HAU, Journal of Ethnographic Theory", "University of Chicago Press"], # HAU: Journal of Ethnographic Theory
    "0094-8276": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # "Geophysical Research Letters"
    "1944-8007": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # "Geophysical Research Letters (electronic)"
    "8755-1209": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Reviews of Geophysics
    "1944-9208": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Reviews of Geophysics (linking)
    "2169-9380": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Space Physics
    "2169-9402": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Space Physics (electronic)
    "1542-7390": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Space Weather
    "2169-897X": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Atmospheres
    "2169-8996": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Atmospheres (electronic)
    "1525-2027": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Geochemistry, Geophysics, Geosystems
    "2328-4277": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Earth's Future
    "1942-2466": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Advances in Modeling Earth Systems
    "0043-1397": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Water Resources Research
    "1944-7973": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Water Resources Research (electronic)
    "0886-6236": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Global Biogeochemical Cycles
    "1944-9224": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Global Biogeochemical Cycles (electronic)
    "2169-9003": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Earth Surface
    "2169-9011": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Earth Surface (electronic)
    "2169-9275": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Oceans
    "2169-9291": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Oceans (electronic)
    "2572-4517": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Paleoceanography and Paleoclimatology
    "2572-4525": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Paleoceanography and Paleoclimatology (electronic)
    "0002-9165": ["American Society for Nutrition", "Oxford University Press (OUP)", "Elsevier BV"], # American Journal of Clinical Nutrition
    "1938-3207": ["American Society for Nutrition", "Oxford University Press (OUP)", "Elsevier BV"], # American Journal of Clinical Nutrition (electronic)
    "0741-5400": ["Society for Leukocyte Biology", "Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Leukocyte Biology
    "1938-3673": ["Society for Leukocyte Biology", "Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Leukocyte Biology (electronic)
    "2168-0450": ["Botanical Society of America", "Wiley-Blackwell"], # Applications in Plant Sciences
    "1010-4283": ["Springer Science + Business Media", "Springer Nature", "SAGE Publications", "IOS Press"], # Tumor Biology
    "1423-0380": ["Springer Science + Business Media", "Springer Nature", "SAGE Publications", "IOS Press"], # Tumor Biology (electronic)
    "1530-9932": ["American Association of Pharmaceutical Scientists (AAPS)", "Springer Nature"], # AAPS PharmSciTech
    "1869-6716": ["Springer Science + Business Media", "Oxford University Press (OUP)"], # Translational Behavioral Medicine
    "0883-6612": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Annals of Behavioral Medicine
    "1532-4796": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Annals of Behavioral Medicine (electronic)
    "0013-0095": ["Wiley-Blackwell", "Informa UK Limited"], #Economic Geography
    "1944-8287": ["Wiley-Blackwell", "Informa UK Limited"], #Economic Geography (electronic)
    "2157-6564": ["Alphamed Press", "Wiley-Blackwell", "Oxford University Press (OUP)"], # STEM CELLS Translational Medicine
    "2157-6580": ["Alphamed Press", "Wiley-Blackwell", "Oxford University Press (OUP)"], # STEM CELLS Translational Medicine (electronic)
    "0002-9122": ["Botanical Society of America", "Wiley-Blackwell"], # American Journal of Botany
    "1537-2197": ["Botanical Society of America", "Wiley-Blackwell"], # American Journal of Botany (electronic)
    "0024-6115": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Proceedings of the London Mathematical Society
    "0160-5682": ["Nature Publishing Group", "Springer Nature", "Informa UK Limited"], # Journal of the Operational Research Society
    "1476-9360": ["Nature Publishing Group", "Springer Nature", "Informa UK Limited"], # Journal of the Operational Research Society (electronic)
    "1078-0998": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"], # Inflammatory Bowel Diseases
    "1536-4844": ["Ovid Technologies (Wolters Kluwer Health)", "Oxford University Press (OUP)"], # Inflammatory Bowel Diseases (electronic)
    "1869-6716": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Translational Behavioral Medicine
    "1613-9860": ["Springer Science + Business Media", "Springer Nature", "Oxford University Press (OUP)"], # Translational Behavioral Medicine (electronic)
    "0883-8305": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Paleoceanography
    "2333-5084": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Earth and Space Science
    "2041-8213": ["IOP Publishing", "American Astronomical Society"], # The Astrophysical Journal
    "0024-6107": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Journal of the London Mathematical Society
    "1469-7750": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Journal of the London Mathematical Society (electronic)
    "2169-9313": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Solid Earth
    "2169-9356": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research: Solid Earth (electronic)
    "0022-3166": ["American Society for Nutrition", "Oxford University Press (OUP)", "Elsevier BV"],# Journal of Nutrition
    "1541-6100": ["American Society for Nutrition", "Oxford University Press (OUP)", "Elsevier BV"], # Journal of Nutrition (electronic)
    "1651-2235": ["Co-Action Publishing", "Informa UK Limited"], # Microbial Ecology in Health & Disease
    "0891-060X": ["Co-Action Publishing", "Informa UK Limited"], # Microbial Ecology in Health & Disease (linking)
    "2575-1433": ["HAU, Journal of Ethnographic Theory", "University of Chicago Press"], # HAU: Journal of Ethnographic Theory
    "2222-1751": ["Springer Nature", "Informa UK Limited"], # Emerging Microbes & Infections
    "0013-0133": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # The Economic Journal
    "1468-0297": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # The Economic Journal (electronic)
    "1358-3883": ["Informa UK Limited", "Springer Nature"], # Tertiary Education and Management
    "1573-1936": ["Informa UK Limited", "Springer Nature"], # Tertiary Education and Management (electronic)
    "1559-8608": ["Informa UK Limited", "Springer Nature"], # Journal of Statistical Theory and Practice
    "1559-8616": ["Informa UK Limited", "Springer Nature"], # Journal of Statistical Theory and Practice (electronic)
    "2199-8531": ["Springer Nature", "MDPI AG", "Elsevier BV"], # Journal of Open Innovation: Technology, Market, and Complexity
    "1939-4551": ["Springer Nature", "Elsevier BV"], # World Allergy Organization Journal
    "1015-8987": ["S. Karger AG", "Cell Physiol Biochem Press GmbH and Co KG"], # Cellular Physiology and Biochemistry
    "1421-9778": ["S. Karger AG", "Cell Physiol Biochem Press GmbH and Co KG"], # Cellular Physiology and Biochemistry (electronic)
    "2052-4986": ["Oxford University Press (OUP)", "Wiley-Blackwell"], # Transactions of the London Mathematical Society
    "2169-9097": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research JGR / E - Planets
    "2169-9100": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Journal of Geophysical Research JGR / E - Planets (electronic)
    "0048-6604": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Radio Science
    "1944-799X": ["Wiley-Blackwell", "American Geophysical Union (AGU)"], # Radio Science (electronic)
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
    "1528-1132": ["Springer Science + Business Media", "Springer Nature", "Ovid Technologies (Wolters Kluwer Health)"], # Clinical Orthopaedics and Related Research® (electronic)
    "1179-5549": ["Libertas Academica, Ltd.", "SAGE Publications"], # Clinical Medicine Insights: Oncology
    "0141-8955": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Journal of Inherited Metabolic Disease
    "0261-3875": ["Wiley-Blackwell", "Cambridge University Press (CUP)"], # Legal Studies
    "1748-121X": ["Wiley-Blackwell", "Cambridge University Press (CUP)"], # Legal Studies (electronic)
    "2045-824X": ["Springer Science + Business Media", "Publiverse Online S.R.L"], # Vascular Cell
    "1869-4179": ["Springer Nature", "Walter de Gruyter GmbH", "Oekom Publishers GmbH"], # Raumforschung und Raumordnung
    "0034-0111": ["Springer Nature", "Walter de Gruyter GmbH", "Oekom Publishers GmbH"], # Raumforschung und Raumordnung (linking)
    "1552-5260": ["Elsevier BV", "Wiley-Blackwell"], # Alzheimer's & Dementia
    "1552-5279": ["Elsevier BV", "Wiley-Blackwell"], # Alzheimer's & Dementia (electronic)
    "1807-5932": ["FapUNIFESP (SciELO)", "Fundacao Faculdade de Medicina", "Elsevier BV"], # Clinics
    "1617-9625": ["Springer Science + Business Media", "Springer Nature", "E.U. European Publishing"], #  Tobacco Induced Diseases, at EP since 2018
    "1878-7657": ["Elsevier BV", "Springer Nature"], # European Geriatric Medicine
    "1878-7649": ["Elsevier BV", "Springer Nature"], # European Geriatric Medicine (linking)
    "0032-5791": ["Oxford University Press (OUP)", "Elsevier BV"], # Poultry Science
    "2050-490X": ["Springer Science + Business Media", "EDP Sciences"], # Regenerative Medicine Research
    "1438-3896": ["Springer Nature", "Wiley-Blackwell"], # Population Ecology
    "1438-390X": ["Springer Nature", "Wiley-Blackwell"], # Population Ecology (electronic)
    "1440-1711": ["Nature Publishing Group", "Springer Nature", "Wiley-Blackwell"], # Immunology and Cell Biology 
    "1616-5047": ["Elsevier BV", "Springer Nature"], # Mammalian Biology
    "1618-1476": ["Elsevier BV", "Springer Nature"], # Mammalian Biology (electronic)
    "0892-6638": ["FASEB", "Wiley-Blackwell"], # The FASEB Journal
    "1530-6860": ["FASEB", "Wiley-Blackwell"], # The FASEB Journal (electronic)
    "0935-1221": ["Schweizerbart", "Copernicus GmbH"], # European Journal of Mineralogy (linking)
    "2049-6958": ["Springer Nature", "PAGEPress Publications", "Mattioli1885"], # Multidisciplinary Respiratory Medicine
    "1828-695X": ["Springer Nature", "PAGEPress Publications", "Mattioli1885"], # Multidisciplinary Respiratory Medicine (linking)
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
    "1995-8692": ["Bern Open Publishing", "University of Bern", "MDPI AG"], # Journal of Eye Movement Research
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
    "1083-351X": ["American Society for Biochemistry & Molecular Biology (ASBMB)", "Elsevier BV"], # Journal of Biological Chemistry (electronic)
    "2160-1836": ["Genetics Society of America", "Oxford University Press (OUP)"], # G3: Genes|Genomes|Genetics
    "1661-8564": ["Springer Nature", "Frontiers Media SA"], # International Journal of Public Health (electronic)
    "1661-8556": ["Springer Nature", "Frontiers Media SA"], # International Journal of Public Health (linking)
    "2474-9842": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # BJS Open
    "1573-2665": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Journal of Inherited Metabolic Disease
    "2352-8729": ["Elsevier BV", "Wiley-Blackwell"], # Alzheimer's & Dementia: Diagnosis, Assessment & Disease Monitoring
    "1617-4011": ["Schweizerbart", "Copernicus GmbH"], # European Journal of Mineralogy 
    "0935-1221": ["Schweizerbart", "Copernicus GmbH"], # European Journal of Mineralogy (linking)
    "2211-8179": ["Elsevier BV", "Ubiquity Press, Ltd."], # Global Heart
    "2211-8160": ["Elsevier BV", "Ubiquity Press, Ltd."], # Global Heart (linking)
    "1940-3372": ["Crop Science Society of America", "Wiley-Blackwell"], # The Plant Genome
    "1751-7311": ["Cambridge University Press (CUP)", "Elsevier BV"], # Animal
    "0042-4900": ["BMJ", "Wiley-Blackwell"], # Veterinary Record
    "2042-7670": ["BMJ", "Wiley-Blackwell"], # Veterinary Record (electronic)
    "2399-2050": ["BMJ", "Wiley-Blackwell"], # Veterinary Record Open
    "2052-6113": ["BMJ", "Wiley-Blackwell"], # Veterinary Record Open (electronic)
    "0022-2275": ["American Society for Biochemistry & Molecular Biology (ASBMB)", "Elsevier BV"], # The Journal of Lipid Research
    "1535-9476": ["American Society for Biochemistry & Molecular Biology (ASBMB)", "Elsevier BV"], # Molecular & Cellular Proteomics
    "1535-9484": ["American Society for Biochemistry & Molecular Biology (ASBMB)", "Elsevier BV"], # Molecular & Cellular Proteomics (electronic)
    "0950-3471": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Historical Research
    "1468-2281": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Historical Research (electronic)
    "1875-6883": ["Springer Nature", "Atlantis Press"], # International Journal of Computational Intelligence Systems
    "0032-0889": ["American Society of Plant Biologists (ASPB)", "Oxford University Press (OUP)"], # Plant Physiology
    "1532-2548": ["American Society of Plant Biologists (ASPB)", "Oxford University Press (OUP)"], # Plant Physiology (electronic)
    "1532-2807": ["Springer Nature", "Frontiers Media SA"], # Pathology and Oncology Research
    "1219-4956": ["Springer Nature", "Frontiers Media SA"], # Pathology and Oncology Research (linking)
    "1044-0305": ["Springer Science + Business Media", "Springer Nature", "American Chemical Society (ACS)"], # Journal of the American Society for Mass Spectrometry
    "1879-1123": ["Springer Science + Business Media", "Springer Nature", "American Chemical Society (ACS)"], # Journal of the American Society for Mass Spectrometry (electronic)
    "2047-4873": ["SAGE Publications", "Oxford University Press (OUP)"], # European Journal of Preventive Cardiology
    "2047-4881": ["SAGE Publications", "Oxford University Press (OUP)"], # European Journal of Preventive Cardiology (electronic)
    "0007-1323": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # British Journal of Surgery
    "1365-2168": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # British Journal of Surgery (electronic)
    "0009-9147": ["American Association for Clinical Chemistry (AACC)", "Oxford University Press (OUP)"], # Clinical Chemistry
    "1530-8561": ["American Association for Clinical Chemistry (AACC)", "Oxford University Press (OUP)"], # Clinical Chemistry (electronic)
    "1943-2631": ["Genetics Society of America", "Oxford University Press (OUP)"], # Genetics
    "0016-6731": ["Genetics Society of America", "Oxford University Press (OUP)"], # Genetics (linking)
    "1046-560X": ["Springer Nature", "Informa UK Limited"], # Journal of Science Teacher Education
    "1573-1847": ["Springer Nature", "Informa UK Limited"], # Journal of Science Teacher Education (electronic)
    "0912-3814": ["Springer Nature", "Wiley-Blackwell"], # Ecological Research
    "1440-1703": ["Springer Nature", "Wiley-Blackwell"], # Ecological Research (electronic)
    "0047-2425": ["American Society of Agronomy", "Wiley-Blackwell"], # Journal of Environmental Quality
    "1537-2537": ["American Society of Agronomy", "Wiley-Blackwell"], # Journal of Environmental Quality (electronic)
    "1751-956X": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Intelligent Transport Systems
    "1751-9578": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Intelligent Transport Systems (electronic)
    "2001-3078": ["Informa UK Limited", "Wiley-Blackwell"], # Journal of Extracellular Vesicles
    "1751-8687": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Generation, Transmission & Distribution
    "1751-8695": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Generation, Transmission & Distribution (electronic)
    "1752-1416": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Renewable Power Generation
    "1752-1424": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Renewable Power Generation (electronic)
    "1751-8784": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Radar, Sonar & Navigation
    "1751-8792": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Radar, Sonar & Navigation (electronic)
    "2051-3305": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # The Journal of Engineering
    "0013-5194": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # Electronics Letters
    "1350-911X": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # Electronics Letters (electronic)
    "2045-7022": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Clinical and Translational Allergy
    "1755-4535": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Power Electronics
    "1755-4543": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Power Electronics (electronic)
    "2590-0366": ["Springer Nature", "Brill"], # Triple Helix 
    "2197-1927": ["Springer Nature", "Brill"], # Triple Helix (electronic)
    "1718-7729": ["MultiMed Inc.", "MDPI AG"], # Current Oncology (electronic)
    "1198-0052": ["MultiMed Inc.", "MDPI AG"], # Current Oncology (linking)
    "0894-0282": ["Scientific Societies", "American Phytopathological Society"], # Molecular Plant-Microbe Interactions
    "1943-7706": ["Scientific Societies", "American Phytopathological Society"], # Molecular Plant-Microbe Interactions (electronic)
    "2379-1381": ["Grapho, LLC", "MDPI AG"], # Tomography
    "2379-139X": ["Grapho, LLC", "MDPI AG"], # Tomography (electronic)
    "2397-1835": ["Ubiquity Press, Ltd.", "Open Library of the Humanities"], # Glossa: a journal of general linguistics
    "1367-5435": ["Springer Nature", "Oxford University Press (OUP)"], # Journal of Industrial Microbiology and Biotechnology
    "1476-5535": ["Springer Nature", "Oxford University Press (OUP)"], # Journal of Industrial Microbiology and Biotechnology (electronic)
    "2192-1962": ["Springer Nature", "KIPS-CSWRG"], # Human-Centric Computing and Information Sciences
    "2523-3548": ["Springer Nature", "Wiley-Blackwell"], # Cancer Communications
    "0045-5091": ["Informa UK Limited", "Cambridge University Press (CUP)"], # Canadian Journal of Philosophy
    "1911-0820": ["Informa UK Limited", "Cambridge University Press (CUP)"], # Canadian Journal of Philosophy (electronic)
    "0391-3988": ["Wichtig Publishing, SRL", "SAGE Publications"], # The International Journal of Artificial Organs
    "1724-6040": ["Wichtig Publishing, SRL", "SAGE Publications"], # The International Journal of Artificial Organs (electronic)
    "0890-2070": ["Wiley-Blackwell", "SAGE Publications"], # European Journal of Personality
    "1099-0984": ["Wiley-Blackwell", "SAGE Publications"], # European Journal of Personality (electronic)
    "1465-3125": ["Informa UK Limited", "SAGE Publications"], # Journal of Orthodontics
    "1465-3133": ["Informa UK Limited", "SAGE Publications"], # Journal of Orthodontics (electronic)
    "2052-6121": ["BMJ", "Wiley-Blackwell"], # Veterinary Record Case Reports
    "0031-8884": ["International Phycological Society", "Informa UK Limited"], # Phycologia
    "2330-2968": ["International Phycological Society", "Informa UK Limited"], # Phycologia (electronic)
    "0923-7534": ["Oxford University Press (OUP)", "Elsevier BV"], # Annals of Oncology
    "1618-1905": ["Spanish Society for Microbiology", "Springer Nature"], # International Microbiology
    "1139-6709": ["Spanish Society for Microbiology", "Springer Nature"], # International Microbiology (linking)
    "2045-8940": ["SAGE Publications", "Wiley-Blackwell"], # Pulmonary Circulation
    "2045-8932": ["SAGE Publications", "Wiley-Blackwell"], # Pulmonary Circulation (linking)
    "2047-4938": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Biometrics
    "2047-4946": ["Institution of Engineering and Technology (IET)", "Wiley-Blackwell"], # IET Biometrics (electronic)
    "2035-8377": ["PAGEPress Publications", "MDPI AG"], # Neurology International
    "2521-3555": ["International Cardiovascular Forum Journal", "Wiley-Blackwell"], # JCSM Clinical Reports
    "1107-0625": ["Zerbinis Medical Publications", "BAKIS Productions"], # Journal of BUON (J BUON)
    "1536-0121": ["Hindawi Publishing Corporation", "SAGE Publications"], # Molecular Imaging
    "1535-3508": ["Hindawi Publishing Corporation", "SAGE Publications"], # Molecular Imaging (linking)
    "1756-591X": ["Oxford University Press (OUP)", "Royal Society of Chemistry (RSC)"], # Metallomics
    "1756-5901": ["Oxford University Press (OUP)", "Royal Society of Chemistry (RSC)"], # Metallomics (linking)
    "1745-3682": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Acta Orthopaedica
    "1745-3674": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Acta Orthopaedica (linking)
    "1432-2277": ["Wiley-Blackwell", "Frontiers Media SA"], # Transplant International
    "0934-0874": ["Wiley-Blackwell", "Frontiers Media SA"], # Transplant International (linking)
    "0022-0302": ["American Dairy Science Association", "Elsevier BV"], # Journal of Dairy Science
    "2279-9036": ["PAGEPress Publications", "SAGE Publications"], # Journal of Public Health Research
    "2295-8010": ["Agri‐Overseas", "Presses Agronomiques de Gembloux"], # Tropicultura
    "0771-3312": ["Agri‐Overseas", "Presses Agronomiques de Gembloux"], # Tropicultura (linking)
    "1863-2521": ["British Editorial Society of Bone & Joint Surgery", "SAGE Publications"], # Journal of Children's Orthopaedics
    "1863-2548": ["British Editorial Society of Bone & Joint Surgery", "SAGE Publications"], # Journal of Children's Orthopaedics (electronic)
    "1686-4360": ["Informa UK Limited", "CAD Solutions, LLC"], # Computer-Aided Design and Applications
    "2535-5449": ["Norwegian University of Science and Technology (NTNU) Library", "Cappelen Damm AS - Cappelen Damm Akademisk"], # BARN - Forskning om barn og barndom i Norden
    "0800-1669": ["Norwegian University of Science and Technology (NTNU) Library", "Cappelen Damm AS - Cappelen Damm Akademisk"], # BARN - Forskning om barn og barndom i Norden (linking)
    "1651-2081": ["Acta Dermato-Venereologica", "MJS Publishing, Medical Journals Sweden AB"], # Journal of Rehabilitation Medicine
    "1650-1977": ["Acta Dermato-Venereologica", "MJS Publishing, Medical Journals Sweden AB"], # Journal of Rehabilitation Medicine (linking)
    "1083-7159": [ "Wiley-Blackwell", "Oxford University Press (OUP)"], # The Oncologist
    "1549-490X": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # The Oncologist (electronic)
    "1178-2234": ["Libertas Academica, Ltd.", "SAGE Publications"], # Breast Cancer: Basic and Clinical Research
    "2048-8726": ["SAGE Publications", "Oxford University Press (OUP)"], # European Heart Journal. Acute Cardiovascular Care
    "2048-8734": ["SAGE Publications", "Oxford University Press (OUP)"], # European Heart Journal: Acute Cardiovascular Care (electronic)
    "0070-3370": ["Springer Nature", "Duke University Press"], # Demography
    "1533-7790": ["Springer Nature", "Duke University Press"], # Demography (electronic)
    "0236-8722": ["Walter de Gruyter GmbH", "Institute of Agrophysics Polish Academy of Sciences"], # International Agrophysics
    "2300-8725": ["Walter de Gruyter GmbH", "Institute of Agrophysics Polish Academy of Sciences"], # International Agrophysics (electronic)
    "2662-6810": ["Springer Nature", "Oxford University Press (OUP)"], # Horticulture Research 
    "2052-7276": ["Springer Nature", "Oxford University Press (OUP)"], # Horticulture Research (electronic)
    "1997-5902": ["African Journals Online (AJOL)", "Elewa Biosciences Journals"], # Journal of Applied Biosciences,
    "1868-6354": ["Ubiquity Press, Ltd.", "Open Library of the Humanities"], # Laboratory Phonology 
    "1868-6346": ["Ubiquity Press, Ltd.", "Open Library of the Humanities"], # Laboratory Phonology (linking)
    "1094-7159": ["Wiley-Blackwell", "Elsevier BV"], # Neuromodulation: Technology at the Neural Interface
    "0009-9104": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Clinical & Experimental Immunology 
    "1365-2249": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Clinical & Experimental Immunology (electronic)
    "1066-5099": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # STEM CELLS 
    "1549-4918": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # STEM CELLS (electronic)
    "0021-8529": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # The Journal of Aesthetics and Art Criticism 
    "1540-6245": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # The Journal of Aesthetics and Art Criticism (electronic)
    "0047-2778": ["Wiley-Blackwell", "Informa UK Limited"], # Journal of Small Business Management 
    "1540-627X": ["Wiley-Blackwell", "Informa UK Limited"], # Journal of Small Business Management (electronic)
    "0140-1971": ["Elsevier BV", "Wiley-Blackwell"], # Journal of Adolescence 
    "1095-9254": ["Elsevier BV", "Wiley-Blackwell"], # Journal of Adolescence (electronic)
    "1903-220X": ["Wildlife Biology", "Wiley-Blackwell"], # Wildlife Biology 
    "0909-6396": ["Wildlife Biology", "Wiley-Blackwell"], # Wildlife Biology (linking)
    "0028-1522": ["Wiley-Blackwell", "Institute of Navigation"], # NAVIGATION: Journal of the Institute of Navigation 
    "2161-4296": ["Wiley-Blackwell", "Institute of Navigation"], # NAVIGATION: Journal of the Institute of Navigation (electronic)
    "1896-0596": ["Exeley, Inc.", "Silesian University of Technology"], # Transport Problems 
    "2300-861X": ["Exeley, Inc.", "Silesian University of Technology"], # Transport Problems (electronic)
    "2472-5552": ["SAGE Publications", "Elsevier BV"], # SLAS Discovery
    "2153-3539": ["Medknow", "Elsevier BV"], # Journal of Pathology Informatics 
    "1933-0219": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # Mucosal Immunology 
    "1355-5502": ["Informa UK Limited", "Oxford University Press (OUP)"], # Journal of Victorian Culture
    "1750-0133": ["Informa UK Limited", "Oxford University Press (OUP)"], # Journal of Victorian Culture (electronic)
    "1059-7700": ["Springer Nature", "Wiley-Blackwell"], # Journal of Genetic Counseling 
    "1573-3599": ["Springer Nature", "Wiley-Blackwell"], # Journal of Genetic Counseling (electronic)
    "2152-7806": ["Medknow", "Scientific Scholar"], # Surgical Neurology International
    "1365-2672": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Applied Microbiology 
	"1364-5072": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Applied Microbiology (linking)
	"1040-4651": ["American Society of Plant Biologists (ASPB)", "Oxford University Press (OUP)"], # The Plant Cell 
	"1532-298X": ["American Society of Plant Biologists (ASPB)", "Oxford University Press (OUP)"], # The Plant Cell (electronic)
	"0011-183X": ["Crop Science Society of America", "Wiley-Blackwell"], # Crop Science 
	"1435-0653": ["Crop Science Society of America", "Wiley-Blackwell"], # Crop Science (electronic)
	"2095-9273": ["Springer Nature", "Elsevier BV"], # Science Bulletin 
	"0014-3820": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Evolution 
	"1558-5646": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Evolution (electronic)
	"0004-8038": ["American Ornithologists' Union", "Oxford University Press (OUP)"], # Ornithology 
	"2732-4613": ["American Ornithologists' Union", "Oxford University Press (OUP)"], # Ornithology (electronic)
	"0961-7671": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # International Journal of Pharmacy Practice 
	"2042-7174": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # International Journal of Pharmacy Practice (electronic)
	"0307-6938": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Clinical and Experimental Dermatology 
	"1365-2230": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Clinical and Experimental Dermatology (electronic)
	"1640-5544": ["Walter de Gruyter GmbH", "Termedia Sp. z.o.o."], # Journal of Human Kinetics 
	"1899-7562": ["Walter de Gruyter GmbH", "Termedia Sp. z.o.o."], # Journal of Human Kinetics (electronic)
	"2206-3552": ["Ivyspring International Publisher", "Copernicus GmbH"], # Journal of Bone and Joint Infection
	"0962-7286": ["Universities Federation for Animal Welfare", "Cambridge University Press (CUP)"], # Animal Welfare 
	"2054-1538": ["Universities Federation for Animal Welfare", "Cambridge University Press (CUP)"], # Animal Welfare (electronic)
	"0964-1998": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of the Royal Statistical Society Series A: Statistics in Society 
	"1467-985X": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of the Royal Statistical Society Series A: Statistics in Society (electronic)
	"1472-765X": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Letters in Applied Microbiology 
	"0266-8254": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Letters in Applied Microbiology (linking)
	"1431-9276": ["Cambridge University Press (CUP)", "Oxford University Press (OUP)"], # Microscopy and Microanalysis 
	"1435-8115": ["Cambridge University Press (CUP)", "Oxford University Press (OUP)"], # Microscopy and Microanalysis (electronic)
	"0007-0963": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # British Journal of Dermatology 
	"1365-2133": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # British Journal of Dermatology (electronic)
	"0022-3573": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Pharmacy and Pharmacology 
	"2042-7158": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Pharmacy and Pharmacology (electronic)
	"0309-8249": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Philosophy of Education 
	"1467-9752": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Philosophy of Education (electronic)
	"2241-5793": ["Springer Nature", "Aristotle University of Thessaloniki (AUTH)"], # Journal of Biological Research-Thessaloniki 
	"1790-045X": ["Springer Nature", "Aristotle University of Thessaloniki (AUTH)"], # Journal of Biological Research-Thessaloniki (linking)
	"0025-5300": ["Carl Hanser Verlag", "Walter de Gruyter GmbH"], # Materials Testing 
	"2195-8572": ["Carl Hanser Verlag", "Walter de Gruyter GmbH"], # Materials Testing (electronic)
	"2056-3744": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Evolution Letters 
	"2471-254X": ["Wiley-Blackwell", "Ovid Technologies (Wolters Kluwer Health)"], # Hepatology Communications 
	"2375-1916": ["Knowledge Enterprise Journals", "European Society of Medicine"], # Medical Research Archives 
	"2375-1924": ["Knowledge Enterprise Journals", "European Society of Medicine"], # Medical Research Archives (electronic)
	"1550-2783": ["Springer Science + Business Media", "Springer Nature", "Informa UK Limited"], # Journal of the International Society of Sports Nutrition
	"1755-0793": ["Thomas Telford Ltd.", "Emerald"], # Proceedings of the Institution of Civil Engineers - Urban Design and Planning 
	"1755-0807": ["Thomas Telford Ltd.", "Emerald"], # Proceedings of the Institution of Civil Engineers - Urban Design and Planning (electronic)
	"0309-3646": ["SAGE Publications", "Ovid Technologies (Wolters Kluwer Health)"], # Prosthetics & Orthotics International 
	"1746-1553": ["SAGE Publications", "Ovid Technologies (Wolters Kluwer Health)"], # Prosthetics & Orthotics International (electronic)
	"0270-9139": ["Wiley-Blackwell", "Ovid Technologies (Wolters Kluwer Health)"], # Hepatology
    "1527-3350": ["Wiley-Blackwell", "Ovid Technologies (Wolters Kluwer Health)"], # Hepatology (electronic)
	"1743-9191": ["Elsevier BV", "Ovid Technologies (Wolters Kluwer Health)"], # International Journal of Surgery
	"1743-9159": ["Elsevier BV", "Ovid Technologies (Wolters Kluwer Health)"], # International Journal of Surgery (linking)
	"2168-1813": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Scandinavian Journal of Urology 
	"2168-1805": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Scandinavian Journal of Urology (print)
	"2000-656X": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Journal of Plastic Surgery and Hand Surgery
	"2000-6764": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Journal of Plastic Surgery and Hand Surgery (electronic)
	"0024-1164": ["Wiley-Blackwell", "Scandinavian University Press / Universitetsforlaget AS"], # Lethaia 
	"1502-3931": ["Wiley-Blackwell", "Scandinavian University Press / Universitetsforlaget AS"], # Lethaia (electronic)
	"2516-3817": ["Elsevier", "Adjacent Digital Politics Ltd"], # Open Access Government
	"1342-078X": ["Springer Nature", "Japanese Society for Hygiene"], # Environmental Health and Preventive Medicine 
	"1347-4715": ["Springer Nature", "Japanese Society for Hygiene"], # Environmental Health and Preventive Medicine (electronic)
	"2475-2991": ["Oxford University Press (OUP)", "Elsevier BV"], # Current Developments in Nutrition
	"2161-8313": ["Oxford University Press (OUP)", "Elsevier BV"], # Advances in Nutrition
	"0023-6837": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # Laboratory Investigation 
	"1747-079X": ["Wiley-Blackwell", "Computers, Materials and Continua (Tech Science Press)"], # Congenital Heart Disease 
	"1747-0803": ["Wiley-Blackwell", "Computers, Materials and Continua (Tech Science Press)"], # Congenital Heart Disease (electronic)
	"2043-7897": ["Informa UK Limited", "Bristol University Press"], # Global Discourse 
	"2475-0379": ["Wiley-Blackwell", "Elsevier BV"], # Research and Practice in Thrombosis and Haemostasis
	"1279-7707": ["Springer Science + Business Media", "Springer Nature", "Elsevier BV"], # The Journal of nutrition, health & aging
	"2474-8706": ["Informa UK Limited", "Elsevier BV"], # Structural Heart 
	"0362-028X": ["International Association for Food Protection", "Elsevier BV"], # Journal of Food Protection 
	"1532-429X": ["Springer Science + Business Media", "Springer Nature", "Elsevier BV"], # Journal of Cardiovascular Magnetic Resonance
	"1097-6647": ["Springer Science + Business Media", "Springer Nature", "Elsevier BV"], # Journal of Cardiovascular Magnetic Resonance (linking)
	"1355-8145": ["Springer Science + Business Media", "Springer Nature", "Elsevier BV"], # Cell Stress and Chaperones
	"1071-3581": ["Springer Nature", "Elsevier BV"], # Journal of Nuclear Cardiology 
	"1538-7836": ["Wiley-Blackwell", "Elsevier BV"], # Journal of Thrombosis and Haemostasis
	"2041-7136": ["Springer Science + Business Media", "Springer Nature", "Frontiers Media SA"], # Pastoralism
    "0942-2056": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Knee Surgery, Sports Traumatology, Arthroscopy 
    "1433-7347": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Knee Surgery, Sports Traumatology, Arthroscopy (electronic)
    "2197-1153": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Journal of Experimental Orthopaedics
    "1460-2075": ["EMBO", "Springer Nature"], # The EMBO Journal 
	"0261-4189": ["EMBO", "Springer Nature"], # The EMBO Journal (linking)
	"0886-3350": ["Elsevier BV", "Ovid Technologies (Wolters Kluwer Health)"], # Journal of Cataract & Refractive Surgery 
	"1873-4502": ["Elsevier BV", "Ovid Technologies (Wolters Kluwer Health)"], # Journal of Cataract & Refractive Surgery (electronic)
	"0804-4643": ["BioScientifica", "Oxford University Press (OUP)"], # European Journal of Endocrinology 
	"1479-683X": ["BioScientifica", "Oxford University Press (OUP)"], # European Journal of Endocrinology (electronic)
	"1420-9101": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Evolutionary Biology 
	"1010-061X": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Evolutionary Biology (linking)
	"1057-2414": ["Wiley-Blackwell", "Informa UK Limited"], # International Journal of Nautical Archaeology 
	"1095-9270": ["Wiley-Blackwell", "Informa UK Limited"], # International Journal of Nautical Archaeology (electronic)
	"1757-1146": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # Journal of Foot and Ankle Research
	"1672-0229": ["Elsevier BV", "Oxford University Press (OUP)"], # Genomics, Proteomics & Bioinformatics 
	"2210-3244": ["Elsevier BV", "Oxford University Press (OUP)"], # Genomics, Proteomics & Bioinformatics (electronic) 
	"1876-2883": ["Wageningen Academic Publishers", "Brill"], # Beneficial Microbes 
	"1876-2891": ["Wageningen Academic Publishers", "Brill"], # Beneficial Microbes (electronic)
	"1098-5549": ["American Society for Microbiology", "Informa UK Limited"], # Molecular and Cellular Biology 
	"0270-7306": ["American Society for Microbiology", "Informa UK Limited"], # Molecular and Cellular Biology (linking)
	"0007-1285": ["Wiley-Blackwell", "British Institute of Radiology", "Oxford University Press (OUP)"], # British Journal of Radiology 
	"1748-880X": ["Wiley-Blackwell", "British Institute of Radiology", "Oxford University Press (OUP)"], # British Journal of Radiology (electronic)
    "1452-3981": ["ESG", "Elsevier BV"], # International Journal of Electrochemical Science
    "1369-7412": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of the Royal Statistical Society Series B: Statistical Methodology 
    "1467-9868": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of the Royal Statistical Society Series B: Statistical Methodology (electronic)
    "0035-9254": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of the Royal Statistical Society Series C: Applied Statistics 
    "1467-9876": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of the Royal Statistical Society Series C: Applied Statistics (electronic)
    "0884-0431": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Bone and Mineral Research 
    "1523-4681": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Journal of Bone and Mineral Research (electronic)
    "1746-1391": ["Informa UK Limited", "Wiley-Blackwell"], # European Journal of Sport Science 
    "1536-7290": ["Informa UK Limited", "Wiley-Blackwell"], # European Journal of Sport Science (electronic)
    "0032-5473": ["BMJ", "Oxford University Press (OUP)"], # Postgraduate Medical Journal 
	"1469-0756": ["BMJ", "Oxford University Press (OUP)"], # Postgraduate Medical Journal (electronic)
	"1473-2262": ["European Cells and Materials", "Forum Multimedia Publishing LLC"], # European Cells and Materials
	"2730-6151": ["Springer Nature", "Oxford University Press (OUP)"], # ISME Communications
	"0141-6790": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Art History 
	"1467-8365": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Art History (electronic)
	"1046-6673": ["American Society of Nephrology (ASN)", "Ovid Technologies (Wolters Kluwer Health)"], # Journal of the American Society of Nephrology 
	"1533-3450": ["American Society of Nephrology (ASN)", "Ovid Technologies (Wolters Kluwer Health)"], # Journal of the American Society of Nephrology (electronic)
	"1469-3178": ["EMBO", "Springer Nature"], # EMBO Reports 
	"1469-221X": ["EMBO", "Springer Nature"], # EMBO Reports (linking)
	"2352-4588": ["Wageningen Academic Publishers", "Brill"], # Journal of Insects as Food and Feed
	"1751-7362": ["Nature Publishing Group", "Springer Nature", "Oxford University Press (OUP)"], # The ISME Journal 
	"1751-7370": ["Nature Publishing Group", "Springer Nature", "Oxford University Press (OUP)"], # The ISME Journal (electronic) 
    "2050-1161": ["Elsevier BV", "Oxford University Press (OUP)"], # Sexual Medicine
    "0277-2116": ["Ovid Technologies (Wolters Kluwer Health)", "Wiley-Blackwell"], # Journal of Pediatric Gastroenterology and Nutrition 
	"1536-4801": ["Ovid Technologies (Wolters Kluwer Health)", "Wiley-Blackwell"], # Journal of Pediatric Gastroenterology and Nutrition (electronic)
	"1733-8387": ["Walter de Gruyter GmbH", "Silesian University of Technology"], # Geochronometria 
	"1897-1695": ["Walter de Gruyter GmbH", "Silesian University of Technology"], # Geochronometria (electronic)
	"2641-5275": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Biomaterial Investigations in Dentistry
	"1760-5393": ["CAIRN", "OpenEdition"], # Revue d'anthropologie des connaissances 
	"2424-7723": ["Whioce Publishing Pte Ltd", "AccScience Publishing"], # International Journal of Bioprinting 
	"2424-8002": ["Whioce Publishing Pte Ltd", "AccScience Publishing"], # International Journal of Bioprinting (electronic)
	"2049-0801": ["Elsevier BV", "Ovid Technologies (Wolters Kluwer Health)"], # Annals of Medicine & Surgery
	"2035-8164": ["PAGEPress Publications", "Open Medical Publishing"], # Orthopedic Reviews
	"1897-4279": ["Polskie Towarzystwo Kardiologiczne", "Via Medica"], # Kardiologia Polska 
	"0022-9032": ["Polskie Towarzystwo Kardiologiczne", "Via Medica"], # Kardiologia Polska (print)
	"0392-1921": ["SAGE Publications", "Cambridge University Press (CUP)"], # Diogenes 
	"1467-7695": ["SAGE Publications", "Cambridge University Press (CUP)"], # Diogenes (electronic)
	"1743-5889": ["Future Medicine Ltd", "Informa UK Limited"], # Nanomedicine 
	"1748-6963": ["Future Medicine Ltd", "Informa UK Limited"], # Nanomedicine (electronic)
	"1387-2877": ["IOS Press", "SAGE Publications"], # Journal of Alzheimer's Disease 
	"1875-8908": ["IOS Press", "SAGE Publications"], # Journal of Alzheimer's Disease (electronic)
	"1750-1911": ["Future Medicine Ltd", "Informa UK Limited"], # Epigenomics 
	"1750-192X": ["Future Medicine Ltd", "Informa UK Limited"], # Epigenomics (electronic)
	"1651-226X": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Acta Oncologica 
	"0284-186X": ["Informa UK Limited", "MJS Publishing, Medical Journals Sweden AB"], # Acta Oncologica (linking)
	"1651-2057": ["Acta Dermato-Venereologica", "MJS Publishing, Medical Journals Sweden AB"], # Acta Dermato Venereologica 
	"0001-5555": ["Acta Dermato-Venereologica", "MJS Publishing, Medical Journals Sweden AB"], # Acta Dermato Venereologica (print)
	"1048-891X": ["Ovid Technologies (Wolters Kluwer Health)", "BMJ"], # International Journal of Gynecological Cancer
	"0736-6205": ["Future Science, LTD", "Informa UK Limited"], # BioTechniques 
	"1940-9818": ["Future Science, LTD", "Informa UK Limited"], # BioTechniques (electronic)
	"2161-2234": ["Wiley-Blackwell", "Philosophy Documentation Center"], # Thought: A Journal of Philosophy 
	"0364-2313": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # World Journal of Surgery 
	"1432-2323": ["Springer Science + Business Media", "Springer Nature", "Wiley-Blackwell"], # World Journal of Surgery (electronic)
	"1743-6095": ["Elsevier BV", "Oxford University Press (OUP)"], # The Journal of Sexual Medicine 
	"1743-6109": ["Elsevier BV", "Oxford University Press (OUP)"], # The Journal of Sexual Medicine (electronic)
	"1556-3316": ["Springer Nature", "SAGE Publications"], # HSS Journal®: The Musculoskeletal Journal of Hospital for Special Surgery 
	"1556-3324": ["Springer Nature", "SAGE Publications"], # HSS Journal®: The Musculoskeletal Journal of Hospital for Special Surgery (electronic)
	"0195-6574": ["International Association for Energy Economics (IAEE)", "SAGE Publications"], # The Energy Journal 
	"1944-9089": ["International Association for Energy Economics (IAEE)", "SAGE Publications"], # The Energy Journal (electronic)
	"0267-0836": ["Informa UK Limited", "SAGE Publications"], # Materials Science and Technology 
	"1743-2847": ["Informa UK Limited", "SAGE Publications"], # Materials Science and Technology (electronic)
	"0278-0771": ["Society of Ethnobiology", "SAGE Publications"], # Journal of Ethnobiology 
	"2162-4496": ["Society of Ethnobiology", "SAGE Publications"], # Journal of Ethnobiology (electronic)
	"0301-9233": ["Informa UK Limited", "SAGE Publications"], # Ironmaking & Steelmaking: Processes, Products and Applications 
	"1743-2812": ["Informa UK Limited", "SAGE Publications"], # Ironmaking & Steelmaking: Processes, Products and Applications (electronic)
	"1059-1478": ["Wiley-Blackwell", "SAGE Publications"], # Production and Operations Management 
	"1937-5956": ["Wiley-Blackwell", "SAGE Publications"], # Production and Operations Management (electronic)
	"1080-6032": ["Elsevier BV", "SAGE Publications"], # Wilderness & Environmental Medicine 
	"1545-1534": ["Elsevier BV", "SAGE Publications"], # Wilderness & Environmental Medicine (electronic)
	"1362-1718": ["Informa UK Limited", "SAGE Publications"], # Science and Technology of Welding and Joining 
	"1743-2936": ["Informa UK Limited", "SAGE Publications"], # Science and Technology of Welding and Joining (electronic)
	"2042-6445": ["Informa UK Limited", "SAGE Publications"], # International Wood Products Journal 
	"2042-6453": ["Informa UK Limited", "SAGE Publications"], # International Wood Products Journal (electronic)
	"0959-3020": ["IOS Press", "SAGE Publications"], # Isokinetics and Exercise Science 
	"1878-5913": ["IOS Press", "SAGE Publications"], # Isokinetics and Exercise Science (electronic)
	"1752-7015": ["White Horse Press", "SAGE Publications"], # Environmental Values 
	"0963-2719": ["White Horse Press", "SAGE Publications"], # Environmental Values (linking)
	"1051-9815": ["IOS Press", "SAGE Publications"], # WORK: A Journal of Prevention, Assessment & Rehabilitation 
	"1875-9270": ["IOS Press", "SAGE Publications"], # WORK: A Journal of Prevention, Assessment & Rehabilitation (electronic)
	"1499-9013": ["Informa UK Limited", "SAGE Publications"], # International Journal of Forensic Mental Health 
	"1932-9903": ["Informa UK Limited", "SAGE Publications"], # International Journal of Forensic Mental Health (electronic)
	"1878-5123": ["IOS Press", "SAGE Publications"], # Journal of Berry Research 
	"1878-5093": ["IOS Press", "SAGE Publications"], # Journal of Berry Research (linking)
	"2168-8184": ["Cureus, Inc.", "Springer Nature"], # Cureus
	"0002-9270": ["Nature Publishing Group", "Springer Nature", "Ovid Technologies (Wolters Kluwer Health)"], # American Journal of Gastroenterology 
	"1572-0241": ["Nature Publishing Group", "Springer Nature", "Ovid Technologies (Wolters Kluwer Health)"], # American Journal of Gastroenterology (electronic)
	"2193-0074": ["Copernicus GmbH", "Pensoft Publishers"], # Fossil Record 
	"2193-0066": ["Copernicus GmbH", "Pensoft Publishers"], # Fossil Record (print)
	"2052-3211": ["Springer Nature", "Informa UK Limited"], # Journal of Pharmaceutical Policy and Practice 
	"1757-4684": ["EMBO", "Springer Nature"], # EMBO Molecular Medicine 
	"1757-4676": ["EMBO", "Springer Nature"], # EMBO Molecular Medicine (linking)
	"1744-4292": ["EMBO", "Springer Nature"], # Molecular Systems Biology 
	"1948-6596": ["California Digital Library (CDL)", "Pensoft Publishers"], # Frontiers of Biogeography 
	"2473-4039": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # JBMR Plus
	"2643-6515": ["American Association for the Advancement of Science (AAAS)", "Elsevier BV"], # Plant Phenomics 
	"1478-422X": ["Informa UK Limited", "SAGE Publications"], # Corrosion Engineering, Science and Technology: The International Journal of Corrosion Processes and Corrosion Control 
	"1743-2782": ["Informa UK Limited", "SAGE Publications"], # Corrosion Engineering, Science and Technology: The International Journal of Corrosion Processes and Corrosion Control (electronic)
	"2468-3574": ["Elsevier BV", "Ovid Technologies (Wolters Kluwer Health)"], # International Journal of Surgery Protocols
	"1877-7171": ["IOS Press", "SAGE Publications"], # Journal of Parkinson’s Disease 
	"1877-718X": ["IOS Press", "SAGE Publications"], # Journal of Parkinson’s Disease (electronic)
	"0938-8982": ["Wiley-Blackwell", "SAGE Publications"], # Learning Disabilities Research & Practice 
	"1540-5826": ["Wiley-Blackwell", "SAGE Publications"], # Learning Disabilities Research & Practice (electronic)
	"1472-3808": ["Informa UK Limited", "Cambridge University Press (CUP)"], # Royal Musical Association Research Chronicle 
	"2167-4027": ["Informa UK Limited", "Cambridge University Press (CUP)"], # Royal Musical Association Research Chronicle (electronic)
	"0022-1767": ["The American Association of Immunologists", "Oxford University Press (OUP)"], # The Journal of Immunology 
	"1550-6606": ["The American Association of Immunologists", "Oxford University Press (OUP)"], # The Journal of Immunology (electronic)
	"1084-5453": ["Oxford University Press (OUP)", "University of Chicago Press"], # Environmental History 
	"1930-8892": ["Oxford University Press (OUP)", "University of Chicago Press"], # Environmental History (electronic)
	"2210-4968": ["IOS Press", "SAGE Publications"], # Semantic Web 
	"1570-0844": ["IOS Press", "SAGE Publications"], # Semantic Web (print)
	"1091-255X": ["Springer Science + Business Media", "Springer Nature", "Elsevier BV"], # Journal of Gastrointestinal Surgery
	"1600-6135": ["Wiley-Blackwell", "Elsevier BV"], # American Journal of Transplantation
	"0893-3952": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # Modern Pathology
	"1098-3600": ["Nature Publishing Group", "Springer Nature", "Elsevier BV"], # Genetics in Medicine 
	"0006-341X": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Biometrics 
	"1541-0420": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Biometrics (electronic)
	"0032-3195": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Political Science Quarterly 
	"1538-165X": ["Wiley-Blackwell", "Oxford University Press (OUP)"], # Political Science Quarterly (electronic)
	"2572-9241": ["Ovid Technologies (Wolters Kluwer Health)", "Wiley-Blackwell"], # HemaSphere
	"1943-3875": ["SAGE Publications", "MDPI AG"], # Craniomaxillofacial Trauma & Reconstruction 
	"1943-3883": ["SAGE Publications", "MDPI AG"], # Craniomaxillofacial Trauma & Reconstruction (electronic) 
	"1479-6694": ["Future Medicine Ltd", "Informa UK Limited"], # Future Oncology 
	"1744-8301": ["Future Medicine Ltd", "Informa UK Limited"], # Future Oncology (electronic)
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
    "1461-1457", # International Journal of Neuropsychopharmacology, Gold OA since 2015
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
    "1569-8432", # International Journal of Applied Earth Observation and Geoinformation, Gold OA since 2020
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
    "1617-4011", # European Journal of Mineralogy, Gold OA since 2020
    "1470-160X", # Ecological Indicators, Gold OA since 2021
    "2213-7165", # Journal of Global Antimicrobial Resistance, Gold OA since 2020
    "0965-2299", # Complementary Therapies in Medicine, Gold OA since 2021
    "2211-8160", # Global Heart, Gold OA since 2020
    "1742-4801", # International Wound Journal, Gold OA since 2021
    "1537-1719", # Molecular Biology and Evolution
    "1740-8695", # Maternal & Child Nutrition
    "1880-6546", # The Journal of Physiological Sciences, Gold OA since 2020
    "2523-3963", # SN Applied Sciences, Gold OA since 2021
    "2045-7960", # Epidemiology and Psychiatric Sciences, Gold OA since 2020
    "2468-2330", # The Cell surface, Gold OA since 2019
    "1751-7311", # Animal, Gold OA since 2021
    "0894-0282", # Molecular Plant-Microbe Interactions, Gold OA since 2021
    "0001-6918", # Acta Psychologica, Gold OA since 2021
    "1463-4236", # Primary Health Care Research & Development, Gold OA since 2019
    "1479-1641", # Diabetes and Vascular Disease Research, Gold OA since 2020
    "0022-2275", # The Journal of Lipid Research, Gold OA since 2021
    "1535-9476", # Molecular & Cellular Proteomics, Gold OA since 2021
    "1759-4685", # Journal of Molecular Cell Biology, Gold OA since 2019
    "0355-3140", # Scandinavian Journal of Work, Environment & Health, Gold OA since 2021
    "1015-6305", # Brain Pathology
    "1751-8687", # IET Generation, Transmission & Distribution, Gold OA since 2021
    "1751-8725", # IET Microwaves, Antennas & Propagation, Gold OA since 2021
    "1532-2807", # Pathology and Oncology Research, Gold OA since 2021
    "1365-2060", # Annals of Medicine, Gold OA since 2021
    "1460-4582", # Health Informatics Journal, Gold OA since 2020
    "2047-2501", # Health Information Science and Systems, Hybrid OA since 2017
    "1534-4320", # IEEE Transactions on Neural Systems and Rehabilitation Engineering, Gold OA since 2021
    "1751-956X", # IET Intelligent Transport Systems, Gold OA since 2021
    "1752-1416", # IET Renewable Power Generation, Gold OA since 2021
    "1524-6175", # The Journal of Clinical Hypertension
    "1755-4535", # IET Power Electronics, Gold OA since 2021 
    "1751-8601", # IET Computers & Digital Techniques, Gold OA since 2021
    "1350-4177", # Ultrasonics Sonochemistry, Gold OA since 2021
    "0957-4530", # Journal of Materials Science: Materials in Medicine, Gold OA since 2021
    "2210-4968", # Semantic Web, Gold OA since 2020
    "2192-4406", # EURO Journal on Computational Optimization, Gold OA since 2021
    "0341-2687", # Schmalenbach Journal of Business Research, Gold OA since 2021
    "1438-4221", # International Journal of Medical Microbiology, Gold OA since 2020
    "1367-5435", # Journal of Industrial Microbiology and Biotechnology, Gold OA since 2020
    "1525-2027", # Geochemistry, Geophysics, Geosystems, Gold OA since 2022
    "0906-4710", # Acta Agriculturae Scandinavica, Section B — Soil & Plant Science, Gold OA since 2022
    "2468-2942", # Cancer Treatment and Research Communications, Gold OA since 2020
    "0001-6349", # Acta Obstetricia et Gynecologica Scandinavica, Gold OA since 2022
    "1600-0412", # Acta Obstetricia et Gynecologica Scandinavica, Gold OA since 2022 (electronic)
    "2329-9037", # Journal of Responsible Innovation, Gold OA since 2021
    "0022-0302", # Journal of Dairy Science, Gold OA since 2022
    "1942-0862", # mAbs, Gold OA since 2020
    "1139-6709", # International Microbiology, Hybrid since 2018 (?), published with Springer since 2018
    "1751-8660", # IET Electric Power Applications, Gold OA since 2021
    "2047-4938", # IET Biometrics, Gold OA since 2021
    "1699-5848", # Histology and Histopathology, Gold OA since 2021
    "1538-4047", # Cancer Biology & Therapy, Gold OA since 2022
    "0013-5194", # Electronics Letters, Gold OA since 2021
    "2352-1864", # Environmental Technology & Innovation, Gold OA since 2022
    "2192-8959", # Case Reports in Perinatal Medicine, Gold OA since 2022
    "1368-5538", # The Aging Male, Gold OA since 2021
    "0803-7051", # Blood Pressure, Gold OA since 2022
    "1559-2324", # Plant Signaling & Behavior, Gold OA since 2022
    "1600-5775", # Journal of Synchrotron Radiation, Gold OA since 2022
    "0004-637X", # The Astrophysical Journal, Gold OA since 2022
    "2041-8205", # The Astrophysical Journal Letters, Gold OA since 2022
    "1432-2277", # Transplant International, Gold OA since 2022
    "0934-0874", # Transplant International, Gold OA since 2022 (linking)
    "2164-5515", # Human Vaccines & Immunotherapeutics, Gold OA since 2022
    "2164-554X", # Human Vaccines & Immunotherapeutics, Gold OA since 2022 (electronic)
    "0888-7543", # Genomics, Gold OA since 2022
    "0023-6438", # LWT, Gold OA since 2022
    "2215-0382", # Colloid and Interface Science Communications, Gold OA since 2022
    "2376-9637", # Forest Products Journal, Gold OA since 2022
    "0015-7473", # Forest Products Journal, Gold OA since 2022 (linking)
    "0022-0302", # Journal of Dairy Science, Gold OA since 2022
    "2193-3685", # Journal of Causal Inference, Gold OA since 2020
    "2041-210X", # Methods in Ecology and Evolution, Gold OA since 2023
    "1538-4365", # The Astrophysical Journal Supplement Series, Gold OA since 2022
    "0908-8857", # Journal of Avian Biology, Gold OA since 2022
    "1368-9800", # Public Health Nutrition, Gold OA since 2022
    "0890-8575", # Natural Resource Modeling, Gold OA since 2021
    "1286-4560", # Annals of Forest Science, Gold OA since 2022
    "1686-4360", # Computer-Aided Design and Applications, Gold OA since 2019
    "2768-6701", # Frontiers in Bioscience-Landmark, Gold OA since 2021
    "2768-6698", # Frontiers in Bioscience-Landmark, Gold OA since 2021 (linking)
    "0219-6352", # Journal of Integrative Neuroscience, Gold OA since 2018
    "1083-7159", # The Oncologist, Gold OA since 2022
    "1549-490X", # The Oncologist, Gold OA since 2022 (electronic)
    "1457-4969", # Scandinavian Journal of Surgery
    "1799-7267", # Scandinavian Journal of Surgery (electronic)
    "2328-8604", # Health Systems & Reform, Gold OA since 2020
    "2328-8620", # Health Systems & Reform, Gold OA since 2020 (electronic)
    "0070-3370", # Demography, Gold OA since 2021
    "1533-7790", # Demography, Gold OA since 2021 (electronic)
    "1758-3004", # Carbon Management, Gold OA since 2022
    "1973-9087", # European Journal of Physical and Rehabilitation Medicine
    "1439-1791", # Basic and Applied Ecology, Gold OA since 2022
    "0928-0987", # European Journal of Pharmaceutical Sciences, Gold OA since 2022
    "0016-7061", # Geoderma, Gold OA since 2023
    "1385-1101", # Journal of Sea Research, Gold OA since 2022
    "2196-7350", # Advanced Materials Interfaces, Gold OA since 2023
    "0094-8276", # Geophysical Research Letters, Gold OA since 2023
    "0905-6947", # Indoor Air, Gold OA since 2023
    "1059-7794", # Human Mutation, Gold OA since 2023
    "0001-6314", # Acta Neurologica Scandinavica, Gold OA since 2023
    "1473-2130", # Journal of Cosmetic Dermatology, Gold OA since 2023
    "0303-4569", # Andrologia, Gold OA since 2023
    "0966-0429", # Journal of Nursing Management, Gold OA since 2023
    "0958-0670", # Experimental Physiology, Gold OA since 2023
    "2199-160X", # Advanced Electronic Materials, Gold OA since 2023
    "1399-543X", # Pediatric Diabetes, Gold OA since 2023
    "0032-7786", # Preslia, Gold OA since 2022
    "0169-1368", # Ore Geology Reviews, Gold OA since 2022
    "0004-6256", # The Astronomical Journal, Gold OA since 2022
    "0028-1522", # NAVIGATION: Journal of the Institute of Navigation, Gold OA since 2022
    "1567-1348", # Infection, Genetics and Evolution, Gold OA since 2022
    "1648-715X", # International Journal of Strategic Property Management, Gold OA since 2018
    "1747-423X", # Journal of Land Use Science, Gold OA since 2022
    "1548-1603", # GIScience & Remote Sensing, Gold OA since 2022
    "1744-1692", # Global Public Health, Gold OA since 2023
    "1541-2555", # COPD: Journal of Chronic Obstructive Pulmonary Disease, Gold OA since 2022
    "1098-612X", # Journal of Feline Medicine and Surgery, Gold OA since 2023
    "0361-9230", # Brain Research Bulletin, Gold OA since 2023
    "1871-6784", # New Biotechnology, Gold OA since 2022
    "2035-648X", # European Journal of Paediatric Dentistry
    "1591-996X", # European Journal of Paediatric Dentistry (linking)
    "1547-6286", # RNA Biology, Gold OA since 2022
    "1555-8584", # RNA Biology, Gold OA since 2022 (electronic)
    "0031-7144", # Die Pharmazie - An International Journal of Pharmaceutical Sciences, Gold OA since 2020
    "1438-7492", # Macromolecular Materials and Engineering, Gold OA since 2023
    "1101-1262", # The European Journal of Public Health, Gold OA since 2022
    "1751-8768", # IET Optoelectronics, Gold OA since 2021
    "2472-5552", # SLAS Discovery, Gold OA since 2022
    "1933-0219", # Mucosal Immunology, Gold OA since 2023
    "1477-8939", # Travel Medicine and Infectious Disease, Gold OA since 2023
    "1745-2759", # Virtual and Physical Prototyping, Gold OA since 2023
    "1877-959X", # Ticks and Tick-borne Diseases, Gold OA since 2023
    "0378-3774", # Agricultural Water Management, Gold OA since 2023
    "0168-1702", # Virus Research, Gold OA since 2023
    "1367-4811", # Bioinformatics, Gold OA since 2023
    "1367-4803", # Bioinformatics, Gold OA since 2023 (linking)
    "0909-752X", # Skin Research and Technology, Gold OA since 2022
    "0004-6361", # Astronomy & Astrophysics, Subscribe to Open (S2O) in 2022
    "1262-3377", # ESAIM: Control, Optimisation and Calculus of Variations, Subscribe to Open (S2O) in 2021
    "2804-7214", # ESAIM: Mathematical Modelling and Numerical Analysis, Subscribe to Open (S2O) in 2021
    "0973-5348", # Mathematical Modelling of Natural Phenomena, Subscribe to Open (S2O) in 2020
    "1262-3318", # ESAIM: Probability and Statistics, Subscribe to Open (S2O) in 2021
    "2257-7777", # Mechanics & Industry, Gold OA since 2021
    "1365-2095", # Aquaculture Nutrition, Gold OA since 2022
    "0030-6053", # Oryx, Gold OA since 2021
    "1365-2109", # Aquaculture Research, Gold OA since 2023
    "1355-557X", # Aquaculture Research, Gold OA since 2023 (linking)
    "2475-0387", # Journal of Theoretical Social Psychology, Gold OA since 2022
    "1478-6451", # International Journal of Sustainable Energy, Gold OA since 2023
    "0067-0049", # The Astrophysical Journal Supplement Series, Gold OA since 2022
    "0737-4038", # Molecular Biology and Evolution, Gold OA since 2021
    "1054-3139", # ICES Journal of Marine Science, Gold OA since 2023
    "2196-0216", # ChemElectroChem, Gold OA since 2023
    "1865-1682", # Transboundary and Emerging Diseases, Gold OA since 2023
    "1865-1674", # Transboundary and Emerging Diseases, Gold OA since 2023 (linking)
    "1876-3413", # International Health, Gold OA since 2020
    "1946-3138", # International Journal of Urban Sustainable Development, Gold OA since 2022
    "0171-9335", # European Journal of Cell Biology, Gold OA since 2021
    "0147-6513", # Ecotoxicology and Environmental Safety, Gold OA since 2021
    "1476-7058", # The Journal of Maternal-Fetal & Neonatal Medicine, Gold OA since 2023
    "0144-3615", # Journal of Obstetrics and Gynaecology, Gold OA since 2023
    "1947-5683", # Annals of GIS, Gold OA since 2019
    "0031-1820", # Parasitology, Gold OA since 2023
    "0962-7286", # Animal Welfare, Gold OA since 2023
    "2154-1248", # Small GTPases, Gold OA since 2023
    "1742-1241", # International Journal of Clinical Practice, Gold OA since 2022
    "1368-5031", # International Journal of Clinical Practice, Gold OA since 2022 (linking)
    "2372-3556", # Molecular & Cellular Oncology, Gold OA since 2022
    "1025-3890", # Stress, Gold OA since 2022
    "1544-0478", # Journal of Natural Fibers, Gold OA since 2023
    "0300-9483", # Boreas, Gold OA since 2022
    "1753-0393", # Journal of Diabetes, Gold OA since 2022
    "1755-0238", # Australian Journal of Grape and Wine Research, Gold OA since 2022
    "1524-4741", # The Breast Journal, Gold OA since 2022
    "1753-8947", # International Journal of Digital Earth, Gold OA since 2022
    "2510-2036", # Computing and Software for Big Science, Gold OA since 2023
    "2510-2044", # Computing and Software for Big Science, Gold OA since 2023 (linking)
    "1545-2263", # Structural Control and Health Monitoring, Gold OA since 2023
    "1545-2255", # Structural Control and Health Monitoring, Gold OA since 2023 (linking)
    "2688-4062", # Small Structures, Gold OA since 2023
    "1758-2229", # Environmental Microbiology Reports, Gold OA since 2023
    "1365-2524", # Health & Social Care in the Community, Gold OA since 2023
    "0966-0410", # Health & Social Care in the Community, Gold OA since 2023 (linking)
    "1083-3021", # Journal of Mammary Gland Biology and Neoplasia, Gold OA since 2023
    "1473-5903", # International Journal of Agricultural Sustainability, Gold OA since 2023
    "0168-6577", # European Journal of Population, Gold OA since 2023
    "2470-8542", # International Journal of Standardization Research, Gold OA since 2019
    "1350-0872", # Microbiology, Gold OA since 2023
    "2472-6303", # SLAS Technology, Gold OA since 2022
    "0029-5515", # Nuclear Fusion, Gold OA since 2023
    "0014-312X", # European Surgical Research, Gold OA since 2023
    "1743-9159", # International Journal of Surgery, Gold OA since 2023
    "0735-6161", # Wood and Fiber Science, Gold OA since 2022
    "2168-1813", # Scandinavian Journal of Urology, Gold OA since 2024 (Vol. 58)
    "2000-6764", # Journal of Plastic Surgery and Hand Surgery, Gold OA since 2024 (Vol. 58)
    "0024-1164", # Lethaia, Gold OA since 2022
    "1932-7005", # Journal of Tissue Engineering and Regenerative Medicine, Gold OA since 2023
    "1932-6254", # Journal of Tissue Engineering and Regenerative Medicine, Gold OA since 2023 (linking)
    "1613-9372", # European Journal of Ageing, Gold OA since 2023
    "1520-6394", # Depression and Anxiety, Gold OA since 2023
    "1091-4269", # Depression and Anxiety, Gold OA since 2023 (linking)
    "0043-1397", # Water Resources Research, Gold OA since 2024
    "1099-5129", # Europace, Gold OA since 2023
    "2691-199X", # Digital Government: Research and Practice
    "2524-7972", # Biochar, Gold OA since 2022
    "0175-7598", # Applied Microbiology and Biotechnology, Gold OA since 2024
    "1573-7462", # Artificial Intelligence Review, Gold OA since 2024
    "1359-4338", # Virtual Reality, Gold OA since 2024
    "0951-3590", # Gynecological Endocrinology, Gold OA since 2023
    "1574-6941", # FEMS Microbiology Ecology, Gold OA since 2024
    "0168-6496", # FEMS Microbiology Ecology, Gold OA since 2024 (linking)
    "1747-079X", # Congenital Heart Disease, Gold OA since 2020
    "1752-6981", # The Clinical Respiratory Journal, Gold OA since 2022
    "1387-3954", # Mathematical and Computer Modelling of Dynamical Systems, Gold OA since 2021
    "1949-1034", # Nucleus, Gold OA since 2018
    "1010-6049", # Geocarto International, Gold OA since 2023
    "0921-2973", # Landscape Ecology, Gold OA since 2024
    "1432-1335", # Journal of Cancer Research and Clinical Oncology, Gold OA since 2024
    "1359-6535", # Antiviral Therapy, Gold OA since 2022
    "1933-6934", # Fly, Gold OA since 2022
    "1931-4361", # Journal of Wine Economics, Gold OA since 2023
    "2212-9820", # Journal of CO2 Utilization, Gold OA since 2023
    "1279-7707", # The Journal of nutrition, health & aging, Gold OA since 2024
    "1574-9541", # Ecological Informatics, Gold OA since 2024
    "2474-8706", # Structural Heart, Gold OA since 2022
    "2161-8313", # Advances in Nutrition, Gold OA since 2023
    "0362-028X", # Journal of Food Protection, Gold OA since 2023
    "1355-8145", # Cell Stress and Chaperones, Gold OA since 2024
    "1745-4549", # Journal of Food Processing and Preservation, Gold OA since 2023
    "1868-503X", # Biomolecular Concepts, Gold OA since 2018
    "0953-7104", # Platelets, Gold OA since 2023
    "1933-6918", # Cell Adhesion & Migration, Gold OA since 2019
    "1355-6215", # Addiction Biology, Gold OA since 2024
    "1351-5101", # European Journal of Neurology, Gold OA since 2024
    "1552-5260", # Alzheimer's & Dementia, Gold OA since 2024
    "1460-2075", # The EMBO Journal, Gold OA since 2024
    "0261-4189", # The EMBO Journal, Gold OA since 2024 (linking)
    "0531-5565", # Experimental Gerontology, Gold OA since 2023
    "2363-8419", # Geomechanics and Geophysics for Geo-Energy and Geo-Resources, Gold OA since 2023
    "1874-785X", # Vocations and Learning, Gold OA since 2023
    "2578-1863", # Human Behavior and Emerging Technologies, Gold OA since 2022
    "1439-0426", # Journal of Applied Ichthyology, Gold OA since 2023
    "1476-0584", # Expert Review of Vaccines, Gold OA since 2023
    "1553-4510", # Social Influence, Gold OA since 2021
    "1043-6618", # Pharmacological Research, Gold OA since 2023
    "0035-8711", # Monthly Notices of the Royal Astronomical Society, Gold OA since 2024
    "1401-7431", # Scandinavian Cardiovascular Journal, Gold OA since 2022
    "0399-0559", # RAIRO - Operations Research, Gold OA since 2021 (S2O)
    "0988-3754", # RAIRO - Theoretical Informatics and Applications, Gold OA since 2021 (S20)
    "1746-1391", # European Journal of Sport Science, Gold OA since 2024
    "1601-1848", # Genes, Brain and Behavior, Gold OA since 2022
    "0031-5990", # Perspectives in Psychiatric Care, Gold OA since 2023
    "1420-682X", # Cellular and Molecular Life Sciences, Gold OA since 2024
    "1432-1262", # International Journal of Colorectal Disease, Gold OA since 2024
    "1471-5546", # Science and Engineering Ethics, Gold OA since 2024
    "1720-8319", # Aging Clinical and Experimental Research, Gold OA since 2024
    "2398-063X", # Behavioural Public Policy, Gold OA since 2024
    "0893-8849", # Journal of the World Aquaculture Society, Gold OA since 2022
    "0025-7273", # Medical History, Gold OA since 2023
    "0266-4623", # International Journal of Technology Assessment in Health Care, Gold OA since 2024
    "0033-2917", # Psychological Medicine, Gold OA since 2025
    "2731-9121", # Communications Psychology, Gold OA since 2023
    "1559-2294", # Epigenetics, Gold OA since 2023
    "1469-3178", # EMBO Reports, Gold OA since 2024
    "1469-221X", # EMBO Reports, Gold OA since 2024 (linking)
    "1751-7362", # The ISME Journal, Gold OA since 2024
    "1099-114X", # International Journal of Energy Research, Gold OA since 2023
    "1590-1262", # Eating and Weight Disorders - Studies on Anorexia, Bulimia and Obesity, Gold OA since 2023
    "1524-0703", # Graphical Models, Gold OA since 2023
    "1871-4757", # NanoEthics, Gold OA since 2023
    "0333-1024", # Cephalalgia, Gold OA since 2023
    "0001-0782", # Communications of the ACM, Gold OA since 2024
    "1365-2354", # European Journal of Cancer Care, Gold OA since 2023
    "0961-5423", # European Journal of Cancer Care, Gold OA since 2023 (linking)
    "0891-6934", # Autoimmunity, Gold OA since 2023
    "0018-442X", # HOMO, Gold OA since 2022
    "0378-3820", # Fuel Processing Technology, Gold OA since 2024
    "2573-8348", # Cancer Reports, Gold OA since 2021
    "1591-9528", # Clinical and Experimental Medicine, Gold OA since 2024
    "1742-3600", # Episteme, Gold OA since 2024
    "1478-9515", # Palliative and Supportive Care, Gold OA since 2025
    "1396-0296", # Dermatologic Therapy, Gold OA since 2023
    "1435-9456", # Animal Cognition, Gold OA since 2024
    "1016-2291", # Pediatric Neurosurgery, Subscribe to Open (S2O) in 2023
    "0016-7568", # Geological Magazine, Gold OA since 2024
    "1471-0684", # Theory and Practice of Logic Programming, Gold OA since 2024
    "1092-8529", # CNS Spectrums, Gold OA since 2024 (Nov.)
    "0022-3778", # Journal of Plasma Physics, Gold OA since 2024 (Sept.)
    "0962-4929", # Acta Numerica, Gold OA since 2025
    "1740-0228", # Journal of Global History, Gold OA since 2024
    "2057-5637", # European Journal of International Security, Gold OA since 2025
    "0922-1565", # Leiden Journal of International Law, Gold OA since 2025
    "1816-3831", # International Review of the Red Cross, Gold OA since 2025
    "1469-3569", # Business and Politics, Gold OA since 2024 (Oct.)
    "1744-1331", # Health Economics, Policy and Law, Gold OA since 2024 (Aug.)
    "0018-246X", # The Historical Journal, Gold OA since 2024 (Aug.)
    "0954-3945", # Language Variation and Change, Gold OA since 2024 (Oct.)
    "0147-5479", # International Labor and Working-Class History, Gold OA since 2024 (June)
    "0007-1234", # British Journal of Political Science, Gold OA since 2024 (July)
    "1867-299X", # European Journal of Risk Regulation, Gold OA since 2025
    "1866-9808", # Language and Cognition, Gold OA since 2023
    "1755-7739", # European Political Science Review, Gold OA since 2023
    "2049-8470", # Political Science Research and Methods, Gold OA since 2024 (Aug.)
    "0094-8373", # Paleobiology, Gold OA since 2024 (Nov.)
    "1383-4924", # The Journal of Comparative Germanic Linguistics, Gold OA since 2023
    "1651-226X", # Acta Oncologica, Gold OA since 2024
    "0142-0615", # International Journal of Electrical Power & Energy Systems, Gold OA since 2024
    "2169-9763", # Journal of International and Comparative Social Policy, Gold OA since 2025
    "0956-7933", # Rural History, Gold OA since 2024 
    "0959-7743", # Cambridge Archaeological Journal, Gold OA since 2024 (Oct.)
    "0967-3911", # Polymers and Polymer Composites, Gold OA since 2022
    "1528-0837", # Journal of Industrial Textiles, Gold OA since 2022
    "1940-0829", # Tropical Conservation Science, Hybrid OA since 2025
    "0022-2615", # Journal of Medical Microbiology, Subscribe to Open (S2O) in Feb. 2025
    "0014-4800", # Experimental and Molecular Pathology, Gold OA since 2023
    "0956-540X", # Geophysical Journal International, Gold OA since 2024 
    "1049-9644", # Biological Control, Gold OA since 2024
    "0924-0519", # Netherlands Quarterly of Human Rights, Subscribe to Open (S2O) since 2023 
    "0954-6634", # Journal of Dermatological Treatment, Gold OA since 2023
    "1534-8687", # New Directions for Child and Adolescent Development, Gold OA since 2023
    "2365-5135", # Automotive and Engine Technology, Gold OA since 2025
    "1877-7171", # Journal of Parkinson’s Disease, Gold OA since 2023
    "0939-3889", # Zeitschrift für Medizinische Physik, Gold OA since 2022
    "0171-5216", # Journal of Cancer Research and Clinical Oncology, Gold OA since 2024
    "0340-7004", # Cancer Immunology, Immunotherapy, Gold OA since 2024
    "1467-5463", # Briefings in Bioinformatics, Gold OA since 2024
    "1103-3088", # YOUNG, Gold OA since 2023
    "1365-2710", # Journal of Clinical Pharmacy and Therapeutics, Gold OA since 2023
    "1947-6035", # Cartilage, Gold OA since 2022
    "1062-7987", # European Review, Gold OA since 2025
    "0269-8897", # Science in Context, Gold OA since 2024
    "1432-184X", # Microbial Ecology, Gold OA since 2024
    "0924-2708", # Acta Neuropsychiatrica, Gold OA since 2025
    "0269-8463", # Functional Ecology, Gold OA since 2025
    "0305-0009", # Journal of Child Language, Gold OA since 2024
    "2049-7547", # Journal of Linguistic Geography, Gold OA since 2023
    "0332-5865", # Nordic Journal of Linguistics, Gold OA since 2024
    "0814-0626", # Australian Journal of Environmental Education, Gold OA since 2023
    "0890-0604", # Artificial Intelligence for Engineering Design, Analysis and Manufacturing, Gold OA since 2025
    "1570-8268", # Web Semantics: Science, Services and Agents on the World Wide Web, Gold OA since 2024
    "1572-1000", # Photodiagnosis and Photodynamic Therapy, Gold OA since 2024
    "0098-8472", # Environmental and Experimental Botany, Gold OA since 2025
    "0163-4453", # Journal of Infection, Gold OA since 2024
    "1573-0409", # Journal of Intelligent & Robotic Systems, Gold OA since 2024
    "1573-515X", # Biogeochemistry, Gold OA since 2024
    "0942-0940", # Acta Neurochirurgica, Gold OA since 2025
    "1432-0711", # Archives of Gynecology and Obstetrics, Gold OA since 2025
    "0939-5555", # Annals of Hematology, Gold OA since 2025
    "0271-9142", # Journal of Clinical Immunology, Gold OA since 2025
    "1435-2451", # Langenbeck's Archives of Surgery, Gold OA since 2025
    "2522-0128", # Advanced Composites and Hybrid Materials, Gold OA since 2025
    "1573-2576", # Inflammation, Gold OA since 2025
    "2573-5098", # JSFA reports, Gold OA since 2025
    "0953-1513", # Learned Publishing, Gold OA since 2025
    "1877-8879", # Scandinavian Journal of Pain, Gold OA since 2024
    "0958-1596", # Critical Public Health, Gold OA since 2024
    "1103-8128", # Scandinavian Journal of Occupational Therapy, Gold OA since 2024
]

# A whitelist to identify titles which a shared by multiple journals. The list
# contains the involved linking ISSNs which are excluded from tests.
AMBIGUOUS_JOURNAL_TITLES = {
    "Journal of Public Health": ["1741-3842", "0943-1853"],  # OUP / Springer
    "Open Medicine": ["1911-2092", "2391-5463"], # Open Medicine Publications / de Gruyter
    "Medicine": ["1357-3039", "0025-7974"], # Elsevier / Ovid Technologies
    "Medicinal Chemistry": ["2161-0444", "1573-4064"], # OMICS / Bentham
    "Journal of Optics": ["0974-6900", "2040-8978"], # Springer Nature / IOP Publishing
    "Educational Studies": ["0013-1946", "0305-5698"], # Both T&F. 0013-1946 with subtitle "A Journal of the American Educational Studies Association"
    "Journal of Surgery": ["2330-0914", "2575-9760"], # Science Publishing Group / Gavin Publishers
    "Engineering": ["1947-394X", "2095-8099"], # Scientific Research Publishing / Elsevier
}

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

def is_ambiguous_title(title, issn_l, other_issn_l):
    if title in AMBIGUOUS_JOURNAL_TITLES:
        if issn_l in AMBIGUOUS_JOURNAL_TITLES[title] and other_issn_l in AMBIGUOUS_JOURNAL_TITLES[title]:
            return True
    return False

def in_whitelist(issn, first_publisher, second_publisher):
    if publisher_identity(first_publisher, second_publisher):
        return True
    if issn in JOURNAL_OWNER_CHANGED:
        return (first_publisher in JOURNAL_OWNER_CHANGED[issn] and
                second_publisher in JOURNAL_OWNER_CHANGED[issn])
    return False
