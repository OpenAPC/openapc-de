
## About

This directory contains APC data from the Wellcome Trust/Charity Open Access Fund for the year 2014-15. There are 3 different files:

### University_Returns_2014-2015_FINAL_Figshare.csv

This is a simple CSV export from the original Excel spreadsheet provided by the Wellcome Trust on [figshare](https://dx.doi.org/10.6084/m9.figshare.3118936.v1). No data was changed.

### University_Returns_2014-2015_FINAL_Figshare_preprocessed.csv

A preprocessed variant of the aforementioned file. The following steps were carried out to make the file processable by the OpenAPC enrichment routines:

- All columns not relevant to the OpenAPC data schema were removed.
- An 'institution' column was added, default value 'Wellcome Trust'.
- A 'period' column was added, default value '2015'. Note that this is slightly incorrect as the data time frame runs from 1st October 2014 to 30th September 2015 (Wellcome Trust financial year).
- The 'cost' column was normalised. Pound signs and decimal marks were removed. Rows with malformed monetary values (like '491625' in line 22, which originates from an already malformed value '491.625' in the original spreadsheet) were removed from the file.
- The values in the 'cost' column were converted from Pound Sterling to Euro. This was done using the average exchange rate for the reported timeframe (01-10-2014 till 30-09-2015) as provided by the [ECB](https://www.ecb.europa.eu/stats/exchange/eurofxref/html/eurofxref-graph-gbp.en.html), which is 1 GBP = 1.3488 EUR. The column was renamed to 'euro'.
- The 'Journal Type' column was renamed to 'is_hybrid'. Values were converted accordingly: 'oa' was mapped to 'FALSE', 'hybrid' to TRUE.
- All rows without a DOI were removed


In the case of rows removed, an empty line (sequence of semicolons) was inserted instead, so rows in the preprocessed file can still be assigned to their counterpart in the original file by line numbers.


