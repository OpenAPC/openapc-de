

# OpenAPC Data SNSF

## History of APCs at the SNSF

| Date |Event  |
|--|--|
|Since 2008|Grantees are encouraged to publish in Gold OA journals. Yet the coverage of APCs was not explicitly regulated. |
|2013.10 |APCs up to 3000 CHF were explicitly allowed to be a part of the project costs (also applied to grants approved before this date).|
|2016.05 |First [OA-Monitoring Report 2013 - 2015](http://doi.org/10.5281/zenodo.584131). It contains an estimation of paid APCs by the SNSF after an sample-based review of financial reports for costs related to publications between October 2013 and August 2015 of the key funding schemes.
|2017.05 |With mySNF Release 6 it became possible to  add APCs as a specific financial item in the budget plan of new grant applications.
|2018.01| An additional form was added to the section of the financial reports in mySNF, where grantees or their financial administration can explicitly report paid APCs and make a link to the publication in the output data section.|
|2018.01|First release of collected data to OpenAPC. Part of the data is the set of the first monitoring period 2013-2015. As this data was extracted from checking samples of financial reports it does not cover all paid APCs of this period. Through a more systematic screening for APCs, the data from 2016-2017 provides a more complete picture. However some paid APCs might have slipped through the screening process.  |
|2018.04|For new grant applications APCs are no longer part of the research budget but can be requested independently. The existing upper limit of 3000 CHF has been temporary removed as part of the [SNSF OA2020 policy](http://www.snf.ch/en/theSNSF/research-policies/open-access/Pages/default.aspx#OA%202020%20Policy).|
|2018.10|A new workflow has been established, where grantees can apply for payment/reimbursement of APCs also for grants that already have expired.|

## CHF to EUR Conversion

Financial Reporting at the SNSF is always done in Swiss Francs (CHF). For OpenAPC all amounts in CHF were converted to EUR. For the conversion, the annual average exchange rate available from the [Swiss National Bank](https://data.snb.ch/de/topics/ziredev#!/cube/devkua?fromDate=2010&toDate=2018&dimSel=D1(EUR1))) was used:

|Year|EUR|CHF|Remark|
|--|--|--|--|
|2009|1|1.51007||
|2010|1|1.38053||
|2011|1|1.23355||
|2012|1|1.20531||
|2013|1|1.23080||
|2014|1|1.21463||
|2015|1|1.06811||
|2016|1|1.09009||
|2017|1|1.11157||
|2018|1|1.15487||
|2019|1|1.12941|[Average Jan-Juni 2019](https://data.snb.ch/de/topics/ziredev#!/cube/devkum?fromDate=2019-01&toDate=2019-07&dimSel=D0(M0),D1(EUR1))| 

## Co-Funding

Some APCs haven't been entirely funded by the SNSF. This applies in particular to cases between October 2013 and March 2018, when there was an upper limit of CHF 3000 per APC. In such cases during the period with the cap, the SNSF usually covered CHF 3000 and the remaining payment was returned to the author and/or the university finance department.

If both paying institutions are represented at OpenAPC, the individual payments was stored in [data/apc_cofunding.csv](apc_cofunding.csv) see example 10.1038/srep25902. However, in cases where the other institutions do not yet provide data on OpenAPC, the entire amount is temporarily allocated to the SNSF. 

For those publications a further list [list of publication with co-funding](snsf_apc_cofunding.csv) in the snsf data folder was created. If another insitution reports a duplicate DOI please check if it is listed here and move it to [data/apc_cofunding.csv](apc_cofunding.csv).


## Hybrid

The SNSF does not support Hybrid  OA due to the issue of double dipping. Accidentally some Hybrid-OA charges have slipped trough the internal checking procedure. For the matter of transparence these Hybrid OA Charges are included here.

## Additional "local" information

For full transparency the [initial uploaded list](snsf_openapc.csv) contains some additional columns:

|name | description |
|--|--|
| chf | the paid amount for the APC (including VAT, discounts, transaction feeds) in Swiss Francs|
| conversion_rate | The applied conversion rate (see above) considering the publication year|
| invoice_original_amount | If available the original amount on the invoice (usually without transaction fees)|
| invoice_original_currency | The currency of the invoice|
| snsf_voucher_number | The voucher number of the SNSF internal accounting system (SAGE) used for the payment to the publisher or for the reimbursement. Only available for APCs which have been handled through the funding scheme for APCs (since October 2018).  |
| grant_snsf |The application in which the APC was processed. For "older" grants this is identical to "grant_snsf_related". Yet with the new funding scheme especially for APCs, this is the number for the APC-grant.|
| grant_snsf_related | In cases where the APC was part of the project funding, this project is mentioned. For the new funding scheme decicated to APC's, the related grant(s) are selected by the author to indicate the relation. A daily updated list of all SNSF projects is available and can be used to join other project information: http://p3.snf.ch/Pages/DataAndDocumentation.aspx |


## Contact

Christian Gutknecht
Coordination of information system in research support 
Swiss National Science Foundation (SNSF)
Wildhainweg 3, Postfach 8232, CH-3001 Bern
Phone: +41 31 308 24 52
cosi@snf.ch
