# OpenAPC Data SNSF

## History of APC handling at the SNSF

| Date |Event  |
|--|--|
|Since 2008|Grantees are encouraged to publish in Gold OA journals. Yet the coverage of APCs was not explicitly regulated. |
|2013.10 |APCs up to 3000 CHF were explicitly allowed to be a part of the project costs (also applied to grants approved before this date).|
|2016.05 |First [OA-Monitoring Report 2013 - 2015](http://doi.org/10.5281/zenodo.584131). It contains an estimation of paid APCs by the SNSF after an sample-based review of financial reports for costs related to publications between October 2013 and August 2015 of the key funding schemes.
|2017.05 |With mySNF Release 6 it became possible to  add APCs as a specific financial item in the budget plan of new grant applications.
|2018.01| An additional form was added to the section of the financial reports in mySNF, where grantees or their financial administration can explicitly report paid APCs and make a link to the publication in the output data section.|
|2018.01|First release of collected data to OpenAPC. Part of the data is the set of the first monitoring period 2013-2015. As this data was extracted from checking samples of financial reports it does not cover all paid APCs of this period. Through a more systematic screening for APCs, the data from 2016-2017 provides a more complete picture. However some paid APCs might have slipped through the screening process.  |
|2018.04|For new grant applications APCs are no longer part of the research budget but can be requested independently. The existing upper limit of 3000 CHF has been temporary removed as part of the [SNSF OA2020 policy](http://www.snf.ch/en/theSNSF/research-policies/open-access/Pages/default.aspx#OA%202020%20Policy).|
|2018.10|A [new workflow](https://oa100.snf.ch/en/funding/journal-articles/) has been established, where grantees can request the payment/refund of APCs even for grants that have already expired.|
|2021.06| [The SNSF has launched a pilot project: researchers will be able to publish their open access articles via the ChronosHub](https://www.snf.ch/en/3Vpw3ybQfivruCDi/news/open-access-simple-and-efficient-publishing-with-chronoshub) platform. The existing path to apply for OA publication grants at the SNSF continues to exist. The latest data delivery (2022-02-24) does include APCs from both ChronosHub and SNSF OA grants, the origin is distinguishable via  the variable `origin`.|
|2021.07| It was decided that the SNSF does only provide publications that do have a DOI. Publications without a DOI can be provided, when they have a title, a journal name, a journal ISSN, a publisher, and a link to a full-text available. Due to inavailability of all this data, around 15% of the SNSF's APC are not reported for publications without a DOI. 
|2023.02| All APC handling of the SNSF is now done by Chronoshub, therefore, the data delivery consists only of APC data of completed payments over Chronoshub. All APCs handled by Chronoshub do have a DOI. 

## CHF to EUR Conversion

Financial Reporting at the SNSF is always done in Swiss Francs (CHF). For OpenAPC all amounts in CHF were converted to EUR. For the conversion, the annual average exchange rate available from the [Swiss National Bank](https://data.snb.ch/de/topics/ziredev#!/cube/devkua?fromDate=2010&toDate=2020&dimSel=D1(EUR1))) was used:

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
|2019|1|1.11247||
|2020|1|1.07055||
|2021|1|1.09400|Average January-June 2021, delivery 2021-06-03|
|2021|1|1.0810|Whole publication year of 2021, delivery 2022-02-24|
|2022|1|1.0048|Whole publication year of 2022, delivery 2023-02-06|
|2023|1|0.9717|Whole publication year of 2023, delivery 2024-03-05 (as provided by Chronoshub on 2024-01-31)|

## Co-Funding

Some APCs haven't been entirely funded by the SNSF. This applies in particular to cases between October 2013 and March 2018, when there was an upper limit of CHF 3000 per APC. In such cases during the period with the cap, the SNSF usually covered CHF 3000 and the remaining payment was returned to the author and/or the university finance department.

If both paying institutions are represented at OpenAPC, the individual payments was stored in [snsf_apc_cofunding.csv](snsf_apc_cofunding.csv) see example 10.1038/srep25902. However, in cases where the other institutions do not yet provide data on OpenAPC, the entire amount is temporarily allocated to the SNSF.

For those publications a further list [list of publication with co-funding](snsf_apc_cofunding.csv) was created in the snsf data folder. Please get in touch if you want to claim the other part, so we can move the publication to [apc_cofunding.csv list of OpenAPC](https://github.com/OpenAPC/openapc-de/blob/master/data/apc_cofunding.csv)

## Hybrid

The SNSF does not support Hybrid OA due to the issue of double dipping. Accidentally some Hybrid-OA charges have slipped trough the internal checking procedure. For the matter of transparency, these Hybrid OA Charges are included here.

## Additional "local" information

For full transparency the initial uploaded lists (without "enriched" in the file name) contain some additional columns:

|name | description |
|--|--|
| `chf` | the paid amount for the APC (including VAT, discounts, transaction fees) in Swiss Francs|
| `conversion_rate` | The applied conversion rate (see above) considering the publication year|
| `invoice_original_amount` | If available the original amount on the invoice (usually without transaction fees) (for datasets up to 2020-11-25)|
| `invoice_original_currency` | The currency of the invoice (for datasets up to 2020-11-25)|
| `snsf_voucher_number` | The voucher number of the SNSF internal accounting system (SAGE) used for the payment to the publisher or for the reimbursement. Only available for APCs which have been handled through the funding scheme for APCs (since October 2018). Since January 2020 the number of the new accounting system Abacus is used. For APCs handled by Chronoshub, we provide the Chronoshub Payment Id in this field (payment dates 2021+). |
| `grant_snsf` |The application in which the APC was processed. For "older" grants this is identical to `grant_snsf_related`. Yet with the new funding scheme especially for APCs, this is the number for the APC-grant. When the field has an `NA` value, the APC was handled via Chronoshub and has no SNSF grant number.|
| `grant_snsf_related` | In cases where the APC was part of the funding scheme "project funding"", the respective project number is mentioned. For the funding scheme dedicated to APCs introduced in 2018, the related grant(s) are selected by the authors to indicate the relation. For APCs being handled by Chronoshub, this field contains the SNSF grant numbers as provided by Chronoshub, that is: the origin grants where the research funds come from. A daily updated list of all SNSF projects is available and can be used to join other project information: https://data.snf.ch/Exportcsv/Grant.csv |
| `title` | (Period 2021+) Title of the publication as 1) entered by the author or 2) as provided through Chronoshub. If we don't have any title available through 1) or 2), we query Crossref and provide the title in Crossref for this DOI.|
| `payment_date` | (Period 2021+) Exact date of the payment.|
| `origin` | (Period 2021+) Whether this APC was payed by the SNSF directly over `SNSF-OA-Grants` or whether it was payed indirectly over `Chronoshub`.|


## Contact

Data Team,
Swiss National Science Foundation (SNSF)
Wildhainweg 3, Postfach 8232, CH-3001 Bern
datateam@snf.ch

https://github.com/snsf-data
