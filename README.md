## About 

The aim of this repository is:

- to release datasets on fees paid for Open Access journal articles by German Universities under an Open Database License
- to share a copy of [Directory of Open Access Journals (DOAJ)](http://doaj.org/) journal master list (downloaded January 2014)
- to demonstrate how reporting on fee-based Open Access publishing can be made more transparent and reproducible across institutions.

## Participating Universities

So far, the following German universities have agreed to share information on paid author processing charges (APC):

- [Bielefeld University](http://oa.uni-bielefeld.de/publikationsfonds.html)
- [Clausthal University of Technology](http://www.ub.tu-clausthal.de/en/angebote-fuer-wissenschaftlerinnen/elektronisches-publizieren/publikationsfonds/)
- [Leibniz Universität Hannover](http://tib.uni-hannover.de/oafonds)
- [Leipzig University](https://www.ub.uni-leipzig.de/open-access/publikationsfonds/)
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

- [Forschungszentrum Jülich](http://www.fz-juelich.de/portal/DE/Home/home_node.html)

## Dataset

At the moment, the dataset releases information on 1.599 articles, with total expenditure of 1.938.505 EURO.

View dataset on [GitHub](https://github.com/njahn82/unibiAPC/blob/master/data/apc_de.csv).


|                 | Articles| Fees paid in EURO| Mean Fee paid|
|:----------------|--------:|-----------------:|-------------:|
|Bielefeld U      |      159|         186096.22|       1170.42|
|Duisburg-Essen U |      106|         120575.00|       1137.50|
|FZJ - ZB         |       76|          90410.94|       1189.62|
|Hannover U       |       42|          53305.10|       1269.17|
|KIT              |      194|         228626.36|       1178.49|
|Konstanz U       |       85|         107776.13|       1267.95|
|Leipzig U        |       60|          79602.89|       1326.71|
|MPG              |      710|         885731.68|       1247.51|
|Regensburg U     |      163|         182609.56|       1120.30|
|TU Clausthal     |        4|           3770.77|        942.69|


## Sample Visualisations

### Distribution over publishers by university



![](figure/plotPublisherAPC.png)

### Comparing fees paid by univeristy and research institution



![](figure/boxplot_institution.png)

### Average fees paid by publisher



![](figure/plotAverageAPC.png)

### Average fees Max Planck Digital Library paid for Springer Open Access articles by year



![](figure/plotAverageSpringerMPDL.png)

For more examples see also [http://njahn82.github.io/unibiAPC/](http://njahn82.github.io/unibiAPC/)

## How to contribute?

In collaboration with the [DINI working group Electronic Publishing](http://dini.de/ag/e-pub1/), a [wiki page](https://github.com/njahn82/unibiAPC/wiki/Handreichung-Dateneingabe)(in German) explains all the steps required. Meeting and telephone conferences are documented as well:

* [Virtual Meeting 19 August](https://github.com/njahn82/unibiAPC/wiki/Protokoll-Kick-Off-19.-August)

## Licence

The datasets are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/ 

This work is licensed under the Creative Commons Attribution 4.0 Unported License.

## How to cite?

Bielefeld University Library archives a remote including version history. To cite:

Deinzer, Gernot; Herb, Ulrich; Frick, Claudia; Geschuhn, Kai Karin; Jaeger, Doris;  Lützenkirchen, Frank; Oberländer, Anja; 
Peil, Vitali; Pieper, Dirk; Schlachter, Michael; Sikora, Adriana; Tullney, Marco; Vieler, Astrid; Jahn, Najko; (2014): *Datasets on fee-based Open Access publishing across German Institutions*. Bielefeld University. [10.4119/UNIBI/UB.2014.18](http://dx.doi.org/10.4119/UNIBI/UB.2014.18)

## Acknowledgement

This project follows [Wellcome Trust example to share data on paid APCs](http://blog.wellcome.ac.uk/2014/03/28/the-cost-of-open-access-publishing-a-progress-report/). It recognises efforts from [JISC](https://www.jisc-collections.ac.uk/News/Releasing-open-data-about-Total-Cost-of-Ownership/) and the [ESAC initative](http://esac-initiative.org/) to standardise APC reporting. 

For data enrichment, sample visualisations and explorations we build on the work of [rOpenSci](http://ropensci.org/) and [LibreCat/Catmandu](http://librecat.org/).

## Contributors

Gernot Deinzer, Ulrich Herb, Claudia Frick, Kai Karin Geschuhn, Doris Jaeger, Frank Lützenkirchen, Anja Oberländer, Vitali Peil, Dirk Pieper, Michael Schlachter, Adriana Sikora, Marco Tullney, Astrid Vieler, Najko Jahn

## Contact

For bugs, feature requests and other issues, please submit an issue via Github.

For general comments, email najko.jahn at uni-bielefeld.de and dirk.pieper at uni-bielefeld.de
