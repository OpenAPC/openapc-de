## About 

The aim of this repository is:

- to share a copy of [Directory of Open Access Journals (DOAJ)](http://doaj.org/) journal master list (downloaded January 2014) -> [data/doajJournalList.csv](data/doajJournalList.csv)
- to release a [Bielefeld University](http://www.uni-bielefeld.de/) Paid APCs 2012/13 Dataset under an Open Database License -> [data/unibi12-13.csv](data/unibi12-13.csv)
- to demonstrate how reporting on fee-based Open Access publishing can be made more transparent and reproducible

This documentation is written in Markdown and embeds source code written in [R](http://www.r-project.org/).

You can run ```knit()``` to reproduce this file

```
require(knitr)
knit(README.Rmd) 
```

## DOAJ

The current [DOAJ journal master list](http://doaj.org/faq#metadata) that can be downloaded as `csv` lacks information on the applicability of author processing charges (APC). Answering [Ulrich Herb's](https://twitter.com/scinoptica) concerns in [The prevalence of Open Access publication fees](http://www.scinoptica.com/pages/topics/the-prevalence-of-open-access-publication-fees.php), we decided to share our DOAJ copy that we used at [Bielefeld University Library](http://www.ub.uni-bielefeld.de/) for reporting Open Access Gold publications at Bielefeld University as part of the [DFG Open-Access Publishing Programme](http://www.dfg.de/en/research_funding/programmes/infrastructure/lis/funding_opportunities/open_access_publishing/index.html) in January 2014.

### Load DOAJ journal master list


```r
doaj <- read.csv("data/doajJournalList.csv", header = TRUE, sep =",")
```
This master list contains


```r
length(unique(doaj$ISSN))
```

```
## [1] 9804
```
registered Open Access journals. It provides information on


```r
colnames(doaj)
```

```
##  [1] "X"                   "Title"               "Title.Alternative"  
##  [4] "Identifier"          "Publisher"           "Language"           
##  [7] "ISSN"                "EISSN"               "Keyword"            
## [10] "Start.Year"          "End.Year"            "Added.on.date"      
## [13] "Subjects"            "Country"             "Publication.fee"    
## [16] "Further.Information" "CC.License"          "Content.in.DOAJ"
```

### A closer look on APCs

This table summarises whether a journal requires APCs or not:


```r
apc.table <- data.frame(table(unlist(doaj$Publication.fee)))
apc.table$Perc <- apc.table$Freq / sum(apc.table$Freq) * 100
colnames(apc.table) <-c("Fee", "Journals", "Share")

knitr::kable(apc.table[order(apc.table$Journals, decreasing = T),], row.names = FALSE, digits = 2)
```



|Fee | Journals| Share|
|:---|--------:|-----:|
|N   |     6547| 66.78|
|Y   |     2583| 26.35|
|CON |      523|  5.33|
|NY  |      148|  1.51|
|    |        3|  0.03|

You may also wish to explore the growth of DOAJ by APC applicability.


```r
#exclude journals with blank APC info
doaj <- doaj[!doaj$Publication.fee == "",]
doaj <- droplevels(doaj)

# transform to date object
doaj$Added.on.date <- as.Date(doaj$Added.on.date, format="%Y-%m-%d")

# relevel
doaj$Publication.fee <- factor (doaj$Publication.fee, 
                             levels = c(rownames(data.frame(rev(sort(table(doaj$Publication.fee)))))))

#prepare df for ggplotting
tt <- data.frame(table(doaj$Publication.fee, doaj$Added.on.date))
tt$Cumsum<-ave(tt$Freq,tt$Var1,FUN=cumsum) 

#plot

ggplot2::ggplot(tt, aes(as.Date(Var2),Cumsum, group = Var1)) + 
geom_line(aes(colour = Var1, show_guide=FALSE)) +
xlab("Date added to DOAJ") + ylab("Cumulative Sum") + 
scale_colour_brewer("Publication Fee",palette=2, type="qual") +
theme_bw(base_size= 16) +
opts(legend.key=theme_rect(fill="white",colour="white"))
```

```
## Error: konnte Funktion "aes" nicht finden
```

 This little exploration demonstrates that the DOAJ journal title master list is an excellent source (not only) to study the longitudinal growth of Open Access journal publishing. As we have shown, by reusing such a file, you can also write your study in a reproducible manner.

We hope that the DOAJ will continue its bulk download service in order to provide an convenient way to monitor Open Access journal publishing.  At Bielefeld University Library, for instance, we use the `csv` download to answer our DFG reporting requirements. 

## Bielefeld University Paid APCs 2012/13 Dataset

With the [Bielefeld University Paid APCs 2012/13 Dataset](data/unibi12-13.csv), we publish information on paid Article Processing Charges (APC) by the [Open Access Publication Fund of Bielefeld University](http://oa.uni-bielefeld.de/publikationsfonds.html). The fund is supported by the German Research Foundation (DFG) under its [Open-Access Publishing Programme](http://www.dfg.de/en/research_funding/programmes/infrastructure/lis/funding_opportunities/open_access_publishing/index.html).


### Load Data


```r
my.df <- read.csv("data/unibi12-13.csv", header = TRUE, sep =",")
head(my.df)
```

```
##     PUBID EURO Period
## 1 2465755  961   2012
## 2 2515416 1037   2012
## 3 2603025 1724   2013
## 4 2533638  142   2012
## 5 2510371  900   2012
## 6 2530855 1600   2012
##                                                     Publisher
## 1 Association for Research in Vision and Ophthalmology (ARVO)
## 2 Association for Research in Vision and Ophthalmology (ARVO)
## 3 Association for Research in Vision and Ophthalmology (ARVO)
## 4                                                 Elsevier BV
## 5                                          Frontiers Media SA
## 6                                          Frontiers Media SA
##                                            Journal
## 1                                Journal of Vision
## 2                                Journal of Vision
## 3                                Journal of Vision
## 4                                             CSBJ
## 5 Frontiers in Cellular and Infection Microbiology
## 6                     Frontiers in Neural Circuits
##                        doi    issn.1 issn.2
## 1           10.1167/12.2.8 1534-7362   <NA>
## 2           10.1167/12.5.7 1534-7362   <NA>
## 3           10.1167/13.7.7 1534-7362   <NA>
## 4   10.5936/csbj.201210004 2001-0370   <NA>
## 5 10.3389/fcimb.2012.00070 2235-2988   <NA>
## 6 10.3389/fncir.2012.00072 1662-5110   <NA>
```

The dataset covers the accounting periods 2012 and 2013 (`Period`). For every single article,  the `doi` is provided. Journal titles (`Journal`), publisher names (`Publisher`) and the International Standard Serial Numbers (`issn.1` and `issn.2`) are normalized according to CrossRef metadata store. In addition, `PUBID` references the copy stored in the institutional repository [PUB - Publications at Bielefeld University](http://pub.uni-bielefeld.de/en).

With this step, we follow Wellcome Trust example to share data on paid APCs. See:

Neylon, Cameron (2014): Wellcome Trust Article Processing Charges by Article 2012/13.
[https://github.com/cameronneylon/apcs](https://github.com/cameronneylon/apcs)


### Paid APCs

Column `EURO` contains the author processing charge  for each paper including VAT. 

In total, we paid


```r
sum(my.df$EURO)
```

```
## [1] 109567
```

for 

```r
nrow(my.df)
```

```
## [1] 93
```
articles.


DFG funding covered 75%.


```r
sum(my.df$EURO) * 0.75
```

```
## [1] 82175
```

#### APC per accounting period

Column `EURO` contains the author processing charge paid for each paper in Euro including VAT. 

To obtain the yearly costs for 2012 and 2013:


```r
tapply(my.df$EURO, my.df$Period, sum)
```

```
##  2012  2013 
## 41726 67841
```


#### APC per Publisher 

To calculate APC paid per publisher and accounting period  and print it as pretty markdown table:


```r
# relevel publishers according to sorting
my.df$Publisher <- factor (my.df$Publisher, 
                             levels = c(rownames(data.frame(rev(sort(table(my.df$Publisher)))))))

# calculate and print
knitr::kable(tapply(my.df$EURO, list(my.df$Publisher, my.df$Period), sum))
```



|                                                            |  2012|  2013|
|:-----------------------------------------------------------|-----:|-----:|
|Springer Science + Business Media                           | 22540| 20362|
|Frontiers Media SA                                          |  7300| 20109|
|Public Library of Science (PLoS)                            |  3809| 19462|
|MDPI AG                                                     |  1976|  1175|
|Wiley-Blackwell                                             |  1333|  2914|
|Hindawi Publishing Corporation                              |   850|  1078|
|Association for Research in Vision and Ophthalmology (ARVO) |  1998|  1724|
|Scientific Research Publishing, Inc,                        |   732|    NA|
|Nature Publishing Group                                     |  1046|    NA|
|Informa UK Limited                                          |    NA|  1017|
|Elsevier BV                                                 |   142|    NA|

Mean APCs paid:


```r
knitr::kable(tapply(my.df$EURO, list(my.df$Publisher, my.df$Period), mean))
```



|                                                            |   2012|   2013|
|:-----------------------------------------------------------|------:|------:|
|Springer Science + Business Media                           | 1408.8| 1197.8|
|Frontiers Media SA                                          | 1042.9| 1256.8|
|Public Library of Science (PLoS)                            |  952.2| 1216.4|
|MDPI AG                                                     |  658.7| 1175.0|
|Wiley-Blackwell                                             | 1333.0| 1457.0|
|Hindawi Publishing Corporation                              |  425.0| 1078.0|
|Association for Research in Vision and Ophthalmology (ARVO) |  999.0| 1724.0|
|Scientific Research Publishing, Inc,                        |  732.0|     NA|
|Nature Publishing Group                                     | 1046.0|     NA|
|Informa UK Limited                                          |     NA| 1017.0|
|Elsevier BV                                                 |  142.0|     NA|

### Licence

The Bielefeld University Paid APCs 2012/13 Dataset is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/ 

### Contact

Najko Jahn < najko.jahn [ at ] uni-bielefeld.de >

Dirk Pieper < dirk.pieper [ at ] uni-bielefeld.de >
