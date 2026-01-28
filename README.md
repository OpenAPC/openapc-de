






## About

The aim of this repository is:

- to release data sets on fees paid for Open Access journal articles and monographs by Universities and Research Society Funds under an Open Database License
- to demonstrate how reporting on fee-based Open Access publishing can be made more transparent and reproducible across institutions.

At the moment this project provides the following cost data:

| Publication Type | Count           | Aggregated Sum (€)      | Contributing Institutions              |
|------------------|-----------------|-------------------------|----------------------------------------|
| Articles         |261,097 | 535,264,785    | 481 |
| Monographs       |2,355 | 15,596,693    | 102 |

## How to access the data?

There are several options. You may simply download the the raw data sets in CSV format, query our [OLAP server](https://github.com/OpenAPC/openapc-olap/blob/master/HOWTO.md) or use our [Treemap site](https://treemaps.openapc.net/) for visual data exploration.

| Dataset         | CSV File                                                                                                                                                                                                                         | OLAP Cube                                                                     | Treemap                                                                       |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| articles        | [APC file](https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de.csv), [data schema](https://github.com/OpenAPC/openapc-de/wiki/schema#openapc-data-set)                                                                 | [APC cube](https://olap.openapc.net/cube/openapc/aggregate)                   | [APC treemap](https://treemaps.openapc.net/apcdata/openapc/)                  |
| TA articles     | [TA file](https://github.com/OpenAPC/openapc-de/blob/master/data/transformative_agreements/transformative_agreements.csv), [data schema](https://github.com/OpenAPC/openapc-de/wiki/schema#transformative-agreements-data-set)   | [TA cube](https://olap.openapc.net/cube/transformative_agreements/aggregate)  | [TA treemap](https://treemaps.openapc.net/apcdata/transformative-agreements/) |
| monographs      | [BPC file](https://github.com/OpenAPC/openapc-de/blob/master/data/bpc.csv), [data schema](https://github.com/OpenAPC/openapc-de/wiki/schema#bpc-data-set)                                                                        | [BPC cube](https://olap.openapc.net/cube/bpc/aggregate)                       | [BPC treemap](https://treemaps.openapc.net/apcdata/bpc/)                      |

Our latest data release can always be accessed via the following DOI:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6883472.svg)](https://doi.org/10.5281/zenodo.6883472)

## Additional Costs

In 2024 OpenAPC started to aggregate additional costs like page charges or submission fees, which may occur in the context of OA publishing aside from APCs. These cost types are considered optional and thus collected in a separate data file, they are linked to a main publication entry using the DOI as primary key. At the moment additional costs are only collected for journal articles.

| Dataset         | Main CSV File                                                                 | Additional Costs File                                                                                       | OLAP Cube                                                             | Treemap                                                                           |
|-----------------|-------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| articles        | [APC file](https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de.csv) | [APC additional costs](https://github.com/OpenAPC/openapc-de/blob/master/data/apc_de_additional_costs.csv)  | [APC_AC cube](https://olap.openapc.net/cube/openapc_ac/aggregate)     | [APC_AC Treemap](https://treemaps.openapc.net/apcdata/openapc/additional_costs)   |

## How to contribute?

Any academic institution or research funder paying for Article Process Charges (APCs) or Book Processing Charges (BPCs) can contribute to OpenAPC, no formal registration is required.
This [page](https://github.com/OpenAPC/openapc-de/wiki/Data-Submission-Handout) ([German version](https://github.com/OpenAPC/openapc-de/wiki/Handreichung-Dateneingabe)) explains the details.

Please note that OpenAPC uses internal identifiers for institutions in all its data sets to maintain backwards compatibility. Additional metadata on all participants (including ROR IDs as persistent identifier) is maintained in a separate [lookup table](https://github.com/OpenAPC/openapc-de/blob/master/data/institutions.csv).

The following institutions have contributed to OpenAPC so far:

## Institutions from Germany 

<details>

###  Higher education institutions 

- [Aachen University of Applied Sciences](https://www.fh-aachen.de/fh-aachen/arbeiten/servicestellen-fuer-beschaeftigte/bibliotheksservices-fuer-beschaeftigte/forschen-publizieren/publikationsfonds-forschung)
- [Alice Salomon Hochschule Berlin](https://www.ash-berlin.eu/studium/einrichtungen-fuer-studierende/bibliothek/open-access/#c29181)
- [Bamberg University](https://www.uni-bamberg.de/en/library/publishing/oa-publishing/)
- [Bauhaus-Universität Weimar](https://www.uni-weimar.de/en/university/structure/central-university-facilities/university-library/research/open-access/open-access-publication-fund/)
- [Bayreuth University](http://www.ub.uni-bayreuth.de/en/digitale_bibliothek/open_access/index.html)
- [Bergische Universität Wuppertal](https://www.bib.uni-wuppertal.de/de/forschen/open-access/publikationsfonds/)
- [Bielefeld University](http://oa.uni-bielefeld.de/publikationsfonds.html)
- [Brandenburg University of Technology Cottbus-Senftenberg](https://www.b-tu.de/en/)
- [Carl von Ossietzky Universität Oldenburg](https://uol.de/en/bis/research-publishing/open-access/open-access-publication-fund)
- [Catholic University of Eichstätt-Ingolstadt](https://www.ku.de/bibliothek/forschen-und-publizieren/open-access)
- [Charité - Universitätsmedizin Berlin](https://bibliothek.charite.de/publizieren/open_access)
- [Christian-Albrechts-Universität zu Kiel](https://www.ub.uni-kiel.de/de/publizieren/open-access-finanzierung)
- [Clausthal University of Technology](https://www.ub.tu-clausthal.de/publizieren-open-access/open-access-publizieren/publikationsfonds)
- [Darmstadt University of Applied Sciences](https://h-da.de/en/)
- [Eberhard Karls Universität Tübingen](https://uni-tuebingen.de/en/facilities/university-library/publishing-research/publishing/open-access-publication-fund/)
- [Fachhochschule Südwestfalen](https://www.fh-swf.de/de/studierende/rund_ums_studium/bibliothek_1/publikationsdienstleistungen/publikationsdienstleistungen.php#absatz_container_oa_fh)
- [Freie Universität Berlin](https://www.fu-berlin.de/sites/open_access/finanzierung-oa/zeitschriftenartikel/publikationsfonds_zeitschriften/index.html)
- [Friedrich-Alexander-Universität Erlangen-Nürnberg](https://ub.fau.de/schreiben-publizieren/open-access/dfg-gefoerderter-publikationsfonds/)
- [Friedrich-Schiller-Universität Jena](https://www.thulb.uni-jena.de/services/forschung-/-lehre/open-access-/-elektronisches-publizieren#c3516)
- [Fulda University of Applied Sciences](https://www.hs-fulda.de/en/)
- [HAWK Hochschule für angewandte Wissenschaft und Kunst Hildesheim/Holzminden/Göttingen](https://www.hawk.de/de/hochschule/organisation-und-personen/zentrale-einrichtungen/zentrum-fuer-information-medien-und-technologie/bibliothek/openaccess)
- [HafenCity Universität Hamburg](https://www.hcu-hamburg.de/en/library/writing-publishing/open-access-in-research)
- [Hamburg University of Applied Sciences](https://www.haw-hamburg.de/hibs/publizieren/publikationsfonds/)
- [Hamburg University of Technology](https://www.tub.tu-harburg.de/publizieren/openaccess/)
- [Heidelberg University](http://www.ub.uni-heidelberg.de/Englisch/service/openaccess/publikationsfonds.html)
- [Heinrich-Heine-Universität Düsseldorf](https://www.ulb.hhu.de/en/reseach-teaching-publishing/open-access/hhus-open-access-fund)
- [Hertie School](https://www.hertie-school.org/en/research/publishing-and-research-data)
- [Hochschule Aalen](https://www.hs-aalen.de/en/facilities/131)
- [Hochschule Anhalt](https://www.hs-anhalt.de/en/university/institutions/library/publish.html)
- [Hochschule Bielefeld - University of Applied Sciences and Arts (HSBI)](https://www.hsbi.de/open-access/publikationsfonds)
- [Hochschule Bonn-Rhein-Sieg](https://www.h-brs.de/en/bib/publication-fund)
- [Hochschule Düsseldorf](https://bib.hs-duesseldorf.de/en)
- [Hochschule Furtwangen](https://www.hs-furtwangen.de/en/search-for-books-and-media/)
- [Hochschule Hannover](https://www.hs-hannover.de/ueber-uns/organisation/bibliothek/services/publizieren-an-der-hsh/)
- [Hochschule Kaiserslautern](https://www.hs-kl.de/en/forschung/weiteres-zur-forschung/publikationsfonds)
- [Hochschule Konstanz Technik, Wirtschaft und Gestaltung](https://www.htwg-konstanz.de/hochschule/einrichtungen/bibliothek/publizieren-open-access/foerdermoeglichkeiten)
- [Hochschule Neubrandenburg](https://www.hs-nb.de/bibliothek/hauptmenue/wissenschaftliche-services/publizieren/open-access-beratung/#c1402011)
- Hochschule Reutlingen
- [Hochschule RheinMain](https://www.hs-rm.de/de/)
- [Hochschule für Technik und Wirtschaft Dresden](https://www.htw-dresden.de/open-access)
- [Humboldt-Universität zu Berlin](https://www.ub.hu-berlin.de/de/forschen-publizieren/open-access/finanzierung/publikationsfonds-zeitschriftenartikel)
- [JLU Gießen](https://www.uni-giessen.de/ub/en/digitales-publizieren-en/openaccess-en/oafonds-en?set_language=en)
- [Johann Wolfgang Goethe-Universität Frankfurt am Main](https://www.ub.uni-frankfurt.de/publizieren/publikationsfonds.html)
- [Johannes Gutenberg University of Mainz](https://www.ub.uni-mainz.de/de/open-access/foerderkriterien-open-access)
- [Leibniz Universität Hannover](https://tib.eu/oafonds)
- [Leipzig University](https://www.ub.uni-leipzig.de/open-science/publikationsfonds/)
- [Leuphana University of Lüneburg](https://www.leuphana.de)
- [Ludwig-Maximilians-Universität München](http://www.en.ub.uni-muenchen.de/writing/open-access-publishing/funding/index.html)
- [Martin Luther Universität Halle-Wittenberg](https://bibliothek.uni-halle.de/dbib/openaccess/)
- [Medizinische Hochschule Brandenburg Theodor Fontane](https://www.mhb-fontane.de/open-access-publikationsfonds-482.html)
- [Munich University of Applied Sciences](https://www.hm.edu)
- [Münster University](https://www.uni-muenster.de/Publizieren/service/publikationsfonds/)
- [Nürtingen-Geislingen University of Applied Science](https://www.hfwu.de)
- [Osnabrück University](https://www.ub.uni-osnabrueck.de/publizieren_archivieren/open_access/publikationsfonds.html)
- [Otto-von-Guericke-Universität Magdeburg](https://www.ub.ovgu.de/Publizieren+_+Open+Access/Open+Access.html)
- [Philipps University of Marburg](https://www.uni-marburg.de/de/ub/forschen/open-access/open-access-publikationsfonds)
- [RWTH Aachen](https://www.ub.rwth-aachen.de/cms/ub/Forschung/Wissenschaftliches-Publizieren/~iigq/Open-Access-Die-neue-Art-zu-publizieren/)
- [Regensburg University of Applied Sciences](https://www.oth-regensburg.de)
- [Rheinische Friedrich-Wilhelms-Universität Bonn](https://www.open-access.uni-bonn.de/de)
- [Rheinland-Pfälzische Technische Universität Kaiserslautern-Landau](https://ub.rptu.de/en/writing-publishing/open-access/financing-of-oa-publications)
- [Ruhr Universität Bochum](http://www.ruhr-uni-bochum.de/oa/)
- [Saarland University](https://www.sulb.uni-saarland.de/lernen/open-access/open-access-publikationsfonds/)
- [TH Köln - University of Applied Sciences](https://www.th-koeln.de/hochschulbibliothek/open-access-publikationsfonds_98372.php)
- TU Bergakademie Freiberg
- [Technische Hochschule Brandenburg](https://bibliothek.th-brandenburg.de/open-access-und-publizieren/open-access/)
- [Technische Hochschule Ingolstadt](https://www.thi.de/)
- [Technische Hochschule Wildau](https://www.th-wildau.de/hochschule/zentrale-einrichtungen/hochschulbibliothek/open-access-und-publikationsdienste/publikationsfonds/)
- [Technische Universität Berlin](http://www.ub.tu-berlin.de/publikationsfonds/)
- [Technische Universität Braunschweig](https://ub.tu-braunschweig.de/publikationsfonds/englisch/index_en.php)
- [Technische Universität Chemnitz](https://www.tu-chemnitz.de/ub/publizieren/openaccess/index.html.en)
- [Technische Universität Darmstadt](https://www.ulb.tu-darmstadt.de/service/elektronisches_publizieren/oa_publikationsfond/index.en.jsp)
- [Technische Universität Dortmund](https://ub.tu-dortmund.de/forschen-publizieren/open-access/)
- [Technische Universität Dresden](https://www.slub-dresden.de/veroeffentlichen/open-access)
- [Technische Universität Ilmenau](https://www.tu-ilmenau.de/universitaet/quicklinks/universitaetsbibliothek/forschen-publizieren/open-access/open-access-finanzierung/open-access-publikationsfonds)
- [Technische Universität München](https://www.ub.tum.de/en/publishing-fund)
- [Ulm University](https://www.uni-ulm.de/einrichtungen/kiz/service-katalog/wid/publikationsmanagement/oap/)
- [University Medical Center Hamburg-Eppendorf](https://www.uke.de/forschung/open-science/publikationsfoerderung/index.html)
- [University of Applied Sciences Mainz](https://www.hs-mainz.de/)
- [University of Applied Sciences Potsdam](https://www.fh-potsdam.de/campus-services/bibliothek/open-access-publizieren#section-18181)
- [University of Bremen](http://www.suub.uni-bremen.de/home-english/refworks-and-publishing/open-access-in-bremen-2/)
- University of Duisburg-Essen
- [University of Education Freiburg](https://www.ph-freiburg.de/)
- [University of Education Schwaebisch Gmuend](https://www.ph-gmuend.de)
- [University of Freiburg](https://www.ub.uni-freiburg.de/en/support/electronic-publishing/open-access/open-access-publication-fund/)
- [University of Greifswald](https://ub.uni-greifswald.de/en/service/for-academics/open-access/funding/)
- [University of Göttingen](http://www.sub.uni-goettingen.de/en/electronic-publishing/open-access/open-access-publication-funding/)
- [University of Kassel](http://www.uni-kassel.de/go/publikationsfonds)
- [University of Konstanz](https://www.kim.uni-konstanz.de/en/openscience/publishing-and-open-access/funding-open-access/)
- [University of Mannheim](https://www.bib.uni-mannheim.de/en/open-access-publishing-fund/)
- [University of Passau](https://www.ub.uni-passau.de/publizieren/open-access/publikationsfonds/)
- [University of Potsdam](https://publishup.uni-potsdam.de/home/index/help/content/publication_fund)
- [University of Regensburg](https://epub.uni-regensburg.de/oa-publizieren.html)
- [University of Rostock](https://www.ub.uni-rostock.de/wissenschaftliche-services/open-access/open-access-foerdermoeglichkeiten/)
- [University of Siegen](https://www.ub.uni-siegen.de/index.php?id=1510&L=1)
- [University of Stuttgart](https://oa.uni-stuttgart.de/publizieren/fonds/)
- [University of Trier](https://www.uni-trier.de/bibliothek/forschen-publizieren/open-access/open-access-publikationsfonds)
- [University of Veterinary Medicine Hannover, Foundation](http://www.tiho-hannover.de/de/kliniken-institute/bibliothek/open-access/publikationsfonds-an-der-tiho/)
- [University of Würzburg](https://www.bibliothek.uni-wuerzburg.de/en/research-publishing/open-access/publication-fund/)
- [Universität Augsburg](https://www.uni-augsburg.de/de/organisation/bibliothek/publizieren-zitieren-archivieren/open-access/)
- [Universität Erfurt](https://www.uni-erfurt.de/bibliothek/forschen-und-publizieren/publizieren-1/open-access-publikationsfonds)
- [Universität Hohenheim](https://kim.uni-hohenheim.de/en/openaccess)
- [Universität der Bundeswehr München](https://www.unibw.de)
- [Universität zu Köln](https://ub.uni-koeln.de/en/forschen-publizieren/publizieren/financial-support-for-open-access-publications)

###  Research institutes 

####  Fraunhofer Society 

- [Fraunhofer-Gesellschaft Publishing Fund](https://www.openaccess.fraunhofer.de/en/open-access-strategy.html)
- [Fraunhofer-Gesellschaft zur Förderung der angewandten Forschung e. V.](https://www.openaccess.fraunhofer.de/en/open-access-strategy.html)

####  Helmholtz Association 

- [Alfred-Wegener-Institut Helmholtz-Zentrum für Polar- und Meeresforschung](https://www.awi.de/en/)
- [Deutsches Elektronen-Synchrotron DESY](https://library.desy.de/open_access/publishing_options_for_authors/)
- [Deutsches Zentrum für Luft- und Raumfahrt](https://www.dlr.de/de/das-dlr/ueber-uns/organisation/wissenschaftliche-information/dlr-bibliothek)
- [Forschungszentrum Jülich](https://www.fz-juelich.de/zb/DE/Leistungen/Open_Access/publikationsfonds/publikationsfonds_node.html)
- [GEOMAR - Helmholtz Centre for Ocean Research Kiel](https://www.geomar.de/en/centre/central-facilities/bibliothek/author-services/publication-costs)
- [GFZ German Research Centre for Geosciences](https://www.gfz-potsdam.de/en) (data provided by the [Library Wissenschaftspark Albert Einstein](http://bib.telegrafenberg.de/en/publishing/open-access/))
- [GSI Helmholtzzentrum für Schwerionenforschung](https://www.gsi.de/bibliothekunddokumentation/open_access_gsi)
- [Helmholtz Zentrum München](https://www.helmholtz-munich.de/en/)
- [Helmholtz-Zentrum Dresden-Rossendorf](http://www.hzdr.de/db/Cms?pNid=73)
- [Helmholtz-Zentrum für Umweltforschung – UFZ](https://www.ufz.de/index.php?en=36297)
- [KIT Karlsruhe](https://www.bibliothek.kit.edu/publikationsfonds.php)
- [Max Delbrück Center for Molecular Medicine (MDC)](https://www.mdc-berlin.de/about_the_mdc/structure/administration/library/oa?mdcbl%5B0%5D=/library&mdctl=0&mdcou=0&mdcot=0&mdcbv=nqe3t2xG8PGtPtxTs7kNhLVIaYkEwltgLl3DWBohxeI)

####  Leibniz Association 

- [DIPF | Leibniz-Institut für Bildungsforschung und Bildungsinformation](https://www.dipf.de/en/knowledge-resources/dipfdocs-open-access?set_language=en)
- [Deutsches Institut für Ernährungsforschung Potsdam-Rehbrücke](https://www.dife.de/en/about-us/organization/science-coordination/)
- [Deutsches Primatenzentrum - Leibniz-Institut für Primatenforschung](https://www.dpz.eu/de/abteilung/bibliothek/serviceangebot.html)
- [Forschungsinstitut für Nutztierbiologie (FBN)](https://www.fbn-dummerstorf.de/)
- [GESIS - Leibniz-Institut für Sozialwissenschaften](https://www.gesis.org/en/home)
- [GIGA German Institute of Global and Area Studies](https://www.giga-hamburg.de/de/das-giga/giga-bibliothek/open-access)
- [IGB - Leibniz-Institute of Freshwater Ecology and Inland Fisheries](https://www.igb-berlin.de/en/library)
- [INM - Leibniz Institute for New Materials](https://www.ntnm-bib.de/en/)
- [IPN - Leibniz Institute for Science and Mathematics Education](https://www.leibniz-ipn.de/de/das-ipn/ueber-uns/bibliothek)
- [Kiel Institute for the World Economy](https://www.ifw-kiel.de/institute/about-the-kiel-institute/organization/open-access-policy-of-the-kiel-institute/)
- [Leibniz Institute for Baltic Sea Research](https://www.io-warnemuende.de/en_index.html)
- [Leibniz Institute for the German Language](https://www.ids-mannheim.de/bibliothek/open-access-am-ids/)
- [Leibniz-Fonds](https://www.leibniz-gemeinschaft.de/en/research/open-science-and-digitalisation/open-access)
- [Leibniz-Institut für Festkörper- und Werkstoffforschung Dresden](https://www.ifw-dresden.de/about-us/library)
- [Leibniz-Institut für Pflanzengenetik und Kulturpflanzenforschung](https://www.ipk-gatersleben.de/en/library)
- [Leibniz-Institut für Präventionsforschung und Epidemiologie - BIPS](https://www.bips-institut.de/en/index.html)
- [Leibniz-Institut für Raumbezogene Sozialforschung (IRS)](https://leibniz-irs.de/en/research/publications/open-access)
- [Leibniz-Institut für Zoo- und Wildtierforschung](https://www.izw-berlin.de/de/bibliothek.html)
- [Leibniz-Institut für ökologische Raumentwicklung](https://www.ioer.de/en/)
- [Leibniz-Zentrum für Agrarlandschaftsforschung (ZALF)](https://www.zalf.de/en/struktur/bib/Pages/Bibliothek.aspx)
- [Leibniz-Zentrum für Marine Tropenforschung](https://www.leibniz-zmt.de/en/research-infrastructure/media-unit.html)
- Museum für Naturkunde - Leibniz-Institut für Evolutions- und Biodiversitätsforschung
- [Paul-Drude-Institut für Festkörperelektronik](http://www.pdi-berlin.de/home/)
- [Potsdam Institute for Climate Impact Research (PIK)](https://www.pik-potsdam.de) (data provided by the [Library Wissenschaftspark Albert Einstein](http://bib.telegrafenberg.de/en/publishing/open-access/))
- [TIB – German National Library of Science and Technology](https://www.tib.eu/en/service/tib-open-access-policy/)
- [WIAS - Weierstrass Institute for Applied Analysis and Stochastics](https://www.wias-berlin.de/services/library/)

####  Max Planck Society 

- [Max Planck Digital Library](http://www.mpdl.mpg.de/21-specials/50-open-access-publishing.html) (The data content covers APCs as paid for by the central budget for the Max Planck Society (MPS). APCs funded locally by Max Planck Institutes are not part of the data. The MPS has a limited input tax reduction. The refund of input VAT for APC is 20%. Until the end of 2007 the MPS was VAT exempt.)

###  Other institutions 

- [Institut für Arbeitsmarkt- und Berufsforschung (IAB)](https://iab.de/en/the-iab/aufgaben-und-leitlinien-en/open-access/)
- [Knowledge Unlatched](http://www.knowledgeunlatched.org/)
- [OA-Monofonds Brandenburg](https://open-access-brandenburg.de/fonds/)
- [SWP - German Institute for International and Security Affairs](https://www.swp-berlin.org/en/)

- Hannover U und TIB

</details>

## Institutions from Austria 

<details>

- [AC2T Research GmbH](https://www.ac2t.at/en/)
- [Carinthia University of Applied Sciences (CUAS)](https://www.fh-kaernten.at/en/)
- [Danube University Krems University for Continuing Education](https://www.donau-uni.ac.at/en.html)
- [FH Campus Wien - University of Applied Sciences](https://www.fh-campuswien.ac.at/en)
- [FH Joanneum - University of Applied Sciences](https://www.fh-joanneum.at/en/)
- [FH Kufstein Tirol - University of Applied Sciences](https://www.fh-kufstein.ac.at/eng/)
- [FH Salzburg - University of Applied Sciences](https://www.fh-salzburg.ac.at/en/)
- [FH St. Pölten - University of Applied Sciences](https://www.fhstp.ac.at/en)
- [FH Vorarlberg - University of Applied Sciences](https://www.fhv.at/en/)
- [FHWien der WKW (FHW)](https://www.fh-wien.ac.at/en/)
- [FWF - Austrian Science Fund](https://www.fwf.ac.at/en/research-funding/open-access-policy/)
- [Ferdinand Porsche FernFH](https://www.fernfh.ac.at/en)
- [Graz University of Technology](https://www.tugraz.at/en/home)
- [Institute for Advanced Studies Vienna](https://www.ihs.ac.at/)
- [Institute of Science and Technology Austria](https://ist.ac.at/en/research/library/publish-communicate/)
- [International Institute for Applied Systems Analysis (IIASA)](https://iiasa.ac.at/)
- [Johannes Kepler University Linz](https://www.jku.at/en/library/service/bibliometrics-and-publication-support/open-access-publishing/publication-fund/)
- [Medical University of Graz](https://www.medunigraz.at/en/)
- [Medical University of Innsbruck](https://www.i-med.ac.at/mypoint/index.xml.en)
- [Medical University of Vienna](https://www.meduniwien.ac.at/web/en/)
- [Modul University Vienna (MUVIENNA)](https://www.modul.ac.at/)
- [Montanuniversität Leoben](https://www.unileoben.ac.at/en/)
- [Paracelsus Medical University](https://www.pmu.ac.at/en/home.html)
- Research Institute of Molecular Pathology (IMP) / IMBA - Institute of Molecular Biotechnology / Gregor Mendel Institute of Molecular Plant Biology
- [Research Institute of Molecular Pathology - IMP](https://www.imp.ac.at/)
- [Technische Universität Wien](https://www.tuwien.at/bibliothek/publizieren/open-access-und-urheberrecht)
- [University of Applied Sciences Burgenland](https://www.fh-burgenland.at/en/)
- [University of Applied Sciences Upper Austria](https://www.fh-ooe.at/en/)
- [University of Applied Sciences Wiener Neustadt for Business and Engineering](https://www.fhwn.ac.at/en/)
- [University of Graz](https://www.uni-graz.at/en/)
- [University of Innsbruck](https://www.uibk.ac.at/en/)
- University of Innsbruck and Medical University of Innsbruck
- [University of Klagenfurt](https://www.aau.at/en/)
- [University of Natural Resources and Life Sciences Vienna (BOKU)](https://boku.ac.at/en/)
- [University of Salzburg](https://www.plus.ac.at/university-library/services/open-access/open-access-policy/?lang=en)
- [University of Veterinary Medicine Vienna](https://www.vetmeduni.ac.at/en/)
- [University of Vienna](https://www.univie.ac.at/en/)
- [Vienna University of Economics and Business (WU)](https://www.wu.ac.at/en/)

</details>

## Institutions from Switzerland 

<details>

- [Agroscope](https://www.agroscope.admin.ch/agroscope/en/home.html)
- [Bern University of Applied Sciences](http://www.bfh.ch/)
- [ETH Zürich](https://library.ethz.ch/en/publishing-and-archiving/publishing-and-registering/publishing-in-open-access-journals.html)
- [Eawag - Swiss Federal Institute of Aquatic Science and Technology](https://www.eawag.ch/en/) (via [Lib4RI](https://www.lib4ri.ch/services/open-access.html))
- [Empa - Swiss Federal Laboratories for Materials Science and Technology](https://www.empa.ch/) (via [Lib4RI](https://www.lib4ri.ch/services/open-access.html))
- [European Organization for Nuclear Research](https://home.web.cern.ch/)
- [Forschungsinstitut für biologischen Landbau FiBL](https://www.fibl.org/en)
- [Graduate Institute of International and Development Studies](http://graduateinstitute.ch/home.html)
- [Haute Ecole Pédagogique du Valais](https://hepvs.ch/)
- [Haute École Pédagogique BEJUNE](https://www.hep-bejune.ch/)
- [Haute École Pédagogique Fribourg](https://hepfr.ch/)
- [Haute École Pédagogique du Canton de Vaud](https://www.hepl.ch/accueil.html)
- [Hochschule Luzern](https://www.hslu.ch/de-ch/hochschule-luzern/campus/bibliotheken/open-access-zugang-zu-wissenschaftlichen-arbeiten/)
- [Kalaidos University of Applied Sciences](https://www.kalaidos-fh.ch/de-CH/)
- [Medicines for Malaria Venture](https://www.mmv.org/)
- [OST University of Applied Science of Eastern Switzerland](https://www.ost.ch/en/)
- [PSI - Paul Scherrer Institute](https://www.psi.ch/en)
- [Pädagogische Hochschule Bern](https://www.phbern.ch/)
- [Pädagogische Hochschule Graubünden](https://phgr.ch/)
- [Pädagogische Hochschule Luzern](https://www.phlu.ch/)
- [Pädagogische Hochschule Thurgau](https://www.phtg.ch/)
- [Pädagogische Hochschule Zürich](https://phzh.ch/ueber-die-phzh/campus/bibliothek/open-access/)
- [Schwyz University of Teacher Education](https://www.phsz.ch/en/)
- [St.Gallen University of Teacher Education](https://www.phsg.ch/en)
- [Swiss Distance University Institute](https://unidistance.ch/en/)
- [Swiss Federal University for Vocational Education and Training](https://www.sfuvet.swiss/)
- [Swiss National Science Foundation (SNSF)](http://www.snf.ch/en/theSNSF/research-policies/open-access/Pages/default.aspx#OA%202020%20Policy)
- [Swiss Ornithological Institute](https://www.vogelwarte.ch/de/home/)
- [University Hospital of Bern](https://www.insel.ch/de/)
- [University Psychiatric Services Bern - UPD](https://www.upd.ch/de/)
- [University of Applied Sciences and Arts Northwestern Switzerland](https://www.fhnw.ch/en)
- [University of Applied Sciences and Arts Western Switzerland](https://www.hes-so.ch/en/homepage)
- [University of Applied Sciences and Arts of Southern Switzerland](https://www.supsi.ch/home_en.html)
- [University of Applied Sciences in Business Administration Zurich](https://fh-hwz.ch/english/)
- [University of Applied Sciences of the Grisons](https://www.fhgr.ch/en/)
- [University of Basel](https://ub.unibas.ch/de/digitale-dienste/open-access/)
- [University of Bern](https://www.ub.unibe.ch/services/open_science/open_access/oa_fonds/index_eng.html)
- [University of Fribourg](https://www.unifr.ch/home/en/)
- [University of Geneva](https://www.unige.ch/)
- [University of Lausanne](https://www.unil.ch/openscience/en/home/menuinst/open-access/open-access-a-lunil/soutien-360/voie-doree/gold-open-access-fund-unil.html)
- [University of Neuchatel](https://www.unine.ch/)
- [University of St.Gallen](https://www.unisg.ch/)
- [University of Teacher Education Zug](https://www.zg.ch/behoerden/direktion-fur-bildung-und-kultur/phzg/university-of-teacher-education-zug)
- [University of Teacher Education in Special Needs](https://www.hfh.ch/en)
- [University of Zurich](https://www.ub.uzh.ch/de/wissenschaftlich-arbeiten/publizieren/Open-Access.html)
- [Università della Svizzera italiana](https://www.usi.ch/en)
- [Universität Luzern](https://www.zhbluzern.ch/lernen-forschen/open-science/open-access-publizieren)
- [WSL - Swiss Federal Institute for Forest, Snow and Landscape Research](https://www.wsl.ch/en/index.html)
- [ZHAW Zurich University of Applied Sciences](https://www.zhaw.ch/en/library/writing-publishing/publishing-and-open-access/oa-at-the-zhaw/#c112481)
- [Zentralbibliothek Zürich](https://www.zb.uzh.ch/en/services/forschungsforderung#Bretscher)
- [Zurich University of the Arts](https://www.zhdk.ch/miz/miz-oa)
- [École Polytechnique Fédérale de Lausanne](https://www.epfl.ch/en/)

</details>

## Institutions from Italy 

<details>

- [Consiglio Nazionale Delle Ricerche (CNR)](https://www.cnr.it/en/cnr-open-access)
- [Free University of Bozen-Bolzano](https://www.unibz.it/en/services/library/publishing-at-unibz/unibz-open-access-publishing-fund/)
- [Scuola Normale Superiore](https://www.sns.it/it)
- [University of Ferrara](https://www.unife.it)
- [University of Milano-Bicocca](https://en.unimib.it/)
- [University of Padua](https://biblio.unipd.it/en/digital-library/about-publishing/agreements-with-publishers)
- [Università degli Studi di Milano](https://www.unimi.it/en)
- [Università degli Studi di Modena e Reggio Emilia](https://international.unimore.it/)
- [Veneto Institute of Oncology (IOV IRCCS)](https://www.ioveneto.it/unit/gestione-documentazione-scientifica/)

</details>

## Institutions from Norway 

<details>

- Akershus University Hospital
- BI Norwegian Business School
- Bergen University College
- Fridtjof Nansen Institute
- GenØk - Centre for Biosafety
- Harstad University College
- Innlandet Hospital Trust
- Institute of Marine Research
- Molde University College
- Nansen Environmental and Remote Sensing Center
- Nord University
- Norwegian Center for Studies on Violence and Traumatic Stress
- Norwegian Institute for Agricultural and Environmental Research
- Norwegian Institute for Air Research
- Norwegian Institute for Nature Research
- Norwegian Institute of Public Health
- Norwegian Institute of Water Research
- Norwegian School of Sport Sciences
- Norwegian University of Life Sciences
- Norwegian University of Science and Technology
- Oslo University Hospital
- Oslo and Akershus University College
- SINTEF (Foundation for Scientific and Industrial Research)
- Sørlandet Hospital Trust
- Uni Research
- University College of Southeast Norway
- University of Agder
- University of Bergen
- University of Oslo
- University of Stavanger
- University of Tromsø - The Arctic University of Norway
- Vestfold Hospital Trust
- Vestre Viken Hospital Trust

</details>

## Institutions from Spain 

<details>

- [Consejo Superior de Investigaciones Cientificas (CSIC)](https://www.csic.es/en)
- [Universitat de Barcelona](https://crai.ub.edu/en/services-and-resources/copyright-intellectual-property-open-access-support/ub-open-acess)

</details>

## Institutions from Sweden 

<details>

- BTH Blekinge Institute of Technology
- Chalmers University of Technology
- Dalarna University
- Halmstad University
- [Institute Mittag-Leffler](http://www.mittag-leffler.se/)
- Jönköping University
- KTH Royal Institute of Technology
- Karlstad University
- Karolinska Institutet
- [Kristianstad University](https://www.hkr.se/en/)
- Linköping University
- Linnaeus University
- Luleå University of Technology
- Lund University
- Malmö University
- [Marie Cederschiöld University](https://www.mchs.se/)
- [Medical Products Agency](https://www.lakemedelsverket.se/en)
- [Mid Sweden University](https://www.miun.se/en)
- Mälardalen University
- [Public Health Agency of Sweden](https://www.folkhalsomyndigheten.se/the-public-health-agency-of-sweden/)
- [RISE Research Institutes of Sweden](https://www.ri.se/en)
- [Sophiahemmet University College](https://www.shh.se/en/)
- Stockholm School of Economics
- Stockholm University
- [Swedish Defence Research Agency](https://www.foi.se/en/foi.html)
- [Swedish Museum of Natural History](https://www.nrm.se/engelska/in-english)
- [Swedish National Road and Transport Research Institute (VTI)](https://www.vti.se/en/)
- Swedish School of Sport and Health Sciences
- Swedish University of Agricultural Sciences
- Södertörns University
- [The Swedish Environmental Protection Agency](https://www.naturvardsverket.se/en)
- Umeå University
- University West
- University of Borås
- University of Gothenburg
- University of Gävle
- University of Skövde
- Uppsala University
- Örebro University

</details>

## Institutions from Finland 

<details>

- Aalto University
- [Arcada University of Applied Sciences](https://www.arcada.fi/en)
- [Centria University of Applied Sciences](https://net.centria.fi/en/)
- [City of Helsinki](https://www.hel.fi/en)
- [Diaconia University of Applied Sciences](https://www.diak.fi/en/)
- [European Chemicals Agency](https://echa.europa.eu/)
- [Finnish Defence Research Agency](https://puolustusvoimat.fi/en/about-us/finnish-defence-research-agency)
- Finnish Environment Institute
- [Finnish Food Authority](https://www.ruokavirasto.fi/)
- [Finnish Institute for Health and Welfare](https://thl.fi/en/web/thlfi-en)
- [Finnish Institute of Occupational Health](https://www.ttl.fi/en)
- [Finnish Medicines Agency Fimea](https://fimea.fi/en/frontpage)
- [Finnish Meteorological Institute](https://en.ilmatieteenlaitos.fi/)
- [Geological Survey of Finland](https://www.gtk.fi/en/)
- Haaga-Helia University of Applied Sciences
- [Hanken School of Economics](https://www.hanken.fi/en)
- Häme University of Applied Sciences
- JAMK University of Applied Sciences
- [LAB University of Applied Sciences](https://www.lab.fi/en)
- Lapin ammattikorkeakoulu (Lapland University of Applied Sciences)
- [Lappeenranta-Lahti University of Technology LUT](https://www.lut.fi/en)
- [Laurea University of Applied Sciences](https://www.laurea.fi/en/)
- [Metropolia University of Applied Sciences](https://www.metropolia.fi/en)
- [National Land Survey of Finland](https://www.maanmittauslaitos.fi/en)
- Natural Resources Institute Finland
- [Novia University of Applied Sciences](https://www.novia.fi/novia-uas/)
- [Oulu University of Applied Sciences](https://www.oamk.fi/en/)
- Satakunta University of Applied Sciences
- Seinäjoki University of Applied Sciences
- [Social Insurance Institution of Finland](https://www.kela.fi/main-page)
- South-Eastern Finland University of Applied Sciences (Xamk)
- [Tampere University](https://libguides.tuni.fi/open-access/introduction)
- [Tampere University of Applied Sciences](https://www.tuni.fi/fi/tutustu-meihin/tamk)
- The National Defence University Finland
- [Turku University of Applied Sciences](https://www.tuas.fi/en/)
- University of Applied Sciences Savonia
- [University of Eastern Finland](https://www.uef.fi/en/etusivu)
- [University of Helsinki](https://www.helsinki.fi/en)
- [University of Jyväskylä](https://openscience.jyu.fi/en/open-access-publishing)
- [University of Lapland](https://lib.luc.fi/EN)
- [University of Oulu](https://www.oulu.fi/en)
- [University of Turku](https://utuguides.fi/openaccess)
- [University of Vaasa](https://www.uwasa.fi/en)
- [University of the Arts Helsinki](https://www.uniarts.fi/en/)
- [VAMK University of Applied Sciences](https://www.vamk.fi/en/)
- [VATT Institute for Economic Research](https://vatt.fi/etusivu)
- VTT Technical Research Centre of Finland
- Åbo Akademi University

</details>

## Institutions from France 

<details>

- [ANSES - Agence nationale de sécurité sanitaire de l'alimentation, de l'environnement et du travail](https://www.anses.fr/en)
- ANSM - Agence Nationale de Sécurité des Médicaments et des produits de santé
- AgroParisTech
- Aix-Marseille Université
- Avignon Université
- CEA - Commissariat à l'énergie atomique et aux énergies alternatives
- CIRAD - Centre de coopération internationale en recherche agronomique pour le développement
- CNAM - Conservatoire national des arts et métiers
- CNRS - Centre national de la recherche scientifique
- Centrale Nantes
- CentraleSupélec
- Centre Georges-François Leclerc (CGFL) - Centre régional de lutte contre le cancer du réseau UNICANCER
- [Centre Hospitalier Universitaire d'Amiens](https://www.chu-amiens.fr/)
- Centre Hospitalier Universitaire d'Orléans
- [Centre Hospitalier Universitaire de Lille](https://www.chu-lille.fr/welcome.en)
- Centre Hospitalier Universitaire de Rennes
- [EHESP - Ecole des hautes études en santé publique](https://www.ehesp.fr/en/)
- ENAC - Ecole Nationale de l'Aviation Civile
- ENGEES - Ecole nationale du Génie de l'Eau et de l'Environnement de Strasbourg
- ENPC - École des Ponts ParisTech
- ENS Lyon - Ecole normale supérieure de Lyon
- ENS Paris - Ecole normale supérieure de Paris
- ENSICAEN - Ecole nationale supérieure de Caen
- ENSTA Bretagne - Ecole nationale supérieure de techniques avancées - Bretagne
- ESPCI - Ecole supérieure de physique et de chimie industrielles
- ESRF - European Synchrotron Radiation Facility
- EURECOM
- EZUS - LYON
- Ecole centrale de Lyon
- Ecole polytechnique
- [EnvA - Ecole nationale vétérinaire d'Alfort](https://www.vet-alfort.fr/)
- French institutions
- HCL - Hospices civils de Lyon
- IFREMER - Institut Français de Recherche pour l'Exploitation de la Mer
- IFSTTAR - Institut Français des Sciences et Technologies des Transports, de l’aménagement et des Réseaux
- ILL - Institut Laue-Langevin
- IMT Atlantique Bretagne - Pays de la Loire
- [IMT Mines Alès](https://www.imt-mines-ales.fr/en)
- INRA - Institut National de la Recherche Agronomique
- INRAE - Institut national de recherche pour l’agriculture, l’alimentation et l’environnement
- INRIA - Institut National de Recherche en Informatique et en Automatique
- INSA Lyon - Institut National des Sciences Appliquées de Lyon
- INSA Strasbourg - Institut National des Sciences Appliquées de Strasbourg
- INSA Toulouse - Institut National des Sciences Appliquées de Toulouse
- INSEP - Institut National du Sport, de l'Expertise et de la Performance
- INSERM - Institut National de la Santé et de la Recherche Médicale
- IRD - Institut de Recherche pour le Développement
- IRSN - Institut de Radioprotection et de Sûreté Nucléaire
- IRSTEA - Institut de Recherche en Sciences et Technologies pour l'Environnement et l'Agriculture
- ISARA - Institut Supérieur d'Agriculture et d'Agroalimentaire Rhône-Alpes
- Institut Pasteur
- LNE - Laboratoire National de Métrologie et d'Essais
- La Rochelle Université
- Le Mans Université
- MNHN - Muséum National d'Histoire Naturelle
- Mines Paris - Ecole nationale supérieure des Mines de Paris
- Nantes Université
- ONERA - Office National d'Etudes et de Recherches Aérospatiales - The French Aerospace Lab
- Sciences Po Paris - Institut d'Etudes Politiques de Paris
- Sorbonne Université
- Toulouse INP - Institut National Polytechnique de Toulouse
- Université Bordeaux Montaigne
- Université Claude Bernard - Lyon I
- Université Clermont Auvergne
- Université Côte d'Azur - UniCA
- Université Grenoble Alpes
- Université Gustave Eiffel
- Université Jean Moulin - Lyon III
- Université Le Havre Normandie
- Université Lumière - Lyon II
- Université Marie et Louis Pasteur
- Université Panthéon-Sorbonne - Paris I
- [Université Paris Cité](https://u-paris.fr/en/)
- Université Paris Descartes - Paris V
- Université Paris Diderot - Paris VII
- Université Paris-Dauphine - Paris IX
- [Université Paris-Est Créteil Val de Marne - Paris XII](https://www.en.u-pec.fr/)
- Université Paris-Est Marne-la-Vallée
- Université Pierre et Marie Curie - Paris VI
- Université Polytechnique Hauts-de-France
- Université Savoie Mont Blanc
- Université Sorbonne Nouvelle - Paris III - USN
- Université Toulouse - Jean Jaurès
- Université Toulouse III
- Université Vincennes-Saint Denis - Paris VIII
- Université d'Angers
- Université d'Evry-Val-d'Essonne
- Université d'Orléans
- Université de Bordeaux
- Université de Bourgogne
- Université de Bretagne Occidentale - UBO
- Université de Bretagne Sud - UBS
- Université de Caen Normandie
- Université de Franche-Comté
- Université de Haute-Alsace
- Université de La Réunion
- Université de Lille
- Université de Lille I Sciences et technologies
- Université de Lille II Droit et Santé
- [Université de Limoges](https://www.unilim.fr/?lang=en)
- Université de Lorraine
- Université de Montpellier
- Université de Montpellier - Paul Valéry
- Université de Nîmes
- Université de Paris Ouest Nanterre La Défense - Paris X
- Université de Pau et des Pays de l'Adour - UPPA
- Université de Perpignan Via Domitia
- Université de Picardie Jules Verne
- Université de Poitiers
- Université de Reims Champagne-Ardenne
- Université de Rennes
- Université de Rennes II Haute-Bretagne
- Université de Strasbourg
- Université de Technologie de Compiègne
- Université de Toulon
- Université de Tours
- Université de Versailles Saint-Quentin-en-Yvelines
- Université de la Nouvelle-Calédonie
- Université de la Polynésie française
- Université de technologie de Troyes
- Université des Antilles
- Université du Littoral Côte d'Opale

</details>

## Institutions from the United Kingdom 

<details>

- Aberystwyth University
- [Anglia Ruskin University](https://www.aru.ac.uk/)
- Aston University
- Bangor University
- Birkbeck, University of London
- [Birmingham City University](https://www.bcu.ac.uk/)
- [Bournemouth University](https://www.bournemouth.ac.uk/)
- Brunel University
- [Cardiff Metropolitan University](https://www.cardiffmet.ac.uk/Pages/default.aspx)
- Cardiff University
- [City University London](https://www.city.ac.uk/)
- Cranfield University
- [Edge Hill University](https://www.edgehill.ac.uk/)
- Edinburgh Napier University
- Glasgow Caledonian University
- Goldsmiths, University of London
- Heriot-Watt University
- Imperial College London
- Institute of Cancer Research (ICR)
- Keele University
- King's College London
- [Kingston University](https://www.kingston.ac.uk/)
- Lancaster University
- Leeds Beckett University
- Liverpool John Moores University
- Liverpool School of Tropical Medicine
- London School of Economics (LSE)
- London School of Hygiene & Tropical Medicine (LSHTM)
- London South Bank University
- Manchester Metropolitan University
- [Natural History Museum](https://www.nhm.ac.uk/)
- Northumbria University
- [Nottingham Trent University](https://www.ntu.ac.uk/)
- Oxford Brookes University
- Plymouth University
- [Queen Margaret University](https://www.qmu.ac.uk/)
- Queen Mary University of London
- Queen's University Belfast
- [Robert Gordon University](https://www.rgu.ac.uk/)
- [Royal Botanic Gardens](https://www.kew.org/)
- Royal Holloway, University of London
- Royal Veterinary College
- SOAS University of London
- [Scotland's Rural College](https://www.sruc.ac.uk/)
- [Sheffield Hallam University](https://libguides.shu.ac.uk/OpenAccess/)
- St George's, University of London
- Swansea University
- The Open University
- [University Campus Suffolk](https://www.uos.ac.uk/)
- University College London (UCL)
- University of Aberdeen
- [University of Abertay Dundee](https://www.abertay.ac.uk/)
- University of Bath
- [University of Bedfordshire](https://www.beds.ac.uk/)
- University of Birmingham
- [University of Bradford](https://www.bradford.ac.uk/external/)
- University of Bristol
- University of Cambridge
- [University of Central Lancashire](https://www.uclan.ac.uk/)
- [University of Chester](https://www1.chester.ac.uk/)
- [University of Derby](https://www.derby.ac.uk/)
- University of Dundee
- University of Durham
- University of East Anglia
- University of Edinburgh
- University of Exeter
- University of Glasgow
- [University of Greenwich](https://www.gre.ac.uk/)
- University of Huddersfield
- University of Hull
- University of Kent
- University of Leeds
- University of Leicester
- [University of Lincoln](http://www.lincoln.ac.uk/home/)
- University of Liverpool
- University of Loughborough
- University of Manchester
- University of Newcastle
- [University of Northampton](https://www.northampton.ac.uk/)
- University of Nottingham
- University of Oxford
- University of Portsmouth
- University of Reading
- [University of Roehampton](https://www.roehampton.ac.uk/)
- University of Salford
- University of Sheffield
- University of Southampton
- University of St Andrews
- [University of Stirling](https://www.stir.ac.uk/)
- University of Strathclyde
- University of Surrey
- University of Sussex
- University of Ulster
- [University of Wales Trinity St David](https://www.uwtsd.ac.uk/)
- University of Warwick
- [University of West of Scotland](https://www.uws.ac.uk/home/)
- [University of Westminster](https://www.westminster.ac.uk/)
- [University of Worcester](https://www.worcester.ac.uk/)
- University of York
- [University of the Highlands and Islands](https://www.uhi.ac.uk/en/)
- University of the West of England
- [Wellcome Trust](https://wellcome.ac.uk/funding/managing-grant/open-access-policy)

</details>

## Institutions from the Czech Republic 

<details>

- [Charles University](https://cuni.cz/UKEN-1.html)
- [University of Chemistry and Technology, Prague](https://www.chemtk.cz/en/)
- [VSB - Technical University of Ostrava](https://www.vsb.cz/en)

</details>

## Institutions from Hungary 

<details>

- [University of Debrecen](https://unideb.hu/en)

</details>

## Institutions from Serbia 

<details>

- [University of Belgrade](http://bg.ac.rs/en/)

</details>

## Institutions from Belgium 

<details>

- [University of Liège](https://www.uliege.be/cms/c_8699436/en/uliege)

</details>

## Institutions from the United States 

<details>

- [Bill & Melinda Gates Foundation](https://www.gatesfoundation.org/how-we-work/general-information/open-access-policy)
- [Harvard University](https://osc.hul.harvard.edu/programs/hope/)
- [Indiana University - Purdue University Indianapolis (IUPUI)](https://ulib.iupui.edu/digitalscholarship/openaccess/oafund)
- [Thomas Jefferson University](https://library.jefferson.edu/pub/open_access.cfm)
- [University of Rhode Island](https://uri.libguides.com/oafund)
- [Virginia Polytechnic Institute and State University](http://guides.lib.vt.edu/oa)

</details>

## Institutions from Canada 

<details>

- [Acadia University](http://www2.acadiau.ca/)
- [Algoma University](https://algomau.ca)
- [Athabasca University](https://www.athabascau.ca)
- [BC Children's Hospital Foundation](http://www.bcchf.ca/)
- [Balsillie School of International Affairs](https://balsillieschool.ca)
- [Bishop's University](https://www.ubishops.ca)
- [Brandon University](https://www.brandonu.ca/)
- [Brock University](https://brocku.ca)
- [Bruyère](http://www.bruyere.org/)
- [Canadian Research Knowledge Network](http://www.crkn-rcdr.ca)
- [Cape Breton University](http://www.cbu.ca/)
- [Carleton University](https://carleton.ca)
- [Concordia University](https://www.concordia.ca/)
- [Dalhousie University](https://www.dal.ca)
- [HEC Montréal](https://www.hec.ca)
- [Holland Bloorview Kids Rehabilitation Hospital](https://hollandbloorview.ca)
- [Hospital for Sick Children](http://www.sickkids.ca/)
- [Institut National de la Recherche Scientifique](https://inrs.ca)
- [Institut Universitaire de Cardiologie et de Pneumologie de Québec](http://iucpq.qc.ca/en)
- [Kwantlen Polytechnic University](https://www.kpu.ca)
- [Lakehead University](https://www.lakeheadu.ca)
- [Laurentian University](https://laurentian.ca/)
- [MacEwan University](https://www.macewan.ca)
- [McGill University](https://www.mcgill.ca)
- [McMaster University](https://www.mcmaster.ca)
- [Memorial University of Newfoundland](https://mun.ca)
- [Mount Allison University](https://mta.ca)
- [Mount Royal University](https://www.mtroyal.ca)
- [Mount Saint Vincent University](https://www.msvu.ca)
- [Mount Sinai Hospital](http://www.mountsinai.on.ca/)
- [NOSM University](https://www.nosm.ca)
- [Nipissing University](https://www.nipissingu.ca)
- [Ontario College of Art and Design](https://www.ocadu.ca)
- [Polytechnique Montréal](https://polymtl.ca)
- [Princess Margaret Cancer Centre](http://www.uhn.ca/PrincessMargaret)
- [Queen's University](http://www.queensu.ca/)
- [Royal Roads University](https://www.royalroads.ca)
- [Saint Mary's University](https://www.smu.ca)
- [Simon Fraser University](https://www.sfu.ca)
- [St. Francis Xavier University](https://www.stfx.ca)
- [St. Jerome's University](http://www.sju.ca/)
- [Sunnybrook Health Science Centre](http://sunnybrook.ca/)
- [Thompson Rivers University](https://www.tru.ca)
- [Toronto General Hospital](http://www.uhn.ca/corporate/AboutUHN/OurHospitals/TGH)
- [Toronto Metropolitan University](https://www.torontomu.ca)
- [Toronto Rehabilitation Institute](http://www.torontorehabfoundation.com/)
- [Toronto Western Hospital](http://www.uhn.ca/corporate/AboutUHN/OurHospitals/TWH)
- [Trent University](https://www.trentu.ca)
- [Trillium Health Centre](http://trilliumhealthpartners.ca/Pages/default.aspx)
- [Trinity Western University](https://www.twu.ca)
- [University Health Network](https://www.uhn.ca)
- [University of Alberta](https://www.ualberta.ca)
- [University of British Columbia](https://www.ubc.ca/)
- [University of Calgary](https://library.ucalgary.ca/oa/)
- [University of Guelph](https://www.uoguelph.ca)
- [University of Lethbridge](https://www.ulethbridge.ca)
- [University of Manitoba](https://umanitoba.ca)
- [University of New Brunswick](https://unb.ca)
- [University of Northern British Columbia](https://www.unbc.ca)
- [University of Ontario Institute of Technology](http://www.uoit.ca/)
- [University of Ottawa](https://www.uottawa.ca)
- [University of Prince Edward Island](http://home.upei.ca/)
- [University of Regina](https://www.uregina.ca)
- [University of Saskatchewan](https://www.usask.ca/)
- [University of Toronto](https://www.utoronto.ca)
- [University of Victoria](https://www.uvic.ca)
- [University of Waterloo](https://uwaterloo.ca/)
- [University of Windsor](https://www.uwindsor.ca)
- [University of Winnipeg](https://www.uwinnipeg.ca)
- [University of the Fraser Valley](https://ufv.ca)
- [Université Laval](https://www.ulaval.ca)
- [Université TÉLUQ](https://www.teluq.ca)
- [Université de Moncton](http://www.umoncton.ca/)
- [Université de Montréal](https://www.umontreal.ca)
- [Université de Sherbrooke](https://www.usherbrooke.ca)
- [Université du Québec](http://www.uquebec.ca)
- [Université du Québec en Abitibi-Témiscamingue](https://www.uqat.ca)
- [Université du Québec en Outaouais](https://uqo.ca)
- [Université du Québec à Chicoutimi](https://www.uqac.ca)
- [Université du Québec à Montréal](https://uqam.ca)
- [Université du Québec à Rimouski](https://www.uqar.ca)
- [Université du Québec à Trois-Rivières](https://www.uqtr.ca)
- [Vancouver Island University](https://www.viu.ca/)
- [Western University](https://uwo.ca)
- [Wilfrid Laurier University](https://wlu.ca)
- [Women's College Hospital](http://www.womenscollegehospital.ca/)
- [York University](https://www.yorku.ca)
- [École Nationale d'Administration Publique](https://enap.ca)
- [École de Technologie Supérieure](https://www.etsmtl.ca)

</details>

## Institutions from Qatar 

<details>

- [Qatar National Library](https://www.qnl.qa/en)

</details>

## Institutions from Malawi 

<details>

- Malawi-Liverpool-Wellcome Clinical Research-Programme

</details>

## Institutions from Thailand 

<details>

- Mahidol Oxford Tropical Medicine Research Unit

</details>

## Institutions from Vietnam 

<details>

- Oxford University Clinical Research Unit

</details>

## Institutions from Greece 

<details>

- [OpenAIRE (FP7 Post-Grant OA Pilot)](https://digital-strategy.ec.europa.eu/en/news/results-fp7-post-grant-open-access-pilot)

</details>

## Institutions from the Netherlands 

<details>

- [Academic Medical Center (AMC)](https://www.amc.nl/web/home.htm)
- [Academisch Centrum Tandheelkunde Amsterdam (ACTA)](https://acta.nl/en/)
- [Delft University of Technology](https://www.tudelft.nl/en/)
- [Eindhoven University of Technology](https://www.tue.nl/en/)
- [Erasmus University Medical Center](https://www.erasmusmc.nl/en/)
- [Erasmus University Rotterdam](https://www.eur.nl/en)
- [Hubrecht Institute for Developmental Biology and Stem Cell Research](https://www.hubrecht.eu/)
- [International Institute of Social History (IISH)](https://iisg.amsterdam/en)
- [Leiden University](https://www.universiteitleiden.nl/en)
- [Leiden University Medical Center (LUMC)](https://www.lumc.nl/)
- [Maastricht University](https://www.maastrichtuniversity.nl/)
- [Maastricht University Medical Center (UMC+)](https://www.mumc.nl/en)
- [Meertens Institute](https://meertens.knaw.nl/en/)
- [Netherlands Institute for Advanced Study in the Humanities and Social Sciences (NIAS)](https://nias.knaw.nl/)
- [Netherlands Institute for Neuroscience](https://nin.nl/)
- [Netherlands Institute of Ecology](https://nioo.knaw.nl/en)
- [Netherlands Interdisciplinary Demographic Institute (NIDI)](https://nidi.nl/en/)
- [Open University of The Netherlands](https://www.ou.nl/en/)
- [Radboud University](https://www.ru.nl/en)
- [Radboud University Medical Center](https://www.radboudumc.nl/en/research)
- [Rathenau Institute](https://www.rathenau.nl/en)
- [Royal Netherlands Academy of Arts and Sciences Bureau (KNAW Bureau)](https://www.knaw.nl/en)
- [Tilburg University](https://www.tilburguniversity.edu/)
- [University Medical Center Groningen (UMCG)](https://www.umcg.nl/)
- [University Medical Center Utrecht](https://www.umcutrecht.nl/en)
- [University of Amsterdam](https://www.uva.nl/en)
- [University of Groningen](https://www.rug.nl/)
- [University of Twente](https://www.utwente.nl/en/)
- [Utrecht University](https://www.uu.nl/en)
- [VU University Amsterdam](https://vu.nl/en)
- [VU University Medical Center (VUmc)](https://www.vumc.nl/)
- [Wageningen University and Research Centre](https://www.wur.nl/en.htm)
- [Westerdijk Fungal Biodiversity Center (CBS)](https://wi.knaw.nl/)

</details>

## Institutions from Liechtenstein 

<details>

- [University of Liechtenstein](https://www.uni.li/study/de/)

</details>

## Institutions from Ireland 

<details>

- [Atlantic Technological University](https://www.atu.ie)
- [Dublin City University](https://www.dcu.ie/)
- [Dublin Institute for Advanced Studies](https://www.dias.ie/)
- [Dundalk Institute of Technology](https://www.dkit.ie/)
- [Dún Laoghaire Institute of Art, Design and Technology](https://iadt.ie/)
- [Mary Immaculate College](https://www.mic.ul.ie/)
- [Maynooth University](https://www.maynoothuniversity.ie/)
- [Munster Technological University](https://www.mtu.ie/)
- [Royal College of Surgeons in Ireland](https://www.rcsi.com/dublin)
- [South East Technological University](https://www.setu.ie/)
- [Teagasc - The Irish Agriculture and Food Development Authority](https://www.teagasc.ie/)
- [Technological University Dublin](https://www.tudublin.ie/)
- [Technological University of the Shannon: Midlands Midwest](https://tus.ie/)
- [Trinity College Dublin](https://www.tcd.ie/)
- [University College Cork](https://www.ucc.ie/en/)
- [University College Dublin](https://www.ucd.ie/)
- [University of Galway](https://www.universityofgalway.ie/)
- [University of Limerick](https://www.ul.ie/)

</details>

## Data sets

*Note: The following numbers and plots are always based on the [latest revision](https://github.com/OpenAPC/openapc-de/releases/latest) of the OpenAPC data set. The underlying code can be found in the associated [R Markdown template](README.Rmd).*

### Articles (APCs)



The article data set contains information on 261,097 open access journal articles being published in fully and hybrid open access journal. Publication fees for these articles were supported financially by 481 research performing institutions and research funders. 

In total, article publication fee spending covered by the OpenAPC initiative amounted to € 535,264,785. The average payment was € 2,050 and the median was € 1,897.

195,082 articles in the data set were published in fully open access journals. Total spending on publication fees for these articles amounts to € 365,493,823, including value-added tax; the average payment was € 1,874 (median =  € 1,746, SD = € 909).

Hybrid open access journals rely on both publication fees and subscriptions as revenue source. 66,015 articles in the data set were published in hybrid journals. Total expenditure amounts to 169,770,962 €; the average fee was € 2,572 (median =  € 2,512, SD = € 1,147).

#### Spending distribution over fully and hybrid open access journals



![](figure/boxplot_oa.png)

#### Spending distribution details



|period | OA articles| OA mean| OA median|   OA min - max| Hybrid Articles| Hybrid mean| Hybrid median| Hybrid min - max|
|:------|-----------:|-------:|---------:|--------------:|---------------:|-----------:|-------------:|----------------:|
|2005   |           7|     858|       871| 480.0 -  1,350|               1|       2,983|         2,983| 2,983.3 -  2,983|
|2006   |          52|   1,021|     1,095| 665.0 -  1,340|              NA|          NA|            NA|               NA|
|2007   |          88|   1,081|     1,062| 870.0 -  1,825|              NA|          NA|            NA|               NA|
|2008   |         205|   1,170|     1,025| 440.8 -  2,830|               1|       2,660|         2,660| 2,660.0 -  2,660|
|2009   |         359|   1,185|     1,060| 124.6 -  4,386|              NA|          NA|            NA|               NA|
|2010   |         401|   1,261|     1,139| 158.8 -  7,419|               3|       2,318|         2,173| 2,152.0 -  2,630|
|2011   |         776|   1,156|     1,127| 104.8 -  4,666|               7|       1,835|         2,097|   552.0 -  2,631|
|2012   |       1,577|   1,173|     1,175|  69.0 -  4,498|              20|       2,308|         2,412|   997.4 -  2,700|
|2013   |       2,473|   1,229|     1,178|  50.0 -  4,574|           1,098|       2,257|         2,260|   120.2 -  4,679|
|2014   |       5,188|   1,375|     1,255|  40.0 -  9,028|           6,525|       2,238|         2,200|   132.3 -  6,000|
|2015   |       8,477|   1,523|     1,451|  59.0 -  5,669|           6,693|       2,609|         2,621|   126.6 -  8,636|
|2016   |       9,850|   1,637|     1,531|  62.5 -  5,985|           7,893|       2,551|         2,514|     2.3 -  9,079|
|2017   |      14,977|   1,701|     1,553|   8.7 - 14,634|          10,644|       2,528|         2,469|    36.9 -  9,858|
|2018   |      16,256|   1,701|     1,582|  13.0 -  8,926|           9,481|       2,551|         2,538|     1.8 -  9,073|
|2019   |      17,797|   1,706|     1,633|  10.7 -  7,684|           7,121|       2,535|         2,498|    75.3 -  9,500|
|2020   |      21,933|   1,725|     1,688|   0.2 -  8,906|           4,573|       2,497|         2,534|    16.6 -  7,416|
|2021   |      26,836|   1,830|     1,795|  27.0 -  8,341|           3,621|       2,561|         2,513|    30.2 - 11,400|
|2022   |      30,026|   2,104|     1,999|  12.4 - 11,175|           3,146|       2,903|         2,730|     2.1 - 14,607|
|2023   |      26,918|   2,306|     2,163|  17.4 -  9,893|           3,491|       3,010|         2,817|   106.4 - 11,895|
|2024   |      10,320|   2,444|     2,345|  40.0 - 10,030|           1,616|       3,258|         3,066|    28.4 - 13,044|
|2025   |         566|   2,329|     2,321| 100.0 -  8,854|              81|       3,402|         3,468|   200.0 -  8,095|



#### Additional Costs for articles



In addition to APCs, additional costs have been reported for 568 articles, totalling € 329,201. The following table shows an overview of the different cost types:



|Cost Type      | Number of Articles| Total Sum (€)|
|:--------------|------------------:|-------------:|
|colour charge  |                 71|        96,682|
|cover charge   |                 12|        15,626|
|other          |                208|        33,724|
|page charge    |                188|       177,075|
|payment fee    |                 72|         3,038|
|reprint        |                  5|         2,207|
|submission fee |                 12|           848|



This plot shows the cost distribution grouped by publishers. It includes only articles where additional reports have been reported and summarizes both additional costs and APCs for all of them:

![](figure/additional_costs.png)

### Books (BPCs)

The book data set contains information on 2,355 open access books. Publication fees were supported financially by 102 research performing institutions and funders. 

In total, book processing charges covered by the OpenAPC initiative amounted to € 15,596,693. The average payment was € 6,623 and the median was € 6,599.

Books can be made Open Access right from the beginning ("frontlist") or only retroactively after having been published traditionally in the first place ("backlist"), which can have a big influence on the paid BPCs.

#### Spending distribution over frontlist and backlist OA books



![](figure/boxplot_bpcs.png)

#### Spending distribution details



|period | Frontlist books| mean BPC| median BPC|  BPC min - max| Backlist books| mean BPC| median BPC| BPC min - max|
|:------|---------------:|--------:|----------:|--------------:|--------------:|--------:|----------:|-------------:|
|2014   |              62|   15,043|     16,000| 1,663 - 20,000|             NA|       NA|         NA|            NA|
|2015   |              44|   14,676|     14,000| 8,000 - 20,000|             NA|       NA|         NA|            NA|
|2016   |              42|   12,449|     14,000| 1,190 - 22,000|             NA|       NA|         NA|            NA|
|2017   |             184|    9,250|      8,780| 1,075 - 21,000|            195|    1,981|      1,981| 1,981 - 1,981|
|2018   |             149|    8,925|      8,250|   476 - 21,104|            191|    1,875|      1,875| 1,875 - 1,875|
|2019   |             173|    7,794|      8,250|   774 - 22,000|            194|    1,876|      1,875| 1,875 - 1,981|
|2020   |             165|    7,469|      7,380|   802 - 19,200|              2|    1,235|      1,235|   595 - 1,875|
|2021   |             176|    6,995|      6,561|   595 - 18,000|             NA|       NA|         NA|            NA|
|2022   |             231|    7,605|      6,902| 1,000 - 50,000|              1|    3,467|      3,467| 3,467 - 3,467|
|2023   |             347|    6,712|      6,000|   265 - 22,000|              7|    1,693|      1,464|   280 - 3,350|
|2024   |             175|    7,689|      6,400|   402 - 46,372|              2|    5,059|      5,059| 2,559 - 7,558|
|2025   |              15|    5,602|      4,165| 1,437 - 12,000|             NA|       NA|         NA|            NA|




## Use of external sources

Metadata representing publication titles or publisher names is obtained from Crossref in order to avoid extensive validation of records. Cases where we don't re-use information from Crossref to disambiguate the spending metadata are documented [here](python/test/test_apc_csv.py). Moreover, indexing coverage in Europe PMC and the Web of science is automatically checked.

### Articles 

|Source     |Variable  |Description                     |
|:--------------|:---------|:-----------------------------------------------|
|CrossRef   |`publisher` |Title of Publisher             |
|CrossRef   |`journal_full_title` |Full title of the journal  |
|CrossRef   |`issn` |International Standard Serial Numbers (collapsed) |
|CrossRef   |`issn_print` |ISSN print |
|CrossRef   |`issn_electronic`  |ISSN electronic        |
|CrossRef   |`license_ref`  |License of the article     |
|CrossRef   |`indexed_in_crossref`  |Is the article metadata registered with CrossRef? (logical)    |
|EuropePMC    |`pmid`  |PubMed ID                 |
|EuropePMC    |`pmcid` |PubMed Central ID         |
|Web of Science |`ut` |Web of Science record ID             |
|DOAJ           |`doaj` |Is the journal indexed in the DOAJ? (logical)    |

### Books

|Source     |Variable  |Description                     |
|:--------------|:---------|:-----------------------------------------------|
|CrossRef   |`publisher` |Title of Publisher             |
|CrossRef   |`book_title` |Full Title of a Book  |
|CrossRef   |`isbn` |International Standard Book Number |
|CrossRef   |`isbn_print` |ISBN print |
|CrossRef   |`isbn_electronic`  |ISBN electronic        |
|CrossRef   |`license_ref`  |License of the article     |
|CrossRef   |`indexed_in_crossref`  |Is the article metadata registered with CrossRef? (logical)    |
|DOAB           |`doab` |Is the book indexed in the DOAB? (logical)    |




### Indexing coverage

|Identifier                 | Coverage (articles)                                               | Coverage (Books)                                            |
|:--------------------------|:------------------------------------------------------------------|-------------------------------------------------------------|
|DOI                        |  99.77%       |89.04%   |
|PubMed ID                  |  73.39%      | NA                                                          |
|PubMed Central ID          |  67.87%     | NA                                                          |
|Web of Science record ID   | 63.11%         | NA                                                          |





## License

The data sets are made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/

This work is licensed under the Creative Commons Attribution 4.0 Unported License.

## How to cite?

When citing this data set, please indicate the [release](https://github.com/OpenAPC/openapc-de/releases/) you are referring to. The releases also contain information on contributors relating to the respective release.

Please do not cite the master branch of the Github repository (https://github.com/OpenAPC/openapc-de/tree/master/), but use the release numbers/tags.

Bielefeld University Library archives a copy (including commit history). To cite:

{Contributors:} *Datasets on fee-based Open Access publishing across German Institutions*. Bielefeld University. [10.4119/UNIBI/UB.2014.18](http://dx.doi.org/10.4119/UNIBI/UB.2014.18)

## Acknowledgement

This project was set up in collaboration with the [DINI working group Electronic Publishing](http://dini.de/ag/e-pub1/). It follows [Wellcome Trust example to share data on paid APCs](http://blog.wellcome.ac.uk/2014/03/28/the-cost-of-open-access-publishing-a-progress-report/) and recognises efforts from [JISC](https://www.jisc-collections.ac.uk/News/Releasing-open-data-about-Total-Cost-of-Ownership/) and the [ESAC initative](http://esac-initiative.org/) to standardise APC reporting.

## Contributors

Jens Harald Aasheim, Sarah Abusaada, Benjamin Ahlborn, Chelsea Ambler, Magdalena Andrae, Jochen Apel, Mauro Apostolico, Karina Barros Ferradás, Myriam Bastin, Hans-Georg Becker, Roland Bertelmann, Daniel Beucke, Manuela Bielow, Jochen Bihn, Peter Blume, Ute Blumtritt, Sabine Boccalini, Stefanie Bollin, Katrin Bosselmann, Valentina Bozzato, Kim Braun, Christoph Broschinski, Paolo Buoso, Cliff Buschhart, Dorothea Busjahn, Pablo de Castro, Ann-Kathrin Christann, Roberto Cozatl, Micaela Crespo Quesada, Amanda Cullin, Patrick Danowski, Gernot Deinzer, Julia Dickel, Andrea Dorner, Stefan Drößler, Karin Eckert, Carsten Elsner, Clemens Engelhardt, Olli Eskola, Katrin Falkenstein-Feldhoff, Ashley Farley, Inken Feldsien-Sudhaus, Silke Frank, Fabian Franke, Claudia Frick, Marléne Friedrich, Paola Galimberti, Elena Gandert, Agnes Geißelmann, Kai Karin Geschuhn, Silvia Giannini, Marianna Gnoato, Larissa Gordon, Paul Gredler, Steffi Grimm, Ute Grimmel-Holzwarth, Evgenia Grishina, Christian Gutknecht, Birgit Hablizel, Florian Hagen, Uli Hahn, Kristina Hanig, Margit L. Hartung, Julia Heitmann-Pletsch, Dominik Hell, Christina Hemme, Eike Hentschel, Ulrich Herb, Stephanie Herzog, Elfi Hesse, Silke Hillmann, Kathrin Höhner, Dana Horch, Conrad Hübler, Christie Hurrell, Arto Ikonen, Simon Inselmann, Doris Jaeger, Najko Jahn, Alexandra Jobmann, Daniela Jost, Tiina Jounio, Juho Jussila, Nadja Kalinna, Mirjam Kant, Kerstin Klein, Andreas Kennecke, Robert Kiley, Ilka Kleinod, Lydia Koglin, Nives Korrodi, Biljana Kosanovic, Stephanie Kroiß, Gerrit Kuehle, Stefanie Kutz, Marjo Kuusela, Anna Laakkonen, Ignasi Labastida i Juan, Gerald Langhanke, Inga Larres, Sarah Last, Stuart Lawson, Anne Lehto, Sari Leppänen, Camilla Lindelöw, Maria Löffler, Jutta Lotz, Kathrin Lucht-Roussel, Susanne Luger, Ute von Lüpke, Jan Lüth, Frank Lützenkirchen, Steffen Malo, Anna Marini, Manuel Moch, Vlatko Momirovski, Andrea Moritz, Max Mosterd, Marcel Nieme, Anja Oberländer, Martina Obst, Jere Odell, Linda Ohrtmann, Vitali Peil, Gabriele Pendorf, Mikko Pennanen, Dirk Pieper, Tobias Pohlmann, Thomas Porquet, Markus Putnings, Andrée Rathemacher, Rainer Rees-Mertins, Edith Reschke, Ulrike Richter, Katharina Rieck, Friedrich Riedel, Simone Rosenkranz, Florian Ruckelshausen, Steffen Rudolph, Ilka Rudolf, Pavla Rygelová, Lea Satzinger, Annette Scheiner, Isabo Schick, Michael Schlachter, Birgit Schlegel, Andreas Schmid, Barbara Schmidt, Katharina Schulz, Stefanie Seeh, Barbara Senkbeil-Stoffels, Adriana Sikora, Tereza Simandlová, Stefanie Söhnitz, Jana Sonnenstuhl, Lisa Spindler, Susanne Stemmler, Matti Stöhr, Eva Stopková, Marius Stricker, Andrea Stühn, Kálmán Szőke, Linda Thomas, Anne Timm, Laura Tobler, Johanna Tönsing, Marco Tullney,  Milan Vasiljevic, Astrid Vieler, Lena Vinnemann, Viola Voß, Christin Wacke, Roland Wagner, Agnieszka Wenninger, Kerstin Werth, Martin Wimmer, Marco Winkler, Sabine Witt, Michael Wohlgemuth, Verena Wohlleben, Qingbo Xu, Philip Young, Esther Zaugg, Miriam Zeunert, Philipp Zumstein

## Contact

For bugs, feature requests and other issues, please submit an issue via [Github](https://github.com/OpenAPC/openapc-de/issues/new).

For general comments, email openapc at uni-bielefeld.de

## Disclaimer

People, who are looking for "Open Advanced Process Control Software" for automation, visualization and process control tasks from home control up to industrial automation, please follow <http://www.openapc.com> (2015-09-30)
