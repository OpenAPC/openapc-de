
## About

This directory contains selected APC data from the [JISC collections](https://www.jisc-collections.ac.uk/Jisc-Monitor/APC-data-collection/), made available on [figshare](https://figshare.com/search?q=jisc+collections&quick=1).

## Contents

Starting from the JISC original files, 3 transformation steps were applied to each file:

### original

Original files, downloaded directly from figshare

### preprocessed

Preprocessed variants of the original files. As OpenAPC data files require 5 specific mandatory data fields (institution, period, euro, doi, is_hybrid) to make them automatically enrichable, several steps were conducted to make the original JISC files compatible with the OpenAPC data schema and enrichment routines:

- All columns not relevant to OpenAPC were deleted, reducing the file to 11 columns: Institution, PubMed Central (PMC) ID, PubMed ID, DOI, Publisher, Journal, ISSN, Type of publication, Date of APC payment, APC paid (£) including VAT if charged, Licence
- All rows without a valid entry in the 'DOI' column were removed (Note that for this and every following row removal steps the line in question was replaced by a comma sequence, so line numbers in the preprocessed files still correspond to their counterpart in the original file).
- The 'Type of publication' column was renamed to 'is_hybrid'. Its contents were mapped as follows:

  | value                                     | target          | 
  |:------------------------------------------|----------------:|
  | Journal Article/Review (Full OA journal)  | FALSE           |
  | Journal Article/Review (Hybrid journal)   | TRUE            |

  All rows containing other values (Book chapter, Conference Paper/Proceeding/Abstract) were deleted (but empty lines were kept).

- The 'Date of APC payment' column was renamed to 'period'. Its values (various date formats) were converted to 4-digit years. In case of missing values a default value equal to the reported year of the file was assigned (e.g. 2014 for APCs2014combined.csv).
- The reported APC values in the 'APC paid (£) including VAT if charged' column were normalised and converted from Pound Sterling to Euro. These calculations were performed using the average exchange rate for the reported timeframes as provided by the [ECB](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-gbp.en.html) (See below for a table listing the applied rates). The column was renamed to 'euro' afterwards. Lines containing malformed or missing values were removed. 

### enriched

Contains the results of the OpenAPC enrichment routines after working on the preprocessed files. In addition to the mandatory columns already prepared during the preprocessing the following columns were recognised by the processing script and transfered directly into the resulting data schema:

| JISC column                       | OpenAPC column          | 
|:----------------------------------|------------------------:|
| PubMed Central (PMC) ID)          | pmcid                   |
| PubMed ID                         | pmid                    |
| Publisher                         | publisher               |
| Journal                           | journal_full_title      |
| ISSN                              | issn                    |
| Licence                           | license_ref             |

Note however that metadata gathered from external sources during the enrichment takes precedence over existing data, so many of those values were overwritten during the process.

### final

A shortcoming of many processed files is the lack of data in the 'Type of publication' column, giving no information on the journal's hybrid status (which is mandatory for OpenAPC). We attempted to mitigate this by automatically importing the hybrid status for by matching journal names from the OpenAPC core data file and the offsetting data file. The files in this directory are the result of this process. Articles without information on hybrid status after this point were deleted. 


## Exchange rates

| period                   | exchange rate (1 GBP = )  | 
|:-------------------------|--------------------------:|
| 2014                     | 1.2411 EUR                | 

