


## About 

The aim of this repository is:

- to release datasets on fees paid for Open Access journal articles by German Universities under an Open Database License
- to share a copy of [Directory of Open Access Journals (DOAJ)](http://doaj.org/) journal master list (downloaded January 2014)
- to demonstrate how reporting on fee-based Open Access publishing can be made more transparent and reproducible across institutions.

## Participating Universities

So far, the following German universities have agreed to share information on paid author processing charges (APC):

- [Bayreuth University](http://www.ub.uni-bayreuth.de/en/digitale_bibliothek/open_access/index.html)
- [Bielefeld University](http://oa.uni-bielefeld.de/publikationsfonds.html)
- [Clausthal University of Technology](http://www.ub.tu-clausthal.de/en/angebote-fuer-wissenschaftlerinnen/elektronisches-publizieren/publikationsfonds/)
- [Hamburg University of Technology](https://www.tub.tu-harburg.de/publizieren/openaccess/)
- [Heidelberg University](http://www.ub.uni-heidelberg.de/Englisch/service/openaccess/publikationsfonds.html)
- [Leibniz Universität Hannover](http://tib.uni-hannover.de/oafonds)
- [Leipzig University](https://www.ub.uni-leipzig.de/open-access/publikationsfonds/)
- [Ludwig-Maximilians-Universität München](http://www.en.ub.uni-muenchen.de/writing/open-access-publishing/funding/index.html)
- [Free University of Berlin](http://www.fu-berlin.de/sites/open_access/dienstleistungen/artikelgebuehren/publikationsfonds/index.html)
- [KIT Karlsruhe](http://www.bibliothek.kit.edu/cms/kit-publikationsfonds.php)
- [University of Bamberg](http://www.uni-bamberg.de/en/ub/publishing/open-access-publishing/open-access-funds/)
- [University of Duisburg-Essen](https://www.uni-due.de/ub/open_access.shtml)
- [University of Göttingen](http://www.sub.uni-goettingen.de/en/electronic-publishing/open-access/open-access-publication-funding/)
- [University of Konstanz](http://www.ub.uni-konstanz.de/openaccess/open-access-publikationsfonds-der-universitaet-konstanz/)
- [University of Regensburg](http://oa.uni-regensburg.de/)

## Participating Research Society Funds in Germany

Dataset on funds that are supported by research societies under its Open-Access Publishing Programme.

Participating Research Organizations:

- [Max Planck Digital Library](http://www.mpdl.mpg.de/21-specials/50-open-access-publishing.html)

The data content covers APCs as paid for by our central budget for the Max Planck Society.  APCs funded locally by Max Planck Institutes are not part of this data set.  The Max Planck Society has a limited input tax reduction. The refund of input VAT for APC is 20%.

- [Forschungszentrum Jülich](http://www.fz-juelich.de/portal/DE/Home/home_node.html)
- [Library Wissenschaftspark Albert Einstein](http://bib.telegrafenberg.de/en/library-wissenschaftspark-albert-einstein/)

## Dataset



At the moment, the dataset releases information on 2 557 articles, with total expenditure of 3 155 129€. Average fee is 1 233.9€.

View dataset on [GitHub](https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de.csv).


|                 | Articles| Fees paid in EURO| Mean Fee paid|
|:----------------|--------:|-----------------:|-------------:|
|Bamberg U        |       16|             15932|           996|
|Bayreuth U       |       57|             64519|          1132|
|Bielefeld U      |      160|            187296|          1171|
|Duisburg-Essen U |      114|            130989|          1149|
|FU Berlin        |       45|             56074|          1246|
|FZJ - ZB         |       76|             90411|          1190|
|GFZ-Potsdam      |       60|             69625|          1160|
|Goettingen U     |      126|            159186|          1263|
|Hamburg TUHH     |       10|             11911|          1191|
|Hannover U       |       50|             63908|          1278|
|Heidelberg U     |       83|            112238|          1352|
|KIT              |      296|            350114|          1183|
|Konstanz U       |       85|            107776|          1268|
|Leipzig U        |       60|             79603|          1327|
|MPG              |     1046|           1315614|          1258|
|Muenchen LMU     |      106|            153553|          1449|
|Regensburg U     |      163|            182610|          1120|
|TU Clausthal     |        4|              3771|           943|

## Use of external sources

Externals sourced were used to compile the dataset in order to provide shared identifiers for publications (e.g. PMID) and disambiguated information on publishers and journals.



|Source     |variable  |description                     |
|:--------------|:---------|:-----------------------------------------------|
|CrossRef   |`publisher` |Title of Publisher             |
|CrossRef   |`journal_full_title` |Full Title of Journal  |
|CrossRef   |`issn` |International Standard Serial Numbers (collapsed) |
|CrossRef   |`issn_print` |ISSN print |
|CrossRef   |`issn_electronic`  |ISSN electronic        |
|CrossRef   |`license_ref`  |License of the article     |
|CrossRef   |`indexed_in_CrossRef`  |Is the article metadata registered with CrossRef? (logical)    |
|EuropePMC    |`pmid`  |PubMed ID                 |
|EuropePMC    |`pmcid` |PubMed Central ID         |
|Web of Science |`ut` |Web of Science record ID             |
|DOAJ           |`DOAJ` |Is the journal indexed in the DOAJ? (logical)    |

## Sample Visualisations

### Distribution over publishers by university



![](figure/plotPublisherAPC.png)

### Comparing fees paid by university and research institution



![](figure/boxplot_institution.png)

### Average fees paid by publisher



![](figure/plotAverageAPC.png)

### Average fees Max Planck Digital Library paid for Springer Open Access articles by year



![](figure/plotAverageSpringerMPDL.png)

For more examples see also [http://openapc.github.io/openapc-de/](http://openapc.github.io/openapc-de/)

## How to contribute?

In collaboration with the [DINI working group Electronic Publishing](http://dini.de/ag/e-pub1/), a [wiki page](https://github.com/OpenAPC/openapc-de/wiki/Handreichung-Dateneingabe)(in German) explains all the steps required. Meeting and telephone conferences are documented as well:

* [Virtual Meeting 19 August](https://github.com/OpenAPC/openapc-de/wiki/Protokoll-Kick-Off-19.-August)
* [Virtual Meeting 11 + 12 February 2015](https://github.com/OpenAPC/openapc-de/wiki/Ergebnisprotokoll-11-bzw.-12.-Februar-2015)

## Licence

The datasets are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/ 

This work is licensed under the Creative Commons Attribution 4.0 Unported License.

## How to cite?

Bielefeld University Library archives a remote including version history. To cite:

Apel, Jochen; Bertelmann, Roland; Beucke, Daniel; Deinzer, Gernot; Dorner, Andrea; Engelhardt, Clemens; Herb, Ulrich; Feldsien-Sudhaus, Inken; Franke, Fabian; Frick, Claudia; Geschuhn, Kai Karin; Jaeger, Doris;  Lützenkirchen, Frank; Kroiss, Stephanie; Oberländer, Anja; 
Peil, Vitali; Pieper, Dirk; Schlachter, Michael; Schlegel, Birgit; Sikora, Adriana; Tullney, Marco; Vieler, Astrid; Witt, Sabine; Jahn, Najko; (2014 -): *Datasets on fee-based Open Access publishing across German Institutions*. Bielefeld University. [10.4119/UNIBI/UB.2014.18](http://dx.doi.org/10.4119/UNIBI/UB.2014.18)

## Acknowledgement

This project follows [Wellcome Trust example to share data on paid APCs](http://blog.wellcome.ac.uk/2014/03/28/the-cost-of-open-access-publishing-a-progress-report/). It recognises efforts from [JISC](https://www.jisc-collections.ac.uk/News/Releasing-open-data-about-Total-Cost-of-Ownership/) and the [ESAC initative](http://esac-initiative.org/) to standardise APC reporting. 

For data enrichment, sample visualisations and explorations we build on the work of [rOpenSci](http://ropensci.org/) and [LibreCat/Catmandu](http://librecat.org/).

## Contributors

Jochen Apel, Roland Bertelmann, Daniel Beucke, Gernot Deinzer, Andrea Dorner,  Clemens Engelhardt, Ulrich Herb, Inken Feldsien-Sudhaus, Fabian Franke, Claudia Frick, Kai Karin Geschuhn, Doris Jaeger, Stephanie Kroiss, Frank Lützenkirchen, Anja Oberländer, Vitali Peil, Dirk Pieper, Michael Schlachter, Birgit Schlegel, Adriana Sikora, Marco Tullney, Astrid Vieler, Sabine Witt, Najko Jahn

## Contact

For bugs, feature requests and other issues, please submit an issue via [Github](https://github.com/OpenAPC/openapc-de/issues/new).

For general comments, email najko.jahn at uni-bielefeld.de and dirk.pieper at uni-bielefeld.de
