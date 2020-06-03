
## About

This directory contains selected APC data from the [JISC collections](https://www.jisc-collections.ac.uk/Jisc-Monitor/APC-data-collection/), made available on [figshare](https://figshare.com/articles/APC_data_collected_by_Jisc_2013-2016/5335999). This collection mainly covers the 2014, 2015 and 2016 periods (OpenAPC period assignment may vary in some cases, see below).

## Contents

Starting from the JISC original spreadsheet, 3 transformation steps were applied to make the data compatible with OpenAPC. Each directory contains interim results of these steps:

### 1. original

Original file, downloaded directly from figshare. The CSV version is an export of the "Data" table without any modifications.

### 2. preprocessed

Preprocessed variants of the original files. As OpenAPC data files require 5 specific mandatory data fields (institution, period, euro, doi, is_hybrid) to make them automatically enrichable, several steps were conducted to make the original JISC file compatible with the OpenAPC data schema and enrichment routines:

1. All columns not relevant to OpenAPC were removed, reducing the file to the following items (The interim result of this step is the "columns_removed" file):

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
            - if 'Date of APC payment' denotes a day (DD-MM-YYYY), use the specific conversion rate to Euro for that day (via [fixer.io](http://fixer.io/), see [here](https://github.com/OpenAPC/openapc-de/blob/master/python/etc/preprocessing/jisc/_fixer_cache.json) for the cached values used)
            - otherwise, use the year value in 'period' to determine the [average yearly conversion rate](https://github.com/OpenAPC/openapc-de/blob/master/python/etc/preprocessing/jisc/jisc_preprocessing.py#L61) for the currency in question as provided by the [ECB](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html).
    2. if 'APC paid (£) including VAT (calculated)' [first option] or 'APC paid (£) including VAT if charged' [second option] is a numerical value larger than 0, perform a conversion:
        - if 'Date of APC payment' denotes a day (DD-MM-YYYY), use the £ -> € conversion rate for that day (via [fixer.io](http://fixer.io/))
        - otherwise, use the year value in 'period' to determine the average yearly £ -> € conversion rate.
    3. otherwise, remove the entry.

Steps 2-7 were executed by an custom python [preprocessing script](https://github.com/OpenAPC/openapc-de/blob/master/python/etc/preprocessing/jisc/jisc_preprocessing.py). The script's [output log](https://github.com/OpenAPC/openapc-de/blob/master/data/jisc_collections/preprocessed/preprocessing.log) was added to the directory along with the resulting file for reference.

8. Rows with DOIs unsuited for enrichment (non-resolving, not listed in crossref or wrong crossref publication type) were removed.
9. Inconsistent institutional names were normalised: 

|  designations                                           | normalised to                |
|:--------------------------------------------------------|-----------------------------:|
| "Newcastle University", "University of Newcastle"       | "University of Newcastle"    |
| "Durham University", "University of Durham"             | "University of Durham"       |
| "Loughborough University", "University of Loughborough" | "University of Loughborough" |

### 3. enriched

Contains the results of the OpenAPC enrichment routines after working on the preprocessed file.

Columns only used in preprocessing were dropped before enrichment, remaining columns were mapped to their OpenAPC equivalent.

Note however that metadata gathered from external sources takes precedence over existing data, so many of those values were overwritten during the process.

### 4. postprocessed

This is the final file as it was added to the OpenAPC core data. The following steps were applied during postprocessing:

1. Several duplicates were removed: 
    - Remaining internal duplicates within the jisc file itself
    - Duplicates with existing OpenAPC [Offsetting](https://github.com/OpenAPC/openapc-de/tree/master/data/offsetting) data (Springer Compact articles)
    - Duplicates with existing data provided by the [Wellcome Trust](https://github.com/OpenAPC/openapc-de/tree/master/data/wellcome) (in this case, however, the wellcome data was removed)

2. As mentioned, the 'is_hybrid' status had to be determined for all entries:
    - Since we had already already processed much of the jisc data [before](https://github.com/OpenAPC/openapc-de/releases/tag/v3.13.0), we could build upon those results and import the status for several DOIs/ISSNs automatically.
    - A second source of information to determine full OA journals was the [ISSN-GOLD-OA](https://doi.org/10.4119/unibi/2913654) dataset created by our colleagues at the [OA Analytics](https://www.intact-project.org/oa_analytics/) project. This table provides ISSNs of journals identified as fully OA and is more comprehensive than the DOAJ.
    - In contrast to JISC, we did not classify remaining unknown journals as hybrid per default. Instead, those entries were removed from the dataset and listed in a [separate file](https://github.com/OpenAPC/openapc-de/blob/master/data/jisc_collections/postprocessed/ALLAPCDATAMERGEDpublicwithnotes_final.csv) for reference and optional inclusion later on.
    
3. Some articles were reported as not having been paid for in APCs (They were published using alternative models of clearing, like the RSC "Gold 4 Gold" voucher system). Those entries were [removed](https://github.com/OpenAPC/openapc-de/commit/40220582) in accordance with the [OpenAPC cost definition](https://github.com/OpenAPC/openapc-de/wiki/Data-Submission-Handout#definition-of-costs).

4. Articles with unusually high APCs were reviewed, erroneous entries were either [fixed or removed](https://github.com/OpenAPC/openapc-de/commit/a5910267).

#### Statistics

The processing reduced the net increase in articles to OpenAPC by a large margin. The following table gives an overview on how many articles were removed for what reason.

Articles in original report: *35698*

Preprocessing:

| Reason for deletion                                                 | Count        |
|:--------------------------------------------------------------------|-------------:|
|No DOI                                                               |   - 8454 (*) |
|Unable to properly calculate a converted euro value larger than 0    |   - 3370     |
|Drop mark found                                                      |   - 2400     |
|Blacklisted pub type ('Conference Paper/Proceeding/Abstract')        |   - 45       |
|period (2017) too recent to determine average yearly conversion rate |   - 22       |
|Blacklisted pub type ('Book chapter')                                |   - 19       |
|Blacklisted pub type ('Book')                                        |   - 3        |
|Blacklisted pub type ('Letter')                                      |   - 2        |
|Blacklisted pub type ('Monograph')                                   |   - 1        |

Remaining after Preprocessing:                                           *21382* 

Postprocessing:

| Reason for deletion                                                  | Count       |
|:---------------------------------------------------------------------|------------:|
|Non-resolving DOIs                                                    | - 41        | 
|Duplicates with OpenAPC Offsetting data set (Springer Compact)        | - 269       | 
|Springer Compact Status unclear (Possible reporting errors)           | - 6         |
|Remaining internal duplicates within jisc data                        | - 156       |
|Duplicates with Wellcome Trust data                                   | - 2109      |
|Duplicates with other OpenAPC core file data ("Double reporting")     | - 6         |
|Journal Gold OA status unknown                                        | - 1808      |
|Non-APC payment model                                                 | - 73        |
|Jisc articles already present in OpenAPC (2014/15 data sets)          | - 10830     |

New articles remaining after Postprocessing:                              *6084*

(*) Some of those could be reconstructed later, see next section.

### Reconstructed DOIs

In a follow-up, some articles initially dropped for not supplying a DOI could be made available for ingestion by automatically looking up the missing DOIs in CrossRef (using the article title). The subdirectory *reconstructed_doi_articles* contains the results and interim steps of this process.

* [jisc_doiless_articles_with_titles.csv](https://github.com/OpenAPC/openapc-de/blob/master/data/jisc_collections/reconstructed_doi_articles/jisc_doiless_articles_with_titles.csv) is the starting point. It contains a subset of the original JISC spreadsheet, filtered to all articles with an article title but without a DOI. The columns are already reduced to the preprocessing set.

* dois_imported: Contains a variant of the previous file, with DOIs having been automatically imported from CrossRef.

* preprocessed, enriched, postprocessed: These directories and their contents are equivalent to the main transformation workflow in the parent directory.

#### Statistics for reconstructed DOIs:

Candidates (articles with a title but without a DOI): 2970

DOIs sucessfully imported: 2518

Preprocessing:

| Reason for deletion                                                 | Count        |
|:--------------------------------------------------------------------|-------------:|
|Drop mark found                                                      |   367        |
|Unable to properly calculate a converted euro value                  |   299        |
|Blacklisted pub type ('Conference Paper/Proceeding/Abstract')        |   13         |
|Blacklisted pub type ('Book chapter')                                |   5          |
|Blacklisted pub type ('Book edited')                                 |   2          |
|Blacklisted pub type ('Book')                                        |   1          |
|Additional unsupported publication types (via CrossRef)              |   8          |

Remaining after Preprocessing:                                          *1823*

Postprocessing:

| Reason for deletion                                                  | Count       |
|:---------------------------------------------------------------------|------------:|
|Duplicates with Wellcome Trust data                                   | - 254       |
|Resolvable duplicates with existing jisc data / internal duplicates   | - 25        |
|Non-resolvable introduced duplicates (*)                              | - 11 (x2)   |
|Non-resolvable introduced duplicates with OpenAIRE (*)                | - 1 (x2)    |

New articles remaining after Postprocessing:                              *1520*

(*) This happens when a reconstructed DOI article is already present in our ingested data and the cost information differs. Since there's no indication which entry is correct, we have to remove them both, thus the (x2).
