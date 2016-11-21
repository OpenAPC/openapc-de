
## About

This directory contains APC data for articles funded by the HOPE Fund (Harvard Open-access Publishing Equity), managed by the Office for Scholarly Communication (OSC) at Harvard University Library.

## Contents

For every year there are 3 different files:

### YYYY.csv

Original file as reported by the OSC (spreadsheet CSV export)

### YYYY_preprocessed.csv

A preprocessed variant, ready for OpenAPC metadata enrichment. The following intermediate steps were conducted:

- A column 'period' was added, denoting the year
- The contents of the 'is_hybrid' column were converted from '0' to 'FALSE'
- The 'Amount Awarded' column was renamed to 'Euro' and its contents (USD monetary values) converted to Euro (see below)

### YYYY_enriched.csv

Metadata enriched files, conforming to the OpenAPC data schema.

## Exchange rates

The reported APC values were converted from US Dollar to Euro. These calculations were performed using the average exchange rate for the reported timeframes as provided by the [ECB](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-usd.en.html):

| period                   | exchange rate (1 USD = )  | 
|:-------------------------|--------------------------:|
| 2010                     | 0.7559 EUR                |
| 2011                     | 0.7192 EUR                |
| 2012                     | 0.7789 EUR                |  
| 2013                     | 0.7532 EUR                |  
| 2014                     | 0.7539 EUR                | 
| 2015                     | 0.9019 EUR                |  
| 2016 (till 27 October)   | 0.8969 EUR                | 

