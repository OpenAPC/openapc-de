
## About

This directory contains selected APC data from the [JISC collections](https://www.jisc-collections.ac.uk/Jisc-Monitor/APC-data-collection/). This collection is an extract from an aggregated file, filtered (TCO year) to cover the 2017 period (OpenAPC period assignment may vary in some cases, see below).

## Contents

Starting from the JISC original data, 3 transformation steps were applied to make the data compatible with OpenAPC. Each directory contains interim results of these steps:

### 1. original

CSV export of the Excel spreadsheet provided by Jisc. No data was modified aside from filtering to restrict the articles to the 2017 period.

### 2. preprocessed

Preprocessed variant of the original files. As OpenAPC data files require 5 specific mandatory data fields (institution, period, euro, doi, is_hybrid) to make them automatically enrichable, several steps were conducted to make the original JISC file compatible with the OpenAPC data schema and enrichment routines:

1. All columns either not relevant to OpenAPC or not containing any values were removed, reducing the file to the following items (The interim result of this step is the "columns_removed" file):

| JISC column                                         | Used in                   | Usage                                           |  
|:----------------------------------------------------|---------------------------|------------------------------------------------:|
| APC paid (£) including VAT if charged               | preprocessing             | generation of 'euro' column                     |
| DOI                                                 | preprocessing, enrichment | mapped to column "doi", record deletion         |
| Date of APC payment                                 | preprocessing             | generation of 'period' column                   |
| ISSN0                                               | enrichment                | mapped to column "issn"                         |
| Institution                                         | enrichment                | mapped to column "institution"                  |
| Journal                                             | enrichment                | mapped to column "journal_full_title"           |
| Licence                                             | enrichment                | mapped to column "license_ref"                  |
| PubMed ID                                           | enrichment                | mapped to column "pmid"                         |
| Publisher                                           | enrichment                | mapped to column "publisher"                    |
| TCO year                                            | preprocessing             | generation of 'period' column                   |
| Type of publication                                 | preprocessing             | record deletion                                 |
| Drop?                                               | preprocessing             | record deletion                                 |
| Period of APC payment                               | preprocessing             | generation of 'period' column                   |
 
2. All rows without a valid entry in the 'DOI' column were removed (Note that for this and every following row removal steps the line in question was replaced by a comma sequence, so line numbers in the preprocessed file still correspond to their counterpart in the original file).
3. All rows with a '1' in the 'Drop?' column were removed, these entries were identified as [removable duplicates](https://nbviewer.jupyter.org/github/kshamash/Article-processing-charges/blob/master/Autogenerate%20APC%20report.ipynb#De-duplication) by JISC. Note that JISC's de-duplication rules, although being compatible with OpenAPC's, do not resolve every duplicate case, so this would require additional efforts on our side later on (OpenAPC enforces a strict [no-duplicate](https://github.com/OpenAPC/openapc-de/wiki/Data-Integrity-Testing#interdependent-tests) policy on DOIs in its datasets).
4. All rows containing one of the following RIOXX terms in the 'Type of publication' column were removed: 'Book', 'Book chapter', 'Book edited', 'Conference Paper/Proceeding/Abstract', 'Letter', 'Monograph'.
5. The 'period' column was added. Since its definition by the OpenAPC data schema is 'Year of APC payment', the value was copied from one of the 'date' columns using the following order (We took the value from the highest ranking non-empty column, optionally formatted as YYYY):
    - Date of APC payment
    - Period of APC payment
    - TCO year
6. The 'is_hybrid' column was added, but initially left empty. Assigning journal hybrid status was postponed to post-enrichment (see below).
7. The 'euro' column was added, with the following heuristic applied to determine its values:
    1. if 'APC paid (£) including VAT if charged' is a numerical value larger than 0, perform a conversion:
        - if 'Date of APC payment' denotes a day (DD-MM-YYYY), use the £ -> € conversion rate for that day (obtained from the [ECB statistical data warehouse](https://sdw.ecb.europa.eu/) which provides historic exchange rates)
        - otherwise, use the year value in 'period' and apply the average annual £ -> € conversion rate (also obtained from the ECB SDW).
    2. otherwise, remove the entry.

Steps 2-7 were executed by an custom python [preprocessing script](https://github.com/OpenAPC/openapc-de/blob/master/python/etc/preprocessing/jisc/jisc_preprocessing.py). The script's [output log](https://github.com/OpenAPC/openapc-de/blob/master/data/jisc_collections/2017/preprocessed/preprocessing.log) was added to the directory along with the resulting file for reference.

8. Rows with DOIs unsuited for enrichment (non-resolving, not listed in crossref or wrong crossref publication type) were removed.

### 3. enriched

Contains the results of the OpenAPC enrichment routines after working on the preprocessed file.

Columns only used in preprocessing were dropped before enrichment, remaining columns were mapped to their OpenAPC equivalent.

Note however that metadata gathered from external sources takes precedence over existing data, so many of those values were overwritten during the process.

### 4. postprocessed

This is the final file as it was added to the OpenAPC core data. The following steps were applied during postprocessing:

1. Some institutional designations were adapted to match earlier Jisc data:

|  designation                                            | changed to                   |
|:--------------------------------------------------------|-----------------------------:|
| "London School of Economics"                            | "LSE"                        |
| "Loughborough University"                               | "University of Loughborough" |


1. Several duplicates were removed: 
    - Internal duplicates within the jisc file itself
    - Duplicates with existing OpenAPC data (only articles originating from previous Jisc data ingestions)
    - Duplicates with existing OpenAPC offsetting data (Some participants reported articles falling under the Springer Compact offsetting deals for UK)
    - Duplicates with existing data provided by the [Wellcome Trust](https://github.com/OpenAPC/openapc-de/tree/master/data/wellcome) (in this case, however, the wellcome data was removed)

2. As mentioned, the 'is_hybrid' status had to be determined for all entries. We used 3 different sources to infer it either based on journal titles or ISSN_L:
    
|  source                                                         | mapping based on    |  inferred hybrid status    |
|:----------------------------------------------------------------|---------------------|---------------------------:|
| OpenAPC core data file                                          | journal_full_title  | TRUE and FALSE             |
| OpenAPC offsetting data file                                    | journal_full_title  | TRUE only                  |
| [ISSN-GOLD-OA](https://doi.org/10.4119/unibi/2913654) data set  | issn_l              | FALSE only                 |


In contrast to JISC, we did not classify remaining unknown journals as hybrid per default. Instead, those entries were removed from the dataset and listed in a [separate file](https://github.com/OpenAPC/openapc-de/blob/master/data/jisc_collections/2017/postprocessed/Jisc_2017_postprocessed_not_included_hybrid_status_unknown.csv) for reference and optional inclusion later on.

#### Statistics

The processing reduced the net increase in articles to OpenAPC. The following table gives an overview on how many articles were removed for what reason.

Articles in original report: *23104*

Preprocessing:

| Reason for deletion                                                 | Count        |
|:--------------------------------------------------------------------|-------------:|
|Unable to properly calculate a converted euro value larger than 0    |   - 5034     |
|No DOI                                                               |   - 1659     |
|Drop mark found                                                      |   - 360      |
|period (2017) too recent to determine average yearly conversion rate |   - 210      |
|Blacklisted pub type ('Conference Paper/Proceeding/Abstract')        |   - 107      |
|Blacklisted pub type ('Book chapter')                                |   - 16       |
|Blacklisted pub type ('Book')                                        |   - 1        |

Remaining after Preprocessing:                                           *15717* 

Postprocessing:

| Reason for deletion                                                  | Count       |
|:---------------------------------------------------------------------|------------:|
|Non-resolving DOIs                                                    | - 45        | 
|Internal duplicates within Jisc data file                             | - 246       |
|Duplicates with previously reported Jisc data                         | - 291       |
|Duplicates with other previously reported data                        | - 5         |
|Duplicates with OpenAPC offsetting data                               | - 426       |
|Journal Gold OA status unknown                                        | - 1398      |

New articles remaining after Postprocessing:                              *13306*
