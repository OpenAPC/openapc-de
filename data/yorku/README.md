# About

This is data from the York University Libraries Open Access Author Fund.  It covers fiscal years 2009--2018.

# Source

Original data source: [YorkU OA Fund_May 2018.xlsx](https://yorkspace.library.yorku.ca/xmlui/bitstream/handle/10315/27524/YorkU%20OA%20Fund_May%202018.xlsx) from [Dataset: York University Libraries Open Access Author Fund](https://yorkspace.library.yorku.ca/xmlui/handle/10315/27524).

# Processing

Steps taken to clean the data, by editing it in Org in Emacs, then exporting it with R:

+ columns moved, renamed, added and deleted to meet requirements
+ "period" simplified from the original date field, so it is just the year
+ "cost" and "currency" columns used to hold costs until "euros" column can be filled in
+ minor cleanup: DOIs standardized, some journal titles and publisher names expanded and standardized
+ removed an open access book
+ removed articles where the cost was 0
* removed a 2013 *BMC Public Health* article (1970 USD) where no DOI is known

# TO DO

* Convert costs from CAD or USD to EUR.  (A very few are in EUR already, but most are USD.)

# Contact

For this data in this repo: William Denton <wdenton@yorku.ca>.  Generally for open access at York: associate dean Andrea Kosavic <akosavic@yorku.ca>.
