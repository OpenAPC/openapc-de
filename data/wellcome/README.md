
## About

This directory contains APC data from the Wellcome Trust/Charity Open Access Fund for the 2013-14, 2014-15 and 2015-16 periods. For each period there are 3 different files:

### Original files

- University_Returns_2013-2014_FINAL_Figshare.csv
- University_Returns_2014-2015_FINAL_Figshare.csv
- COAF_All_institutes_full_data_combined_v2_FIGSHARE_2015-2016.csv

These are simple CSV exports from the original Excel spreadsheets provided by the Wellcome Trust on figshare ([2013-14](http://dx.doi.org/10.6084/M9.FIGSHARE.1321361), [2014-15](https://dx.doi.org/10.6084/m9.figshare.3118936.v1) and [2015-16](https://doi.org/10.6084/m9.figshare.4765999.v2)). No data was changed.

### Preprocessed files

Preprocessed variants of the aforementioned files are indicated by a "_preprocessed" suffix. The following steps were carried out to make the files processable by the OpenAPC enrichment routines:

- All columns not relevant to the OpenAPC data schema were removed.
- An 'institution' column was added, default value 'Wellcome Trust'.
- A 'period' column was added, defaulting to the second year of each file. Note that this is slightly incorrect as the data time frames run from 1st October to 30th September of the following year (Wellcome Trust financial year). However, there is no means to adress this issue at the moment.
- The 'cost' column was normalised. Pound signs and decimal marks were removed. Rows with malformed monetary values (like '491625' in line 22 of the 2014-15 file, which originates from an already malformed value '491.625' in the original spreadsheet) were removed.
- The values in the 'cost' column were converted from Pound Sterling to Euro. This was done using the average exchange rate for the reported timeframes as provided by the [ECB](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-gbp.en.html). The column was renamed to 'euro'.

|file                                                             | time frame                 | exchange rate (1 GBP =)     | 
|:----------------------------------------------------------------|---------------------------:|----------------------------:|
|University_Returns_2013-2014_FINAL_Figshare_preprocessed.csv     | 01-10-2013 till 30-09-2014 | 1.2215 EUR                  |
|University_Returns_2014-2015_FINAL_Figshare_preprocessed.csv     | 01-10-2014 till 30-09-2015 | 1.3488 EUR                  |
|COAF_All_institutes_full_data_combined_v2_FIGSHARE_2015-2016.csv | 01-10-2015 till 30-09-2016 | 1.1477 EUR                  |

- The 'Journal Type' column was renamed to 'is_hybrid'. Values were converted accordingly: 'oa' was mapped to 'FALSE', 'hybrid' to TRUE.
- All rows without a DOI were removed

Additionally, some semantical corrections were conducted:

- Cases of duplicate DOIs were corrected, either by deleting the duplicate or by manually correcting the DOI in case of obviously wrong assignments (Example: [c27ba52](https://github.com/OpenAPC/openapc-de/commit/c27ba52325d96441deeb0bc2ba81fad81c926e85)). In case of duplicates across different periods, the most recent entry was given precedence in all cases.
- Missing hybrid status was manually added in several cases and entries with non-supported publication types (book chapters, proceedings...) were removed (Example: [14c04f6](https://github.com/OpenAPC/openapc-de/commit/14c04f6c71b7938bd64f9bcb679db760165b971c)).

In the case of rows removed, an empty line (sequence of semicolons) was inserted instead, so rows in the preprocessed files can still be assigned to their counterpart in the original file by line numbers.

### Enriched files

Enriched, OpenAPC-compatible version of the preprocessed files. During enrichment, the following overwriting policy was employed:

Values in the columns PMCID, PMID, Publisher, Journal title and ISSN were replaced if in conflict with a non-NA value imported from Crossref/Pubmed. 

## Duplicate treatment in connection with JISC data

The JISC collections data processed in December 2016 included a lot of articles already reported by the Wellcome Trust. Since the JISC data provides a more accurate breakdown (institutions), it was given precedence and the equivalent Wellcome records were removed (See [7ef06f2](https://github.com/OpenAPC/openapc-de/commit/7ef06f28edc7c78b6e5aa2b9610b6b4e16740529) and [ac797c0](https://github.com/OpenAPC/openapc-de/commit/ac797c02762cba7841c2bc827e318bcb39581176)).
