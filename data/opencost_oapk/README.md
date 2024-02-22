
## About

This directory contains cost data which has been collected from German institutions by the [Forschungszentrum Jülich](https://www.fz-juelich.de/en) (FZJ) as part of the DFG programme "Open-Access-Publikationskosten" ([Open Access Publication Funding](https://www.fz-juelich.de/en/zb/open-science/open-access/monitoring-dfg-oa-publication-funding)). When reporting their data, Institutions could optionally declare it to be reusable by OpenAPC.

On OpenAPC's side, the transfer, storing and processing of the data is part of the [openCost](https://www.opencost.de/en/) initiative, utilizing the [metadata schema](https://github.com/opencost-de/opencost/tree/main/doc) for cost data developed within that project.

## Contents

- oapk_Report_OpenCost_2023-11-22T16_08.xml: The original XML file transferred to OpenAPC by the FZJ. It contains cost data on both publications (APCs/BPCs) as well as payments for transformative agreements such as the DEAL contracts. The file format conforms to the metadata schema for publication costs created by the openCost project. Since the schema is still under development, the XML file should not be expected to validate against later versions, the current file is based on a snapshot from [August 2023](https://github.com/opencost-de/opencost/blob/be1b6870067b6d1bc34f90a9780f78f5c3341401/doc/opencost.xsd).

- opencost_out: This directory contains the extracted cost data from the XML input, transformed to OpenAPC compatible CSV.

 
