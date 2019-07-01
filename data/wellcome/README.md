
## About

This directory contains APC data from the Wellcome Trust/Charity Open Access Fund from 2013 to 2017. There are 3 different files for each period (fiscal year running from 1st October to 30th September):

### Original files

- University_Returns_2013-2014_FINAL_Figshare.csv
- University_Returns_2014-2015_FINAL_Figshare.csv
- COAF_All_institutes_full_data_combined_v2_FIGSHARE_2015-2016.csv
- COAF_Institutes_16_17_Data_FIGSHAREv2.csv

These are simple CSV exports from the original Excel spreadsheets provided by the Wellcome Trust on figshare ([2013-14](http://dx.doi.org/10.6084/M9.FIGSHARE.1321361), [2014-15](https://dx.doi.org/10.6084/m9.figshare.3118936.v1), [2015-16](https://doi.org/10.6084/m9.figshare.4765999.v2) and [2016-17](https://doi.org/10.6084/m9.figshare.6205376)). No data was changed.

### Preprocessed files

Preprocessed variants of the aforementioned files are indicated by a "_preprocessed" suffix. The following steps were carried out to make the files processable by the OpenAPC enrichment routines:

- All columns not relevant to the OpenAPC data schema were removed.
- An 'institution' column was added, default value 'Wellcome Trust'.
- A 'period' column was added, defaulting to the second year of each file. Note that this is slightly incorrect as the data time frames run from 1st October to 30th September of the following year (Wellcome Trust financial year). However, there is no means to adress this issue at the moment.
- The 'cost' column was normalised. Pound signs and decimal marks were removed. Rows with malformed monetary values (like '491625' in line 22 of the 2014-15 file, which originates from an already malformed value '491.625' in the original spreadsheet) were removed.
- The values in the 'cost' column were converted from Pound Sterling to Euro. This was done using the average exchange rate for the reported timeframes as provided by the [ECB](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-gbp.en.html). The column was renamed to 'euro'.

|file                                                                          | time frame                 | exchange rate (1 GBP =)     | 
|:-----------------------------------------------------------------------------|---------------------------:|----------------------------:|
|University_Returns_2013-2014_FINAL_Figshare_preprocessed.csv                  | 01-10-2013 till 30-09-2014 | 1.2215 EUR                  |
|University_Returns_2014-2015_FINAL_Figshare_preprocessed.csv                  | 01-10-2014 till 30-09-2015 | 1.3488 EUR                  |
|COAF_All_institutes_full_data_combined_v2_FIGSHARE_2015-2016_preprocessed.csv | 01-10-2015 till 30-09-2016 | 1.1477 EUR                  |
|COAF_Institutes_16_17_Data_FIGSHAREv2_preprocessed.csv                        | 01-10-2016 till 30-09-2017 | 1.1405 EUR                  |

- The 'Journal Type' column was renamed to 'is_hybrid'. Values were converted accordingly: 'oa' was mapped to 'FALSE', 'hybrid' to TRUE (in case of 2016/17: Column 'Fully Open Access Journal', '0' mapped to TRUE, '1' mapped to FALSE).
- All rows without a DOI or a cost value of 0 were removed.

In all cases of rows removed, an empty line (sequence of semicolons) was inserted instead, so rows in the preprocessed files can still be assigned to their counterpart in the original file by line numbers.

### Enriched files

Enriched, OpenAPC-compatible version of the preprocessed files. During enrichment, values in the columns PMCID, PMID, Publisher, Journal title and ISSN were replaced if in conflict with a non-NA value imported from Crossref/Pubmed. 

In addition, some corrections were applied post-enrichment:

- Missing or wrong hybrid status was manually corrected in several cases
- Entries with non-supported publication types (book chapters, proceedings...) were removed
- duplicate cases were resolved (see below)

## Duplicate treatment

Since OpenAPC ingests APC data for the UK from other sources as well (most notably the [Jisc collections](https://github.com/OpenAPC/openapc-de/tree/master/data/jisc_collections)), duplicates (identified via DOI) arise frequently (In fact, for the 2016/17 data set we identified about 70% of all articles as already being present in our collections!). 
Those cases have to be cleared as OpenAPC enforces a strict no-duplicate policy over all its data sets. Here's an overview of possible duplicate cases and how they are resolved:

| type            |                                              description                                | resolving strategy                                           | reasoning                                                                                                                       | example |
|:----------------|-----------------------------------------------------------------------------------------|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|--------:|
| internal        | A DOI occuring more than once inside a COAF data file                                   | Delete all cases                                             | Unable to determine which entry is correct                                                                                      | [c63f3a3a](https://github.com/OpenAPC/openapc-de/commit/c63f3a3a) |
| Jisc data       | A DOI also reported by Jisc in a collections report                                     | Keep Jisc article, drop COAF entry                           | Jisc data more informative (states the author's affiliation)                                                                    | [7beaecfc](https://github.com/OpenAPC/openapc-de/commit/7beaecfc) |
| offsetting data | A DOI also reported in an offsetting report (usually Springer Compact UK)               | Keep offsetting data, drop COAF entry                        | No "standard" APC is charged for articles published under offsetting contracts                                                  | [c6797749](https://github.com/OpenAPC/openapc-de/commit/c6797749) |
| other duplicate | Article already present in OpenAPC core data and not originating from a Jisc report     | Move both articles to unresolved duplicates collection file  | Unable to determine if case of "double reporting" (Full APC reported twice) or co-funding (APC shared between institutions)     |         |

