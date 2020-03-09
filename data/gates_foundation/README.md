## About

This directory contains data on APC costs covered by the [Bill and Melinda Gates Foundation](https://www.gatesfoundation.org/how-we-work/general-information/open-access-policy). Since the original data required some preprocessing to make it ingestible by OpenAPC, intermediate results are provided together with the original and the final, OpenAPC-compatible version.

### Original

File: [Gates_Open_Access_Publishing_Charges_Project_Data.csv](Gates_Open_Access_Publishing_Charges_Project_Data.csv)

This is the original CSV file as obtained from the [UCLA Dataverse repository](https://dataverse.ucla.edu/dataset.xhtml;jsessionid=5f982d0cf8234478939c09ae6932?persistentId=doi:10.25346/S6/EEFYIP). No data was modified.

File: [Gates_Report_02062020.csv](Gates_Report_02062020.csv)

An additional table provided by the Gates Foundation, providing DOIs which are missing in the first file. Some columns were removed during CSV export to protect potentially sensitive author data.

### Preprocessed

File: [Gates_Open_Access_Publishing_Charges_Project_Data_preprocessed.csv](Gates_Open_Access_Publishing_Charges_Project_Data_preprocessed.csv)

This is a modified variant of the first original file, with the aim to make it compatible with the OpenAPC enrichment scripts. The following tasks were carried out:

- An "institution" column was added, default value "Bill & Melinda Gates Foundation" for all entries.
- An "is_hybrid" column was added, but initially left empty (determining the journals' hybrid status was postponed to after enrichment, see below)
- A "doi" column was added, its value imported from the supplement table via the "PublicationID" key.
- A "period" column was added, its value set to the year component of the date in "Date Payment Completed"
- An "euro" column was added. To determine its value, an exchange rate was obtained by looking up the values in "Date Payment Completed" and "Currency" in the [statistical data warehouse of the European Central Bank](https://sdw.ecb.europa.eu/) (The ECB keeps records on historical exchange rates between Euro and all other major currencies on a daily basis). The value in "APC" was then divided by this exchange rate.
- All columns not relevant to the preprocessing or enrichment were removed. This included all other columns containing data on additional expenditures like "Color Charg" \[sic\] or "Page Charge" as those components are not part of an APC as per OpenAPC's [definition](https://github.com/OpenAPC/openapc-de/wiki/Data-Submission-Handout#definition-of-costs).
- Articles without a DOI or with a value of 0 in the "APC" column were removed (A line of empty values was inserted in place to keep line numbers between all processed files in sync)

All steps described above were carried out by a [python preprocessing script](../../python/etc/preprocessing/gates_foundation/gates_foundation_preprocessing.py), its log output can be viewed [here](../../python/etc/preprocessing/gates_foundation/log.txt). 

### Enriched

File: [Gates_Open_Access_Publishing_Charges_Project_Data_enriched.csv](Gates_Open_Access_Publishing_Charges_Project_Data_enriched.csv)

This is the resulting file after runnning the OpenAPC enrichment scripts. Some more entries were dropped during this process if Crossref reported an incompatible publication type (OpenAPC only aggregates journal articles, so records belonging to types like data sets, conference papers or book chapters were removed).


### Postprocessed

File: [Gates_Open_Access_Publishing_Charges_Project_Data_postprocessed.csv](Gates_Open_Access_Publishing_Charges_Project_Data_postprocessed.csv)

The final, OpenAPC-compatible version. Two last steps had to be performed on the enriched file:

- The original data did not include information on the hybrid status of the journal an article had been published in, which is mandatory for OpenAPC (there's a column "Open Access Status" in the supplement table, but we found it to be inaccurate in many cases). We solved this issue by importing the hybrid status from different sources (OpenAPC's own core data and TA data files and the remaining ones from [journalTOCs](http://www.journaltocs.hw.ac.uk/)). Only a small number of journals had to be looked up manually.
- Some duplicates in the data had to cleared, as each DOI may only appear once in the OpenAPC data set. In most of these cases both affected lines had to be deleted, as we could not tell which one was correct in case of different APC values.

### Statistics

Entries in original file: 3552

| Reason for deletion                                                 | Count        |
|:--------------------------------------------------------------------|-------------:|
|No DOI found                                                         |   - 101      |
|Invalid DOI                                                          |   - 7        |
|APC value of 0                                                       |   - 163      |
|Incompatible publication type (conference paper)                     |   - 10       |
|Incompatible publication type (book or book chapter)                 |   - 3        |
|Incompatible publication type (posted content)                       |   - 1        |
|Incompatible publication type (data set)                             |   - 1        |
|Duplicates removed                                                   |   - 26       |

Entries remaining after postprocessing: 3240

