
## About

This directory contains selected APC data from the [JISC collections](https://www.jisc-collections.ac.uk/Jisc-Monitor/APC-data-collection/), made available on [figshare](https://figshare.com/articles/APC_data_collected_by_Jisc_2013-2016/5335999).

## Contents

Starting from the JISC original spreadsheet, 3 transformation steps were applied to make the data compatible with OpenAPC. Each directory contains interim results of these steps:

### 1. original

Original file, downloaded directly from figshare. The CSV version is an export of the "Data" table without any modifications.

### 2. preprocessed

Preprocessed variant of the original files. As OpenAPC data files require 5 specific mandatory data fields (institution, period, euro, doi, is_hybrid) to make them automatically enrichable, several steps were conducted to make the original JISC file compatible with the OpenAPC data schema and enrichment routines:

1. All columns not relevant to OpenAPC were removed, reducing the file to the following items:

| JISC column                                         | Used in                   | Usage                                           |  
|:----------------------------------------------------|---------------------------|------------------------------------------------:|
| APC paid (actual currency) including VAT if charged | preprocessing             | generation of 'euro' column                     |
| APC paid (£) including VAT (calculated)             | preprocessing             | generation of 'euro' column                     |
| APC paid (£) including VAT if charged               | preprocessing             | generation of 'euro' column                     |
| Currency of APC                                     | preprocessing             | generation of 'euro' column                     |
| DOI                                                 | preprocessing, enrichment | mapped to column "doi", record deletion         |
| Date of APC payment                                 | preprocessing             | generation of 'period' column                   |
| Date of initial application by author               | preprocessing             | generation of 'period' column                   |
| ISSN0                                               | enrichment                | mapped to column "issn"                         |
| Institution                                         | enrichment                | mapped to column "institution"                  |
| Journal                                             | enrichment                | mapped to column "journal_full_title"           |
| Licence                                             | enrichment                | mapped to column "license_ref"                  |
| PubMed Central (PMC) ID                             | enrichment                | mapped to column "pmcid"                        |
| PubMed ID                                           | enrichment                | mapped to column "pmid"                         |
| Publisher                                           | enrichment                | mapped to column "publisher"                    |
| TCO year                                            | preprocessing             | generation of 'period' column                   |
| Type of publication                                 | preprocessing             | record deletion                                 |
| Drop?                                               | preprocessing             | record deletion                                 |
| Year of publication                                 | preprocessing             | generation of 'period' column                   |
 
2. All rows without a valid entry in the 'DOI' column were removed (Note that for this and every following row removal steps the line in question was replaced by a comma sequence, so line numbers in the preprocessed file still correspond to their counterpart in the original file).
3. All rows with a '1' in the 'Drop?' column were removed, these entries were identified as [removable duplicates](https://nbviewer.jupyter.org/github/kshamash/Article-processing-charges/blob/master/Autogenerate%20APC%20report.ipynb#De-duplication) by JISC. Note that JISC's de-duplication rules, although being compatible with OpenAPC's, do not resolve every duplicate case, so this would require additional efforts on our side later on (OpenAPC enforces a strict [no-duplicate](https://github.com/OpenAPC/openapc-de/wiki/Data-Integrity-Testing#interdependent-tests) policy on DOIs in its datasets).
4. All rows containing one of the following RIOXX terms in the 'Type of publication' column were removed: 'Book', 'Book chapter', 'Book edited', 'Conference Paper/Proceeding/Abstract', 'Letter', 'Monograph'.
5. The 'period' column was added. Since its definition by the OpenAPC data schema is 'Year of APC payment', the value was copied from one of the 'date' columns using the following order (We took the value from the highest ranking non-empty column, optionally formatted as YYYY):
    - Date of APC payment
    - Year of publication
    - Date of initial application by author
    - TCO year
6. The 'is_hybrid' column was added, but initially left empty. Assigning journal hybrid status was postponed to post-enrichment (see below).
7. The 'euro' column was added, with the following heuristic applied to determine its values:
    1. if 'APC paid (actual currency) including VAT if charged' is a numerical value larger than 0:
        - if 'Currency of APC' is 'EUR', use the value directly
        - if 'Currency of APC' is any other non-null value (AUD, CAD, CHF, GBP, JPY, USD), perform a conversion:
            - if 'Date of APC payment' denotes a day (DD-MM-YYYY), use the specific conversion rate to Euro for that day (via [fixer.io](http://fixer.io/))
            - otherwise, use the year value in 'period' to determine the average yearly conversion rate for the currency in question (see below for details).
    2. if 'APC paid (£) including VAT (calculated)' [first option] or 'APC paid (£) including VAT if charged' [second option] is a numerical value larger than 0, perform a conversion:
        - if 'Date of APC payment' denotes a day (DD-MM-YYYY), use the £ -> € conversion rate for that day (via [fixer.io](http://fixer.io/))
        - otherwise, use the year value in 'period' to determine the average yearly £ -> € conversion rate.
    3. otherwise, remove the entry.

### 3. enriched

Contains the results of the OpenAPC enrichment routines after working on the preprocessed file.

Columns only used in preprocessing were dropped before enrichment, remaining columns were mapped to their OpenAPC equivalent.

Note however that metadata gathered from external sources takes precedence over existing data, so many of those values were overwritten during the process.

### 4. postprocessed

As a final step, the 'is_hybrid' status had to be determined for all entries:
- Since we had already already processed much of the jisc data [before](https://github.com/OpenAPC/openapc-de/releases/tag/v3.13.0), we could build upon those results and import the status for several DOIs/ISSNs automatically.
- A second source of information to determine full OA journals was the [ISSN-GOLD-OA](https://doi.org/10.4119/unibi/2906347) dataset created by our colleagues at the [OA Analytics](https://www.intact-project.org/oa_analytics/) project. This table provides ISSNs of journals identified as fully OA and is more comprehensive than the DOAJ.
- In contrast to JISC, we did not classify remaining unknown journals as hybrid per default. Instead, those entries were removed from the dataset and listed in a separate file for reference ("not_included_hybrid_status_unknown")

- Cases of co-funding (DOI duplicates between different institutions) were removed. A file tagged with the suffix "not_included_co_funding" lists these articles for reference.
- Other Duplicates were removed, either by correcting the data (in obvious cases) or by removing both entries if the correct one could not be determined.


## Exchange rates

| period                   | exchange rate (1 GBP = )  | 
|:-------------------------|--------------------------:|
| 2013                     | 1.1777 EUR                |
| 2014                     | 1.2411 EUR                | 
| 2015                     | 1.3785 EUR                |
| 2016                     | 1.2239 EUR                |
