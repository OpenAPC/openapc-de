## About

This directory contains offsetting data for Springer Compact publications from dutch universities and institutions, kindly provided by [TU Delft Library](http://www.library.tudelft.nl/en/).

## Contents

### 160602_OC_Agreement_April_2016_report_Netherlands.xlsx

This is the original file as provided by TU Delft Library. No modifications were made.

### springer_netherlands_mm_yyyy.csv

These preprocessed files represent monthly partitions, exported from the according tables in the original spreadsheet. Most of the original columns were dropped as they are not relevant to the OpenAPC data schema.

column      | origin
------------|---------------------------------------------------------
institution | column "OC Membership Institution" in the original table
doi         | column "DOI" in the original table
period      | inserted, default value: table year
is_hybrid   | inserted, default value: TRUE

### springer_netherlands_mm_yyyy_enriched.csv

Enriched variants of the aforementioned files.

### springer_netherlands_yyyy_full_enriched.csv

Enriched files, aggregated into a yearly table.

### institution_names_normalisation.csv

As the original data was inconsistent in terms of institution designations, an additional normalisation step was required. This table shows the names in question and their normalisation targets.  
