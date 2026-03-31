

## Transformative Agreements data set

OpenAPC maintains a dedicated data set comprising articles published under transformative and other publishing agreements such as the Springer Compact pilot agreements or the German DEAL agreements. Before June 2019 this collection was known as the [offsetting data set](https://github.com/OpenAPC/openapc-de/tree/master/data/offsetting).

Unlike in the main APC data set, the Transformative Agreements (TA) data set focuses on publications that are part of publishing agreements. Many of these articles do not carry article-level cost information, as costs are often covered by aggregated contract payments (e.g. publish and/or read components) rather than individual publication fees.

At the same time, publishing agreements may also include publications for which article-based charges apply (e.g. discounted APCs within such agreements). These articles are also recorded in the TA data set and may include cost information at article level where applicable. 

Contract-related metadata and aggregated cost information are recorded separately in a dedicated contracts data set (contracts.csv). Articles in the TA data set are linked to their respective contracts, allowing analyses that combine publication output with agreement-level costs without assigning aggregated contract costs directly to individual articles.

The TA data set is relevant for analyses of publishing patterns under agreements and provides insights into the distribution of publications across publishers’ portfolios, supporting discussions on differentiated pricing models and institutional publishing strategies.

Academic institutions and research funders globally are invited to contribute data on publications under publishing agreements to support a comprehensive data set that enables extensive analyses and fosters transparency in scholarly publishing.  

## Overview

This dataset contains information on 184,853 articles, published at 557 institutions under 233 different transformative agreements. The data can also be inspected as a [treemap visualisation](https://treemaps.openapc.net/apcdata/ta-euro/).

### Breakdown by agreement



|Agreement                                                 | Articles|
|:---------------------------------------------------------|--------:|
|Springer Nature (DEAL) 2020-2023                          |    30388|
|Wiley (DEAL) 2019-2023                                    |    20593|
|Springer Compact                                          |    13332|
|Elsevier (CSAL) 2020-2023                                 |    10742|
|Sage (CRKN) 2021-2023                                     |     5811|
|Elsevier (FinELib) 2021-2023                              |     4784|
|Wiley (CSAL) 2021-2024                                    |     4405|
|Springer Compact (VSNU) 2015-2016                         |     4013|
|Springer Compact (Jisc) 2019-2022                         |     3876|
|Springer Compact (Bibsam) 2019-2021                       |     3730|
|Springer Compact (CSAL) 2020-2022                         |     3583|
|Springer Compact (Bibsam) 2016-2018                       |     3382|
|Springer Compact (KEMOE/FWF) 2016-2018                    |     3339|
|EDP Sciences (Couperin) 2017-2021                         |     3330|
|Elsevier (CRUE-CSIC Alliance) 2021-2024                   |     2924|
|Springer Compact (FinELib) 2021-2023                      |     2656|
|Sage (CRKN) 2024-2026                                     |     2497|
|EDP Sciences (Couperin) 2022-2026                         |     2423|
|Wiley (IReL) 2021-2024                                    |     2332|
|Elsevier (CSAL) 2024-2028                                 |     2246|
|Wiley (FinELib) 2023-2024                                 |     2208|
|Springer Compact (VSNU) 2018-2023                         |     2042|
|Elsevier (FinELib) 2024-2025                              |     1922|
|Wiley (FinELib) 2020-2022                                 |     1640|
|Springer Nature (DEAL) 2024-2028                          |     1577|
|Springer Nature (CRUI-CARE) 2020-2024                     |     1535|
|Springer Nature (IReL) 2021-2024                          |     1425|
|Springer Nature (CSAL) 2023-2025                          |     1409|
|Springer Compact (Bibsam) 2022-2024                       |     1388|
|Elsevier (CRUI-CARE) 2023-2027                            |     1343|
|Taylor & Francis (FinELib) 2023-2024                      |     1205|
|Taylor & Francis (CSAL) 2021-2023                         |     1148|
|Wiley (CRUE-CSIC Alliance) 2022-2024                      |     1109|
|Taylor & Francis (FinELib) 2020-2022                      |     1041|
|Taylor & Francis (IReL) 2021-2023                         |     1006|
|IEEE (FinELib) 2021-2023                                  |      933|
|Wiley (KEMOE/FWF) 2018-2020                               |      928|
|Springer Nature (FinELib) 2024-2025                       |      906|
|Wiley (CRUI-CARE) 2020-2023                               |      780|
|Wiley (DEAL) 2024-2028                                    |      723|
|Wiley (IReL) 2025-2028                                    |      710|
|Sage (FinELib) 2023-2024                                  |      707|
|Elsevier (DEAL) 2023-2028                                 |      660|
|Sage (CSAL) 2023-2025                                     |      649|
|Oxford University Press (CSAL) 2023-2024                  |      642|
|Springer Nature (CRUE-CSIC Alliance) 2021-2024            |      636|
|Cambridge University Press (IReL) 2021-2025               |      622|
|Springer Compact (MPDL) 2015-2018                         |      622|
|Taylor & Francis (IReL) 2024-2026                         |      620|
|Sage (FinELib) 2020-2022                                  |      588|
|American Chemical Society (FinELib) 2021-2023             |      565|
|Sage (IReL) 2021-2023                                     |      562|
|Oxford University Press (FinELib) 2021-2023               |      559|
|American Chemical Society (IReL) 2021-2025                |      553|
|IOP Publishing (CSAL) 2022-2024                           |      550|
|Taylor & Francis (CSAL) 2024-2027                         |      550|
|Cambridge University Press (CSAL) 2021-2023               |      530|
|American Chemical Society (CRUE-CSIC Alliance) 2021-2024  |      512|
|Sage (CSAL) 2021-2022                                     |      508|
|Elsevier (KEMOE/FWF) 2021-2023                            |      498|
|American Chemical Society (KEMOE) 2020-2022               |      444|
|Taylor & Francis (KEMOE/FWF) 2017-2019                    |      439|
|Emerald (FinELib) 2021-2023                               |      435|
|IEEE (IReL) 2024-2026                                     |      432|
|Sage (IReL) 2024-2026                                     |      431|
|Springer Nature (IReL) 2025-2027                          |      426|
|Wiley (KEMOE/FWF) 2021-2023                               |      415|
|IEEE (IReL) 2021-2023                                     |      409|
|IReL PLOS Agreement                                       |      406|
|Oxford University Press (CSIC) 2020-2024                  |      403|
|Oxford University Press (IReL) 2021-2023                  |      395|
|Springer Compact (KEMOE/FWF) 2019-2021                    |      372|
|Royal Society of Chemistry (CSAL) 2021-2023               |      364|
|Wolters Kluwer Health (CSAL) 2022-2024                    |      338|
|IEEE (FinELib) 2024-2025                                  |      324|
|American Chemical Society (CSAL) 2023-2025                |      318|
|Wiley (CRUI-CARE) 2024-2027                               |      294|
|AIP Publishing (CSAL) 2022-2024                           |      287|
|Oxford University Press (IReL) 2024-2026                  |      279|
|Royal Society of Chemistry (MPDL) 2017-2018               |      246|
|Wiley (CzechELib) 2023-2026                               |      231|
|Taylor & Francis (KEMOE) 2020-2023                        |      217|
|American Chemical Society (CRUI-CARE) 2020-2023           |      207|
|Royal Society of Chemistry (CSIC) 2021-2022               |      201|
|Royal Society of Chemistry (CSIC) 2019-2020               |      200|
|Springer Nature (CzechELib) 2023-2025                     |      200|
|Oxford University Press (FinELib) 2024-2025               |      198|
|Wiley (CRUE-CSIC Alliance) 2021-2021                      |      198|
|Elsevier (QNL) 2020-2022                                  |      194|
|Springer Nature (KEMOE/FWF) 2022-2023                     |      185|
|Cambridge University Press (CSAL) 2024-2026               |      179|
|Elsevier (FinELib) 2022-2024                              |      173|
|Royal Society of Chemistry (FinELib) 2022-2023            |      171|
|Springer Nature (CRUI-CARE) 2025-2029                     |      167|
|Royal Society of Chemistry (IReL) 2022-2024               |      165|
|Emerald (IReL) 2021-2023                                  |      164|
|Nature (CSAL) 2023-2025                                   |      164|
|IEEE (CRUI-CARE) 2022-2024                                |      151|
|Royal Society of Chemistry (CSIC) 2023-2025               |      150|
|Royal Society of Chemistry (CSAL) 2024-2026               |      143|
|Emerald (FinELib) 2024                                    |      140|
|Royal Society of Chemistry (FinELib) 2024-2025            |      134|
|Royal Society of Chemistry (CSAL) 2019-2020               |      133|
|IEEE (CSAL) 2021-2024                                     |      131|
|Royal Society of Chemistry (KEMOE) 2017-2018              |      127|
|IOP Publishing (KEMOE/FWF) 2020-2022                      |      126|
|Karger (CSAL) 2020-2022                                   |      118|
|Taylor & Francis (CSIC) 2021-2023                         |      109|
|Cambridge University Press (CRUI-CARE) 2023-2025          |      105|
|Karger (CSAL) 2023-2025                                   |      105|
|IOP Publishing (IReL) 2021-2024                           |      103|
|QNL Springer Nature Agreement                             |      103|
|Emerald (IReL) 2024-2026                                  |       95|
|QNL Wiley Agreement                                       |       92|
|IOP Publishing (KEMOE/FWF) 2017-2019                      |       91|
|Walter de Gruyter (CRUI-CARE) 2020-2022                   |       91|
|Cambridge University Press (FinELib) 2024-2025            |       86|
|Wolters Kluwer Health (FinELib) 2024-2026                 |       86|
|Taylor & Francis (CzechELib) 2023-2025                    |       85|
|Cambridge University Press (CRUI-CARE) 2020-2022          |       83|
|Royal Society of Chemistry (CRUI-CARE) 2022-2024          |       82|
|Wolters Kluwer Health (FinELib) 2018-2022                 |       81|
|Royal Society of Chemistry (IReL) 2025-2028               |       79|
|Springer Nature (EISZ) 2020-2022                          |       79|
|IReL RIA Agreement                                        |       76|
|Oxford University Press (CzechELib) 2023-2025             |       73|
|Association for Computing Machinery (FinELib) 2022-2024   |       66|
|IOP Publishing (CSIC) 2023-2025                           |       66|
|Elsevier (EISZ) 2022-2022                                 |       64|
|Royal Society of Chemistry (FinELib) 2020-2021            |       60|
|American Chemical Society (CzechELib) 2023-2025           |       58|
|Royal Society of Chemistry (TIB) 2021-2023                |       58|
|Wolters Kluwer Health (CRUI-CARE) 2021-2024               |       57|
|Oxford University Press (CRUI-CARE) 2024-2026             |       56|
|Royal Society of Chemistry (TIB) 2018-2020                |       56|
|Royal Society of Chemistry (KEMOE/FWF) 2021-2024          |       55|
|Taylor & Francis (CSIC) 2024-2026                         |       55|
|Akadémiai Kiadó (EISZ) 2021-2023                          |       54|
|Austrian Consortium RSC agreement                         |       52|
|The Royal Society (IReL) 2021-2023                        |       52|
|Association for Computing Machinery (IReL) 2023-2025      |       51|
|AIP Publishing (IReL) 2020-2022                           |       50|
|IOP Publishing (CRUI-CARE) 2023-2025                      |       50|
|Royal Society of Chemistry (CzechELib) 2023-2025          |       50|
|AIP Publishing (IReL) 2023-2025                           |       49|
|Optica Publishing Group (IReL) 2022-2024                  |       49|
|QNL T&F Agreement                                         |       48|
|AIP Publishing (CSIC) 2022-2024                           |       46|
|Taylor & Francis (MPDL) 2017-2019                         |       46|
|Wolters Kluwer Health (FinELib) 2022-2024                 |       46|
|Cambridge University Press (CSIC) 2020-2022               |       45|
|Emerald (CRUI-CARE) 2020-2024                             |       45|
|Cambridge University Press (CSIC) 2023-2025               |       44|
|Cambridge University Press (CzechELib) 2023-2025          |       43|
|IOP Publishing (IReL) 2025-2027                           |       38|
|Taylor & Francis (QNL) 2019-2020                          |       37|
|BMJ Publishing (IReL) 2021-2023                           |       36|
|BMJ Publishing (IReL) 2024-2026                           |       36|
|Microbiology Society (IReL) 2024-2026                     |       36|
|Wiley (EISZ) 2022-2022                                    |       35|
|AIP Publishing (CRUI-CARE) 2023-2026                      |       34|
|Springer Nature (FinELib) 2022-2024                       |       33|
|IOP Publishing (MPDL) 2018-2020                           |       32|
|Microbiology Society (IReL) 2021-2023                     |       32|
|American Chemical Society (CRUI-CARE) 2024-2026           |       31|
|American Psychological Association (IReL) 2022-2024       |       30|
|QNL IEEE Agreement                                        |       30|
|American Physical Society (IReL) 2025-2027                |       28|
|Royal Irish Academy (IReL) 2021-2023                      |       28|
|Sage (BSB) 2021-2023                                      |       28|
|The Royal Society (IReL) 2024-2026                        |       27|
|Elsevier (IReL) 2024-2026                                 |       26|
|Brill (CSIC) 2023-2024                                    |       23|
|Emerald (KEMOE) 2017-2019                                 |       23|
|Karger (CzechELib) 2023-2027                              |       23|
|The Royal Society (CSIC) 2024-2024                        |       22|
|Optica Publishing Group (IReL) 2025-2027                  |       21|
|Royal Irish Academy (IReL) 2024-2026                      |       21|
|CUP (BSB) 2022-2024                                       |       20|
|IOP Publishing (CzechELib) 2023-2025                      |       19|
|Sage (CSIC) 2024-2025                                     |       19|
|The Royal Society (CSIC) 2023-2023                        |       19|
|CzechELib SAGE agreement                                  |       18|
|Sage (BSB) 2024-2025                                      |       17|
|Sage (KEMOE) 2019-2022                                    |       17|
|AIP Publishing (CzechELib) 2023-2025                      |       16|
|IEEE (KEMOE/FWF) 2021-2024                                |       16|
|Sage (KEMOE) 2016-2018                                    |       16|
|Walter de Gruyter (CSIC) 2023-2025                        |       16|
|Walter de Gruyter (SUB Göttingen) 2023-2024               |       16|
|Wolters Kluwer Health (CRUI-CARE) 2025-2027               |       14|
|Association for Computing Machinery (IReL) 2020-2022      |       13|
|Microbiology Society (CSIC) 2021-2023                     |       13|
|The Royal Society (CSIC) 2022-2022                        |       12|
|The Company of Biologists (CSIC) 2021-2023                |       11|
|Walter de Gruyter (CRUI-CARE) 2023-2025                   |       11|
|BMJ Publishing (CSAL) 2024-2024                           |       10|
|Royal Society of Chemistry (CRUI-CARE) 2025               |       10|
|Association for Computing Machinery (CSAL) 2022-2025      |        9|
|ACS (University of Jyväskylä) 2025-2026                   |        8|
|IReL ECS Agreement                                        |        8|
|Portland Press (CSIC) 2023-2024                           |        8|
|Taylor & Francis (ZBW) 2024-2026                          |        8|
|Nature (MPDL) 2021-2024                                   |        7|
|Hogrefe (SUB Göttingen) 2024-2026                         |        6|
|The Company of Biologists (CSIC) 2024-2026                |        6|
|The Electrochemical Society (IReL) 2022-2022              |        6|
|The Electrochemical Society (IReL) 2023-2023              |        6|
|Emerald (CRUI-CARE) 2025                                  |        5|
|Hogrefe (SUB Göttingen) 2021-2023                         |        5|
|The Company of Biologists (IReL) 2023-2025                |        5|
|Association for Computing Machinery (CRUI-CARE) 2022-2025 |        4|
|BMJ (BSB) 2023-2024                                       |        4|
|Microbiology Society (CSIC) 2024-2024                     |        4|
|Portland Press (CSIC) 2021-2022                           |        4|
|The Electrochemical Society (IReL) 2021-2021              |        4|
|American Society of Mechanical Engineers (IReL) 2025-2027 |        3|
|Association for Computing Machinery (CzechELib) 2023-2025 |        3|
|BMJ Publishing (CRUI-CARE) 2023-2024                      |        3|
|BMJ Publishing (CRUI-CARE) 2025                           |        3|
|IReL CSHL Agreement                                       |        3|
|QNL De Gruyter Agreement                                  |        3|
|QNL OVID Agreement                                        |        3|
|Taylor & Francis (KEMOE/FWF) 2014-2016                    |        3|
|Bentham Science Publishers (CSIC) 2024-2026               |        2|
|Cambridge University Press (EISZ) 2022-2022               |        2|
|Rockefeller University Press (CSIC) 2023-2024             |        2|
|The Company of Biologists (IReL) 2020-2022                |        2|
|ACS (HGF) 2023-2025                                       |        1|
|Cold Spring Harbor Laboratory Press (IReL) 2021-2021      |        1|
|Rockefeller University Press (IReL) 2022-2024             |        1|
|Walter de Gruyter (EISZ) 2022-2022                        |        1|
|Wolters Kluwer Health (EISZ) 2022-2022                    |        1|



### Breakdown by institution



|Institution                                                                                                                                        | Articles|
|:--------------------------------------------------------------------------------------------------------------------------------------------------|--------:|
|Consejo Superior de Investigaciones Cientificas (CSIC)                                                                                             |     6859|
|French institutions                                                                                                                                |     5753|
|ETH Zurich                                                                                                                                         |     5145|
|TU Muenchen                                                                                                                                        |     5041|
|University of Helsinki                                                                                                                             |     4985|
|University of Zurich                                                                                                                               |     4920|
|FWF - Austrian Science Fund                                                                                                                        |     3469|
|Muenchen LMU                                                                                                                                       |     2998|
|University of Bern                                                                                                                                 |     2947|
|University College Dublin                                                                                                                          |     2808|
|Milano U                                                                                                                                           |     2801|
|University of Geneva                                                                                                                               |     2782|
|Charité - Universitätsmedizin Berlin                                                                                                               |     2526|
|Aalto University                                                                                                                                   |     2521|
|University of Lausanne                                                                                                                             |     2487|
|Tampere University                                                                                                                                 |     2444|
|University of Basel                                                                                                                                |     2339|
|University of Turku                                                                                                                                |     2283|
|University of Oulu                                                                                                                                 |     2261|
|École Polytechnique Fédérale de Lausanne                                                                                                           |     2184|
|University of Padua                                                                                                                                |     2148|
|KIT                                                                                                                                                |     2125|
|Trinity College Dublin                                                                                                                             |     2089|
|University of Eastern Finland                                                                                                                      |     1786|
|Tuebingen U                                                                                                                                        |     1782|
|University College Cork                                                                                                                            |     1726|
|Frankfurt U                                                                                                                                        |     1716|
|Wuerzburg U                                                                                                                                        |     1690|
|Friedrich-Schiller-Universität Jena                                                                                                                |     1655|
|University of Jyväskylä                                                                                                                            |     1556|
|Bonn U                                                                                                                                             |     1495|
|Heidelberg U                                                                                                                                       |     1385|
|University of Galway                                                                                                                               |     1255|
|Goettingen U                                                                                                                                       |     1201|
|Lund University                                                                                                                                    |     1177|
|Erlangen Nuernberg U                                                                                                                               |     1173|
|Bielefeld U                                                                                                                                        |     1169|
|TU Berlin                                                                                                                                          |     1168|
|University of Toronto                                                                                                                              |     1150|
|JGU Mainz                                                                                                                                          |     1124|
|University of Limerick                                                                                                                             |     1124|
|Karolinska Institutet                                                                                                                              |     1061|
|TU Dresden                                                                                                                                         |     1054|
|HHU Düsseldorf                                                                                                                                     |     1050|
|UCL                                                                                                                                                |     1022|
|Freiburg U                                                                                                                                         |      967|
|Dublin City University                                                                                                                             |      950|
|MPG                                                                                                                                                |      946|
|University of Cambridge                                                                                                                            |      912|
|University of Oxford                                                                                                                               |      883|
|Koeln U                                                                                                                                            |      873|
|Lappeenranta-Lahti University of Technology LUT                                                                                                    |      871|
|Uppsala University                                                                                                                                 |      869|
|University of Gothenburg                                                                                                                           |      820|
|Charles University                                                                                                                                 |      819|
|Greifswald U                                                                                                                                       |      806|
|Empa - Swiss Federal Laboratories for Materials Science and Technology                                                                             |      802|
|Hohenheim U                                                                                                                                        |      802|
|Leipzig U                                                                                                                                          |      787|
|Imperial College London                                                                                                                            |      771|
|TU Darmstadt                                                                                                                                       |      768|
|DLR                                                                                                                                                |      766|
|Duisburg-Essen U                                                                                                                                   |      732|
|University of British Columbia                                                                                                                     |      729|
|Bochum U                                                                                                                                           |      686|
|Medical University of Vienna                                                                                                                       |      682|
|HU Berlin                                                                                                                                          |      664|
|Åbo Akademi University                                                                                                                             |      664|
|Giessen U                                                                                                                                          |      658|
|King's College London                                                                                                                              |      652|
|Hannover U und TIB                                                                                                                                 |      646|
|RWTH Aachen                                                                                                                                        |      640|
|University of Fribourg                                                                                                                             |      635|
|Maynooth University                                                                                                                                |      625|
|Royal College of Surgeons in Ireland                                                                                                               |      620|
|Münster U                                                                                                                                          |      611|
|PSI - Paul Scherrer Institute                                                                                                                      |      604|
|Marburg U                                                                                                                                          |      602|
|KTH Royal Institute of Technology                                                                                                                  |      590|
|University of Manchester                                                                                                                           |      585|
|Kiel U                                                                                                                                             |      572|
|Saarland U                                                                                                                                         |      567|
|Stockholm University                                                                                                                               |      559|
|University of Vienna                                                                                                                               |      548|
|University of Amsterdam                                                                                                                            |      542|
|Utrecht University                                                                                                                                 |      527|
|Kassel U                                                                                                                                           |      515|
|Qatar National Library                                                                                                                             |      510|
|Wageningen University and Research Centre                                                                                                          |      506|
|FZJ - ZB                                                                                                                                           |      502|
|University of Groningen                                                                                                                            |      501|
|University of Edinburgh                                                                                                                            |      495|
|Delft University of Technology                                                                                                                     |      484|
|Umeå University                                                                                                                                    |      475|
|Regensburg U                                                                                                                                       |      463|
|Leiden University                                                                                                                                  |      461|
|Swedish University of Agricultural Sciences                                                                                                        |      461|
|Linköping University                                                                                                                               |      459|
|Chalmers University of Technology                                                                                                                  |      458|
|Erasmus MC                                                                                                                                         |      453|
|McGill University                                                                                                                                  |      449|
|Academic Medical Center (AMC)                                                                                                                      |      447|
|Natural Resources Institute Finland                                                                                                                |      437|
|University of Innsbruck and Medical University of Innsbruck                                                                                        |      436|
|University of Alberta                                                                                                                              |      435|
|University of Vaasa                                                                                                                                |      431|
|University Medical Center Hamburg-Eppendorf                                                                                                        |      428|
|University of Leeds                                                                                                                                |      428|
|VTT Technical Research Centre of Finland Ltd                                                                                                       |      427|
|TU Braunschweig                                                                                                                                    |      426|
|VU University Amsterdam                                                                                                                            |      426|
|TU Bergakademie Freiberg                                                                                                                           |      411|
|University of Southampton                                                                                                                          |      398|
|FU Berlin                                                                                                                                          |      397|
|Radboud University Medical Center                                                                                                                  |      397|
|Dortmund TU                                                                                                                                        |      395|
|University of Sheffield                                                                                                                            |      387|
|Fraunhofer-Gesellschaft                                                                                                                            |      386|
|McMaster University                                                                                                                                |      385|
|Siegen U                                                                                                                                           |      385|
|University of Neuchatel                                                                                                                            |      384|
|Maastricht University                                                                                                                              |      382|
|University of Applied Sciences and Arts Western Switzerland                                                                                        |      382|
|TU Chemnitz                                                                                                                                        |      381|
|University of Bristol                                                                                                                              |      378|
|University of St.Gallen                                                                                                                            |      378|
|University of Nottingham                                                                                                                           |      377|
|University Medical Center Utrecht                                                                                                                  |      375|
|Western University                                                                                                                                 |      364|
|VU University Medical Center (VUmc)                                                                                                                |      363|
|Hamburg TUHH                                                                                                                                       |      360|
|Eawag - Swiss Federal Institute of Aquatic Science and Technology                                                                                  |      359|
|University of Birmingham                                                                                                                           |      355|
|WSL - Swiss Federal Institute for Forest, Snow and Landscape Research                                                                              |      353|
|ZHAW Zurich University of Applied Sciences                                                                                                         |      351|
|Hannover U                                                                                                                                         |      349|
|Technological University Dublin                                                                                                                    |      346|
|University of Calgary                                                                                                                              |      343|
|Cardiff University                                                                                                                                 |      339|
|University of Ottawa                                                                                                                               |      338|
|University of Warwick                                                                                                                              |      332|
|Agroscope                                                                                                                                          |      320|
|Konstanz U                                                                                                                                         |      316|
|Leiden University Medical Center (LUMC)                                                                                                            |      316|
|Radboud University                                                                                                                                 |      309|
|RPTU Kaiserslautern-Landau                                                                                                                         |      299|
|Stuttgart U                                                                                                                                        |      299|
|University of Twente                                                                                                                               |      297|
|Potsdam U                                                                                                                                          |      290|
|University of Liverpool                                                                                                                            |      289|
|Università della Svizzera italiana                                                                                                                 |      287|
|University of Glasgow                                                                                                                              |      285|
|Eindhoven University of Technology                                                                                                                 |      283|
|Erasmus University                                                                                                                                 |      283|
|TU Wien                                                                                                                                            |      283|
|Bayreuth U                                                                                                                                         |      279|
|University of Newcastle                                                                                                                            |      275|
|University Medical Center Groningen (UMCG)                                                                                                         |      270|
|Luleå University of Technology                                                                                                                     |      269|
|University of Exeter                                                                                                                               |      262|
|York University                                                                                                                                    |      261|
|Université de Montréal                                                                                                                             |      260|
|Rostock U                                                                                                                                          |      257|
|Medical University of Graz                                                                                                                         |      248|
|Augsburg U                                                                                                                                         |      246|
|Ulm U                                                                                                                                              |      242|
|University of Debrecen                                                                                                                             |      236|
|Dalhousie University                                                                                                                               |      233|
|Graduate Institute of International and Development Studies                                                                                        |      232|
|University of Graz                                                                                                                                 |      232|
|University of Reading                                                                                                                              |      226|
|Finnish Institute for Health and Welfare                                                                                                           |      225|
|Mannheim U                                                                                                                                         |      220|
|University of Natural Resources and Life Sciences Vienna (BOKU)                                                                                    |      219|
|Queen's University                                                                                                                                 |      218|
|Queen's University Belfast                                                                                                                         |      217|
|University of Waterloo                                                                                                                             |      215|
|Scuola Normale Superiore                                                                                                                           |      212|
|Simon Fraser University                                                                                                                            |      209|
|GFZ-Potsdam                                                                                                                                        |      208|
|Tilburg University                                                                                                                                 |      208|
|University of York                                                                                                                                 |      205|
|Graz University of Technology                                                                                                                      |      202|
|University of Manitoba                                                                                                                             |      201|
|Örebro University                                                                                                                                  |      200|
|University of Bath                                                                                                                                 |      199|
|Alfred-Wegener-Institut                                                                                                                            |      198|
|MLU Halle-Wittenberg                                                                                                                               |      196|
|TiHo Hannover                                                                                                                                      |      195|
|Bern University of Applied Sciences                                                                                                                |      194|
|Oldenburg U                                                                                                                                        |      192|
|Queen Mary, University of London                                                                                                                   |      192|
|Finnish Environment Institute                                                                                                                      |      190|
|Maastricht University Medical Center (UMC+)                                                                                                        |      189|
|University of Applied Sciences and Arts Northwestern Switzerland                                                                                   |      185|
|Wuppertal U                                                                                                                                        |      182|
|University of Durham                                                                                                                               |      175|
|Carleton University                                                                                                                                |      173|
|University of Loughborough                                                                                                                         |      173|
|HZDR                                                                                                                                               |      171|
|University Hospital of Bern                                                                                                                        |      169|
|University of St Andrews                                                                                                                           |      168|
|University of Sussex                                                                                                                               |      168|
|LSE                                                                                                                                                |      166|
|University of Applied Sciences and Arts of Southern Switzerland                                                                                    |      165|
|University of East Anglia                                                                                                                          |      164|
|Hanken School of Economics                                                                                                                         |      163|
|Johannes Kepler University Linz                                                                                                                    |      157|
|Lancaster University                                                                                                                               |      155|
|Nottingham Trent University                                                                                                                        |      154|
|Bamberg U                                                                                                                                          |      153|
|Linnaeus University                                                                                                                                |      153|
|Memorial University of Newfoundland                                                                                                                |      151|
|University of Saskatchewan                                                                                                                         |      151|
|University of Strathclyde                                                                                                                          |      151|
|Université Laval                                                                                                                                   |      151|
|University of Leicester                                                                                                                            |      146|
|Swansea University                                                                                                                                 |      142|
|University of Aberdeen                                                                                                                             |      142|
|Universität Luzern                                                                                                                                 |      142|
|Concordia University                                                                                                                               |      138|
|Toronto Metropolitan University                                                                                                                    |      137|
|University of Victoria                                                                                                                             |      135|
|UFZ                                                                                                                                                |      134|
|University of Lapland                                                                                                                              |      133|
|Paracelsus Medical University                                                                                                                      |      132|
|University of Guelph                                                                                                                               |      132|
|University of Kent                                                                                                                                 |      125|
|Brunel University                                                                                                                                  |      124|
|University of Innsbruck                                                                                                                            |      124|
|Montanuniversität Leoben                                                                                                                           |      122|
|DESY                                                                                                                                               |      121|
|Osnabrück U                                                                                                                                        |      121|
|Salzburg U                                                                                                                                         |      119|
|University of Dundee                                                                                                                               |      115|
|Teagasc                                                                                                                                            |      113|
|GEOMAR                                                                                                                                             |      109|
|Northumbria University                                                                                                                             |      109|
|University of Surrey                                                                                                                               |      107|
|Jönköping University                                                                                                                               |      102|
|Liverpool John Moores University                                                                                                                   |      102|
|Heriot-Watt University                                                                                                                             |       98|
|Fraunhofer-Gesellschaft Publishing Fund                                                                                                            |       96|
|Hochschule Luzern                                                                                                                                  |       94|
|Leibniz-IGB                                                                                                                                        |       94|
|Malmö University                                                                                                                                   |       93|
|Université de Sherbrooke                                                                                                                           |       91|
|Vienna University of Economics and Business (WU)                                                                                                   |       88|
|Royal Holloway                                                                                                                                     |       87|
|City University London                                                                                                                             |       86|
|European Organization for Nuclear Research                                                                                                         |       86|
|University of Windsor                                                                                                                              |       84|
|Helmholtz Zentrum München                                                                                                                          |       83|
|Karlstad University                                                                                                                                |       82|
|Sheffield Hallam University                                                                                                                        |       82|
|TU Ilmenau                                                                                                                                         |       81|
|University West                                                                                                                                    |       80|
|Université du Québec à Montréal                                                                                                                    |       80|
|Mary Immaculate College                                                                                                                            |       79|
|University of Portsmouth                                                                                                                           |       78|
|Trier U                                                                                                                                            |       77|
|Royal Botanic Gardens                                                                                                                              |       76|
|Cranfield University                                                                                                                               |       75|
|Mälardalen University                                                                                                                              |       74|
|Bangor University                                                                                                                                  |       72|
|University of Hull                                                                                                                                 |       72|
|University of Ulster                                                                                                                               |       72|
|Bournemouth University                                                                                                                             |       71|
|Brandenburg University of Technology Cottbus-Senftenberg                                                                                           |       69|
|Forschungsinstitut für biologischen Landbau FiBL                                                                                                   |       68|
|Geological Survey of Finland                                                                                                                       |       68|
|Mid Sweden University                                                                                                                              |       67|
|University of Stirling                                                                                                                             |       66|
|Wilfrid Laurier University                                                                                                                         |       65|
|Manchester Metropolitan University                                                                                                                 |       64|
|Aachen FH                                                                                                                                          |       63|
|Finnish Institute of Occupational Health                                                                                                           |       63|
|HAW Hamburg                                                                                                                                        |       62|
|Leuphana University of Lüneburg                                                                                                                    |       61|
|Atlantic Technological University                                                                                                                  |       60|
|TU Clausthal                                                                                                                                       |       60|
|The Open University                                                                                                                                |       60|
|University of Huddersfield                                                                                                                         |       60|
|University of Veterinary Medicine Vienna                                                                                                           |       59|
|Aston University                                                                                                                                   |       58|
|Universität der Bundeswehr München                                                                                                                 |       58|
|Brock University                                                                                                                                   |       57|
|HEC Montréal                                                                                                                                       |       57|
|University of Lincoln                                                                                                                              |       57|
|Université du Québec                                                                                                                               |       57|
|University of the West of England                                                                                                                  |       56|
|Keele University                                                                                                                                   |       54|
|University of Klagenfurt                                                                                                                           |       54|
|BTH Blekinge Institute of Technology                                                                                                               |       52|
|RISE Research Institutes of Sweden                                                                                                                 |       51|
|University of Regina                                                                                                                               |       50|
|Magdeburg U                                                                                                                                        |       48|
|St George's, University of London                                                                                                                  |       48|
|Hospital for Sick Children                                                                                                                         |       47|
|South East Technological University                                                                                                                |       47|
|MDC                                                                                                                                                |       46|
|University of Gävle                                                                                                                                |       45|
|Munster Technological University                                                                                                                   |       44|
|Natural History Museum                                                                                                                             |       44|
|Södertörns University                                                                                                                              |       44|
|IFW Dresden                                                                                                                                        |       43|
|Leeds Beckett University                                                                                                                           |       43|
|Leibniz-IPK                                                                                                                                        |       41|
|University of New Brunswick                                                                                                                        |       41|
|Catholic University of Eichstätt-Ingolstadt                                                                                                        |       40|
|Leibniz-ZMT                                                                                                                                        |       40|
|Sunnybrook Health Science Centre                                                                                                                   |       40|
|University of Salford                                                                                                                              |       40|
|Bauhaus-Universität Weimar                                                                                                                         |       39|
|Edge Hill University                                                                                                                               |       39|
|University of Bradford                                                                                                                             |       39|
|University of Greenwich                                                                                                                            |       39|
|Aberystwyth University                                                                                                                             |       38|
|International Institute for Applied Systems Analysis (IIASA)                                                                                       |       38|
|Swedish Museum of Natural History                                                                                                                  |       38|
|Swiss Ornithological Institute                                                                                                                     |       38|
|University Health Network                                                                                                                          |       38|
|Robert Gordon University                                                                                                                           |       36|
|National Land Survey of Finland                                                                                                                    |       35|
|Netherlands Institute of Ecology                                                                                                                   |       35|
|Kingston University                                                                                                                                |       34|
|Technological University of the Shannon: Midlands Midwest                                                                                          |       34|
|University of Borås                                                                                                                                |       34|
|University of Ontario Institute of Technology                                                                                                      |       34|
|GESIS                                                                                                                                              |       33|
|HS Bielefeld                                                                                                                                       |       33|
|Leibniz-IZW                                                                                                                                        |       33|
|HafenCity Universität Hamburg                                                                                                                      |       32|
|Pädagogische Hochschule Zürich                                                                                                                     |       32|
|University of Central Lancashire                                                                                                                   |       32|
|GSI                                                                                                                                                |       31|
|IST Austria                                                                                                                                        |       31|
|Leibniz-BIPS                                                                                                                                       |       31|
|Leibniz-ZALF                                                                                                                                       |       31|
|University of Liechtenstein                                                                                                                        |       31|
|University of West of Scotland                                                                                                                     |       31|
|Hertie School                                                                                                                                      |       30|
|OST University of Applied Science of Eastern Switzerland                                                                                           |       30|
|University of Skövde                                                                                                                               |       30|
|Goldsmiths                                                                                                                                         |       29|
|University of Applied Sciences Upper Austria                                                                                                       |       29|
|University of Derby                                                                                                                                |       29|
|Finnish Meteorological Institute                                                                                                                   |       28|
|Halmstad University                                                                                                                                |       28|
|Trent University                                                                                                                                   |       28|
|Kristianstad University                                                                                                                            |       27|
|Lakehead University                                                                                                                                |       27|
|Mount Royal University                                                                                                                             |       27|
|Open University of The Netherlands                                                                                                                 |       27|
|Fachhochschule Südwestfalen                                                                                                                        |       26|
|MacEwan University                                                                                                                                 |       26|
|Université du Québec à Trois-Rivières                                                                                                              |       26|
|Athabasca University                                                                                                                               |       25|
|University of Lethbridge                                                                                                                           |       25|
|University of Westminster                                                                                                                          |       25|
|Glasgow Caledonian University                                                                                                                      |       24|
|Medical University of Innsbruck                                                                                                                    |       24|
|Mount Saint Vincent University                                                                                                                     |       24|
|St. Francis Xavier University                                                                                                                      |       24|
|HS Hannover                                                                                                                                        |       23|
|Turku University of Applied Sciences                                                                                                               |       23|
|Universität Erfurt                                                                                                                                 |       23|
|Dalarna University                                                                                                                                 |       22|
|Bremen U                                                                                                                                           |       21|
|Royal Roads University                                                                                                                             |       21|
|University of Prince Edward Island                                                                                                                 |       21|
|INM - Leibniz-Institut für Neue Materialien                                                                                                        |       20|
|London South Bank University                                                                                                                       |       20|
|Stockholm School of Economics                                                                                                                      |       20|
|Cardiff Metropolitan University                                                                                                                    |       19|
|Dundalk Institute of Technology                                                                                                                    |       19|
|Hochschule Bonn-Rhein-Sieg                                                                                                                         |       19|
|Häme University of Applied Sciences                                                                                                                |       19|
|Pädagogische Hochschule Bern                                                                                                                       |       19|
|South-Eastern Finland University of Applied Sciences (Xamk)                                                                                        |       19|
|St.Gallen University of Teacher Education                                                                                                          |       19|
|Swiss Federal University for Vocational Education and Training                                                                                     |       19|
|University of Winnipeg                                                                                                                             |       19|
|Westerdijk Fungal Biodiversity Center (CBS)                                                                                                        |       19|
|Swedish Defence Research Agency                                                                                                                    |       18|
|Swedish National Road and Transport Research Institute (VTI)                                                                                       |       18|
|University of Bedfordshire                                                                                                                         |       18|
|University of Northern British Columbia                                                                                                            |       18|
|DIPF                                                                                                                                               |       17|
|Edinburgh Napier University                                                                                                                        |       17|
|Laurea University of Applied Sciences                                                                                                              |       17|
|MHB Fontane                                                                                                                                        |       17|
|Paul-Drude-Institut für Festkörperelektronik                                                                                                       |       17|
|Cape Breton University                                                                                                                             |       16|
|Danube University Krems University for Continuing Education                                                                                        |       16|
|Leibniz-IOW                                                                                                                                        |       16|
|Nipissing University                                                                                                                               |       16|
|Saint Mary's University                                                                                                                            |       16|
|University of Education Schwaebisch Gmuend                                                                                                         |       16|
|Université de Moncton                                                                                                                              |       16|
|HAWK Hildesheim/Holzminden/Göttingen                                                                                                               |       15|
|Metropolia University of Applied Sciences                                                                                                          |       15|
|TH Köln                                                                                                                                            |       15|
|ASH Berlin                                                                                                                                         |       14|
|HS RheinMain                                                                                                                                       |       14|
|Birmingham City University                                                                                                                         |       13|
|DIfE                                                                                                                                               |       13|
|Institut national de la recherche scientifique                                                                                                     |       13|
|Munich University of Applied Sciences                                                                                                              |       13|
|Université du Québec en Outaouais                                                                                                                  |       13|
|École de technologie supérieure                                                                                                                    |       13|
|GIGA                                                                                                                                               |       12|
|Haaga-Helia University of Applied Sciences                                                                                                         |       12|
|Haute École Pédagogique du Canton de Vaud                                                                                                          |       12|
|PIK-Potsdam                                                                                                                                        |       12|
|Regensburg University of Applied Sciences                                                                                                          |       12|
|Toronto Rehabilitation Institute                                                                                                                   |       12|
|Darmstadt University of Applied Sciences                                                                                                           |       11|
|FH Salzburg - University of Applied Sciences                                                                                                       |       11|
|Scotland's Rural College                                                                                                                           |       11|
|Swedish School of Sport and Health Sciences                                                                                                        |       11|
|University of Chester                                                                                                                              |       11|
|University of Education Freiburg                                                                                                                   |       11|
|University of the Highlands and Islands                                                                                                            |       11|
|Acadia University                                                                                                                                  |       10|
|Arcada University of Applied Sciences                                                                                                              |       10|
|Mount Allison University                                                                                                                           |       10|
|Polytechnique Montreal                                                                                                                             |       10|
|TH Wildau                                                                                                                                          |       10|
|Thompson Rivers University                                                                                                                         |       10|
|Toronto Western Hospital                                                                                                                           |       10|
|University of Applied Sciences of the Grisons                                                                                                      |       10|
|University of the Fraser Valley                                                                                                                    |       10|
|Université du Québec en Abitibi-Témiscamingue                                                                                                      |       10|
|Université du Québec à Chicoutimi                                                                                                                  |       10|
|Brandon University                                                                                                                                 |        9|
|Dublin Institute for Advanced Studies                                                                                                              |        9|
|HS Düsseldorf                                                                                                                                      |        9|
|Laurentian University                                                                                                                              |        9|
|Social Insurance Institution of Finland                                                                                                            |        9|
|TH Ingolstadt                                                                                                                                      |        9|
|Université du Québec à Rimouski                                                                                                                    |        9|
|VATT Institute for Economic Research                                                                                                               |        9|
|Finnish Food Authority                                                                                                                             |        8|
|HS Reutlingen                                                                                                                                      |        8|
|Leibniz-IDS                                                                                                                                        |        8|
|Leibniz-IÖR                                                                                                                                        |        8|
|Museum für Naturkunde Berlin                                                                                                                       |        8|
|Trinity Western University                                                                                                                         |        8|
|University of Abertay Dundee                                                                                                                       |        8|
|University of Northampton                                                                                                                          |        8|
|University of Wales Trinity St David                                                                                                               |        8|
|Zurich University of the Arts                                                                                                                      |        8|
|Academisch Centrum Tandheelkunde Amsterdam (ACTA)                                                                                                  |        7|
|Anglia Ruskin University                                                                                                                           |        7|
|FH St. Pölten - University of Applied Sciences                                                                                                     |        7|
|HTWG Konstanz                                                                                                                                      |        7|
|Institute for Advanced Studies Vienna                                                                                                              |        7|
|Medicines for Malaria Venture                                                                                                                      |        7|
|Pädagogische Hochschule Luzern                                                                                                                     |        7|
|Queen Margaret University                                                                                                                          |        7|
|TH Brandenburg                                                                                                                                     |        7|
|Toronto General Hospital                                                                                                                           |        7|
|Women's College Hospital                                                                                                                           |        7|
|Bruyère                                                                                                                                            |        6|
|HS Neubrandenburg                                                                                                                                  |        6|
|Holland Bloorview Kids Rehabilitation Hospital                                                                                                     |        6|
|Institut für Arbeitsmarkt- und Berufsforschung                                                                                                     |        6|
|Kiel Institute for the World Economy                                                                                                               |        6|
|Netherlands Institute for Neuroscience                                                                                                             |        6|
|Netherlands Interdisciplinary Demographic Institute (NIDI)                                                                                         |        6|
|Seinäjoki University of Applied Sciences                                                                                                           |        6|
|Tampere University of Applied Sciences                                                                                                             |        6|
|University of Roehampton                                                                                                                           |        6|
|University of Teacher Education in Special Needs                                                                                                   |        6|
|HS Anhalt                                                                                                                                          |        5|
|HTW Dresden                                                                                                                                        |        5|
|JAMK University of Applied Sciences                                                                                                                |        5|
|Kwantlen Polytechnic University                                                                                                                    |        5|
|LAB University of Applied Sciences                                                                                                                 |        5|
|SWP - German Institute for International and Security Affairs                                                                                      |        5|
|University Psychiatric Services Bern                                                                                                               |        5|
|University of Worcester                                                                                                                            |        5|
|École Nationale d'Administration Publique                                                                                                          |        5|
|Institute of Art, Design + Technology                                                                                                              |        4|
|Mount Sinai Hospital                                                                                                                               |        4|
|Novia University of Applied Sciences                                                                                                               |        4|
|Potsdam FH                                                                                                                                         |        4|
|Research Institute of Molecular Pathology - IMP                                                                                                    |        4|
|University of Applied Sciences in Business Administration Zurich                                                                                   |        4|
|University of Teacher Education Zug                                                                                                                |        4|
|Université TÉLUQ                                                                                                                                   |        4|
|Algoma University                                                                                                                                  |        3|
|Carinthia University of Applied Sciences (CUAS)                                                                                                    |        3|
|FH Campus Wien - University of Applied Sciences                                                                                                    |        3|
|FH Vorarlberg - University of Applied Sciences                                                                                                     |        3|
|Fulda University of Applied Sciences                                                                                                               |        3|
|HS Furtwangen                                                                                                                                      |        3|
|Hochschule Aalen                                                                                                                                   |        3|
|IPN - Leibniz Kiel                                                                                                                                 |        3|
|Institut Universitaire de Cardiologie et de Pneumologie de Québec                                                                                  |        3|
|Kalaidos University of Applied Sciences                                                                                                            |        3|
|Medical Products Agency                                                                                                                            |        3|
|OCAD University                                                                                                                                    |        3|
|Public Health Agency of Sweden                                                                                                                     |        3|
|Pädagogische Hochschule Thurgau                                                                                                                    |        3|
|Research Institute of Molecular Pathology (IMP) / IMBA - Institute of Molecular Biotechnology / Gregor Mendel Institute of Molecular Plant Biology |        3|
|Trillium Health Partners                                                                                                                           |        3|
|Vancouver Island University                                                                                                                        |        3|
|European Chemicals Agency                                                                                                                          |        2|
|FH Joanneum - University of Applied Sciences                                                                                                       |        2|
|Finnish Defence Research Agency                                                                                                                    |        2|
|HS Kaiserslautern                                                                                                                                  |        2|
|Haute Ecole Pédagogique du Valais                                                                                                                  |        2|
|Haute École Pédagogique Fribourg                                                                                                                   |        2|
|Hubrecht Institute for Developmental Biology and Stem Cell Research                                                                                |        2|
|IRS                                                                                                                                                |        2|
|Institute Mittag-Leffler                                                                                                                           |        2|
|Lapin ammattikorkeakoulu (fi)                                                                                                                      |        2|
|Marie Cederschiöld University                                                                                                                      |        2|
|Meertens Institute                                                                                                                                 |        2|
|Modul University Vienna (MUVIENNA)                                                                                                                 |        2|
|Oulu University of Applied Sciences                                                                                                                |        2|
|Passau U                                                                                                                                           |        2|
|Princess Margaret Cancer Centre                                                                                                                    |        2|
|Pädagogische Hochschule Graubünden                                                                                                                 |        2|
|Rathenau Institute                                                                                                                                 |        2|
|Schwyz University of Teacher Education                                                                                                             |        2|
|Sophiahemmet University College                                                                                                                    |        2|
|St Jerome's University                                                                                                                             |        2|
|University Campus Suffolk                                                                                                                          |        2|
|VAMK University of Applied Sciences                                                                                                                |        2|
|AC2T Research GmbH                                                                                                                                 |        1|
|BC Children's Hospital                                                                                                                             |        1|
|Balsillie School of International Affairs                                                                                                          |        1|
|Bishop's University                                                                                                                                |        1|
|Canadian Research Knowledge Network                                                                                                                |        1|
|Centria University of Applied Sciences                                                                                                             |        1|
|City of Helsinki                                                                                                                                   |        1|
|Diaconia University of Applied Sciences                                                                                                            |        1|
|FH Kufstein Tirol - University of Applied Sciences                                                                                                 |        1|
|FHWien der WKW (FHW)                                                                                                                               |        1|
|Ferdinand Porsche FernFH                                                                                                                           |        1|
|Finnish Medicines Agency                                                                                                                           |        1|
|Forschungsinstitut für Nutztierbiologie                                                                                                            |        1|
|Haute École Pédagogique BEJUNE                                                                                                                     |        1|
|International Institute of Social History (IISH)                                                                                                   |        1|
|Netherlands Institute for Advanced Study in the Humanities and Social Sciences (NIAS)                                                              |        1|
|Northern Ontario School of Medicine University                                                                                                     |        1|
|Royal Netherlands Academy of Arts and Sciences Bureau (KNAW Bureau)                                                                                |        1|
|SAMK Satakunta University of Applied Sciences                                                                                                      |        1|
|Swiss Distance University Institute                                                                                                                |        1|
|The National Defence University                                                                                                                    |        1|
|The Swedish Environmental Protection Agency                                                                                                        |        1|
|University of Applied Sciences Burgenland                                                                                                          |        1|
|University of Applied Sciences Savonia                                                                                                             |        1|
|University of Applied Sciences Wiener Neustadt for Business and Engineering                                                                        |        1|



