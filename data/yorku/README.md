# About

This is data from the York University Libraries Open Access Author Fund.  It covers fiscal years 2009--2018.

# Source

Original data source: [YorkU OA Fund July 2018.xlsx](https://yorkspace.library.yorku.ca/xmlui/bitstream/handle/10315/27524/YorkU%20OA%20Fund%20July%202018.xlsx) from [Dataset: York University Libraries Open Access Author Fund](https://yorkspace.library.yorku.ca/xmlui/handle/10315/27524).

# Processing

The source Excel spreadsheet is cleaner than the previous version.  Once it is downloaded, this R script is all that is needed for generate the CSV here:

``` R
library(tidyverse)
library(readxl)

yorkdata <- read_excel("YorkU OA Fund July 2018.xlsx", sheet="raw data") %>%
    mutate(institution = "York University") %>%
    mutate(period = as.Date(date)) %>%
    mutate(is_hybrid = "FALSE") %>%
    rename(journal_full_title = journal_title) %>%
    ## Exclude anything with 0 cost
    filter(fee > 0) %>%
    ## Some fees are in EUR; others need to be converted from fee and currency column
    mutate(euro = if_else(currency == "EUR", fee, 0)) %>%
    ## Exclude anything without both a DOI a URL (we are missing data for these)
    filter(! (is.na(doi) & is.na(url))) %>%
    ## Add in ISSN for the one journal where it is needed (no DOI, but it does have a URL)
    mutate(issn = if_else(journal_full_title == "American Journal of Translational Research", "1943-8141", "")) %>%
    ## Exclude the one thing without a journal title, which is an ebook
    filter(! is.na(journal_full_title)) %>%
    select(institution, period, euro, doi, is_hybrid, publisher, journal_full_title, issn, url)
write_csv(yorkdata, "york-university.csv")

```

# TO DO

* Convert costs from CAD or USD to EUR.  (A very few are in EUR already, but most are USD.)

# Contact

For this data in this repo: William Denton <wdenton@yorku.ca>.  Generally for open access at York: associate dean Andrea Kosavic <akosavic@yorku.ca>.
