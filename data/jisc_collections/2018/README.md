
## About

This directory contains APC data from the [JISC collections](https://www.jisc-collections.ac.uk/Jisc-Monitor/APC-data-collection/) for the 2018 period.

## Contents

Starting from the JISC original data, 3 transformation steps were applied to make the data compatible with OpenAPC. Each directory contains interim results of these steps:

### 1. original

CSV export of the Excel spreadsheet provided by Jisc. No data was modified.

### 2. preprocessed

Preprocessed variant of the original files. As OpenAPC data files require 5 specific mandatory data fields (institution, period, euro, doi, is_hybrid) to make them automatically enrichable, several steps were conducted to make the original JISC file compatible with the OpenAPC data schema and enrichment routines:

1. All columns either not relevant to OpenAPC or not containing any values were removed, reducing the file to the following items (The interim result of this step is the "columns_removed" file):

| JISC column                                         | Used in                   | Usage                                           |  
|:----------------------------------------------------|---------------------------|------------------------------------------------:|
| Institution                                         | enrichment                | mapped to column "institution"                  |
| Date of acceptance                                  | preprocessing             | generation of 'period' column                   |
| PubMed ID                                           | enrichment                | mapped to column "pmid"                         |
| DOI                                                 | preprocessing, enrichment | mapped to column "doi", record deletion         |
| Publisher                                           | enrichment                | mapped to column "publisher"                    |
| Journal                                             | enrichment                | mapped to column "journal_full_title"           |
| Type of publication                                 | preprocessing             | record deletion                                 |
| Article title                                       | preprocessing             | reverse DOI lookup                              |
| Date of publication                                 | preprocessing             | generation of 'period' column                   |
| Date of APC payment                                 | preprocessing             | generation of 'period' column                   |
| APC paid (£) including VAT if charged               | preprocessing             | generation of 'euro' column                     |

2. A [reverse DOI lookup](http://openapc.github.io/general/openapc/2018/01/29/doi-reverse-lookup/) was tried on all entries without a DOI. In case of success the reconstructed DOI was added. 

3. All rows without a valid entry in the 'DOI' column were removed (Note that for this and every following row removal steps the line in question was replaced by a comma sequence, so line numbers in the preprocessed file still correspond to their counterpart in the original file).
4. All rows containing one of the following RIOXX terms in the 'Type of publication' column were removed: 'Book', 'Book chapter', 'Book edited', 'Conference Paper/Proceeding/Abstract', 'Letter', 'Monograph'.
5. The 'period' column was added. Since its definition by the OpenAPC data schema is 'Year of APC payment', the value was copied from one of the 'date' columns using the following order (We took the value from the highest ranking non-empty column, optionally formatted as YYYY):
    - Date of APC payment 
    - Date of publication
    - Date of acceptance
6. The 'is_hybrid' column was added, but initially left empty. Assigning journal hybrid status was postponed to post-enrichment (see below).
7. The 'euro' column was added, with the following heuristic applied to determine its values:
    1. if 'APC paid (£) including VAT if charged' is a numerical value larger than 0, perform a conversion:
        - if 'Date of APC payment' denotes a day (MM/DD/YYYY), use the £ -> € conversion rate for that day (obtained from the [ECB statistical data warehouse](https://sdw.ecb.europa.eu/) which provides historic exchange rates)
        - otherwise, use the year value in 'period' and apply the average annual £ -> € conversion rate (also obtained from the ECB SDW).
    2. otherwise, remove the entry.

Steps 3-7 were executed by an custom python [preprocessing script](https://github.com/OpenAPC/openapc-de/blob/master/python/etc/preprocessing/jisc/jisc_preprocessing.py). The script's [output log](https://github.com/OpenAPC/openapc-de/blob/master/data/jisc_collections/2018/preprocessed/preprocessing.log) was added to the directory along with the resulting file for reference.

8. Rows with DOIs unsuited for enrichment (non-resolving, not listed in crossref or wrong crossref publication type) were removed.

### 3. enriched

Contains the results of the OpenAPC enrichment routines after working on the preprocessed file.

Columns only used in preprocessing were dropped before enrichment, remaining columns were mapped to their OpenAPC equivalent.

Note however that metadata gathered from external sources takes precedence over existing data, so many of those values were overwritten during the process.

### 4. postprocessed

This is the final file as it was added to the OpenAPC core data. The following steps were applied during postprocessing:

1. Some institutional designations were changed to match earlier Jisc data:

|  designation                                            | changed to                         |
|:--------------------------------------------------------|-----------------------------------:|
| "Loughborough University"                               | "University of Loughborough"       |
| "Newcastle University"                                  | "University of Newcastle"          |
| "Durham University"                                     | "University of Durham"             |
| "Queen Mary University of London"                       | "Queen Mary, University of London" |

1. Several duplicates were resolved: 
    - Internal duplicates within the jisc file itself
    - Duplicates with existing OpenAPC core data (mainly articles originating from previous Jisc data ingestions)
    - Duplicates with existing Transformative Agreements data (Some participants reported articles falling under the Springer Compact offsetting deals for UK)
    - Duplicates with existing data provided by the [Wellcome Trust](https://github.com/OpenAPC/openapc-de/tree/master/data/wellcome) (in this case, however, the wellcome data was removed)

2. As mentioned, the 'is_hybrid' status had to be determined for all entries. We used 3 different sources to infer it either based on journal titles or ISSN_L:
    
|  source                                                                                      | mapping based on                  |  inferred hybrid status    |
|:---------------------------------------------------------------------------------------------|-----------------------------------|---------------------------:|
| OpenAPC core data file                                                                       | journal_full_title                | TRUE and FALSE             |
| OpenAPC Transformative Agreements data file                                                  | journal_full_title                | TRUE only                  |
| [ISSN-GOLD-OA](https://doi.org/10.4119/unibi/2913654) data set                               | issn_l                            | FALSE only                 |
| [JournalTOCs data import](https://openapc.github.io/general/openapc/2018/07/11/journaltocs/) | issn, issn_electronic, issn_print | TRUE and FALSE             |

