## About 

The aim of this repository is:

- to release datasets on fees paid for Open Access journal articles by German Universities under an Open Database License
- to share a copy of [Directory of Open Access Journals (DOAJ)](http://doaj.org/) journal master list (downloaded January 2014) -> [data/doaj/doajJournalList.csv](data/doajJournalList.csv)
- to demonstrate how reporting on fee-based Open Access publishing can be made more transparent and reproducible across institutions.

## Dataset

At the moment, the dataset releases information on 1.432 articles, with total expenditure of 1.732.556 EURO.

View dataset on [GitHub](https://github.com/njahn82/unibiAPC/blob/master/data/apc_de.csv).

## Participating Universities

So far, the following German universities have agreed to share information on paid author processing charges (APC):

- [Bielefeld University](http://oa.uni-bielefeld.de/publikationsfonds.html)
- [Leibniz Universität Hannover](http://tib.uni-hannover.de/oafonds)
- [KIT Karlsruhe](http://www.bibliothek.kit.edu/cms/kit-publikationsfonds.php)*
- [University of Duisburg-Essen](https://www.uni-due.de/ub/open_access.shtml)
- [University of Konstanz](http://www.ub.uni-konstanz.de/openaccess/open-access-publikationsfonds-der-universitaet-konstanz/)
- [University of Regensburg](http://oa.uni-regensburg.de/)

* (KIT omitted DOI due to privacy concerns)

## Participating Research Society Funds in Germany

Dataset on funds that are supported by research societies under its Open-Access Publishing Programme.

Participating Research Organizations:

- [Max Planck Digital Library](http://www.mpdl.mpg.de/21-specials/50-open-access-publishing.html)

The data content covers APCs as paid for by our central budget for the Max Planck Society.  APCs funded locally by Max Planck Institutes are not part of this data set.  The Max Planck Society has a limited input tax reduction. The refund of input VAT for APC is 20%.

## Sample Visualisations

### Distribution over publishers by university


```
## Loading required package: ggplot2
## Loading required package: methods
## Loading required package: wesanderson
```

![](figure/plotPublisherAPC.png)


### Average fees paid by publisher



![](figure/plotAverageAPC.png)

### Average fees Max Planck Digital Library paid for Springer Open Access articles by year



![](figure/plotAverageSpringerMPDL.png)

For more exapmles see also [http://njahn82.github.io/unibiAPC/](http://njahn82.github.io/unibiAPC/)

## How to contribute?

In collaboration with the [DINI working group Electronic Publishing](http://dini.de/ag/e-pub1/), a [wiki page](https://github.com/njahn82/unibiAPC/wiki/Handreichung-Dateneingabe)(in German) explains all the steps required. Meeting and telephone conferences are documented as well:

* [Virtual Meeting 19 August](https://github.com/njahn82/unibiAPC/wiki/Protokoll-Kick-Off-19.-August)

## Licence

The datasets are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/ 

This work is licensed under the Creative Commons Attribution 4.0 Unported License.

## How to cite?

Bielefeld University Library archives a remote including version history. To cite:

Deinzer, Gernot; Herb, Ulrich; Lützenkirchen, Frank;
Peil, Vitali; Pieper, Dirk; Tullney, Marco; Jahn, Najko; (2014): *Datasets on fee-based Open Access publishing across German Institutions*. Bielefeld University. [10.4119/UNIBI/UB.2014.18](http://dx.doi.org/10.4119/UNIBI/UB.2014.18)

## Acknowledgement

This project follows [Wellcome Trust example to share data on paid APCs](http://blog.wellcome.ac.uk/2014/03/28/the-cost-of-open-access-publishing-a-progress-report/). It recognises efforts from [JISC](https://www.jisc-collections.ac.uk/News/Releasing-open-data-about-Total-Cost-of-Ownership/) and the [ESAC initative](http://esac-initiative.org/) to standardise APC reporting. 

For data enrichment, sample visualisations and explorations we build on the work of [rOpenSci](http://ropensci.org/) and [LibreCat/Catmandu](http://librecat.org/).

## Contributors

Gernot Deinzer, Ulrich Herb, Kai Karin Geschuhn, Doris Jaeger, Frank Lützenkirchen, Vitali Peil, Dirk Pieper, Adriana Sikora, Marco Tullney, Najko Jahn

## Contact

For bugs, feature requests and other issues, please submit an issue via Github.

For general comments, email najko.jahn at uni-bielefeld.de and dirk.pieper at uni-bielefeld.de
