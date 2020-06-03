## About 

This directory contains APC data from Norwegian institutions, provided by the Norwegian APC funds.

## Contents

Starting from the provided original spreadsheet, 3 transformation steps were applied to make the data compatible with OpenAPC's data format. Each directory contains interim results of these steps.

### 1. original

Contains a csv export of the original Excel spreadsheet. No data was modified.

### 2. preprocessed

Preprocessed variant of the original file. This file is a result of the following transformation steps:

1. All contents in the "DOI" column not representing a resolving DOI were removed.
2. For all entries with an empty "DOI" field, reconstruction of the correct DOI was attempted via semi-automatic article title lookup (crossref API).
3. Articles without a recoverable DOI were removed.
4. Monetary values ("APC in NOK") were converted from Norwegian kroner to Euro using average exchange rates for the according year (see below).
5. Some column titles were modified (see below) to make them reusable by our enrichment script.

### 3. enriched

Contains the results of the OpenAPC enrichment routines after working on the preprocessed file.

### 4. postprocessed

Some additional steps were required before adding the data to the OpenAPC core data file:

1. Since the original file lacked information on the hybrid status of journals (mandatory column "is_hybrid" in OpenAPC), this field was imported from existing data in the core/offsetting files. New journals were classified manually.
2. Duplicate cases (DOIs occuring more than once) were either resolved or removed if no solution was obvious. These changes were applied retroactively to the enriched and preprocessed files.
3. Articles from Telemark University College processed in 2016 were reassigned to University College of Southeast Norway (Telemark UC was merged into USN on 1 January 2016).

### Column usage and mappings

| Column              | Changed to  | Usage                                         |
|:--------------------|-------------|----------------------------------------------:|
| Year                | period      | mapped to OpenAPC column "period"             |
| Institution - Abbrv | -           | dropped                                       |
| Instsitution [sic]  | institution | mapped to OpenAPC column "institution"        |
| ArticleTitle        | -           | reverse DOI lookup if applicable; dropped     |
| JournalTitle        | -           | mapped to OpenAPC column "journal_full_title" |
| ISSN                | -           | mapped to OpenAPC column "issn"               |
| NSD Level           | -           | dropped                                       |
| DOI                 | -           | mapped to OpenAPC column "doi"                |
| APC in NOK          | euro        | converted; mapped to OpenAPC column "euro"    |


### Exchange Rates

|period    | exchange rate (1 NOK =)     | 
|:---------|----------------------------:|
| 2015     |  0.1119 EUR                 |
| 2016     |  0.1077 EUR                 |
