#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv

import openapc_toolkit as oat

import xml.etree.ElementTree as ET

ARG_HELP_STRINGS = {
    "oapk_xml_file": "the xml file to transform",
    "gold_dois": "a file containing dois which in fact belong to a deal agreement, each DOI one a single line",
    "esac_id": "the ESAC ID to use for the new part_of_contract",
    "contract_year": "the year part in the generated group_id"
}

namespaces = {
    "opencost": "https://opencost.de"
}

ins_map = oat._create_institution_map_dict("ror_id")

parser = argparse.ArgumentParser()
parser.add_argument("oapk_xml_file", help=ARG_HELP_STRINGS["oapk_xml_file"])
parser.add_argument("gold_dois", help=ARG_HELP_STRINGS["gold_dois"])
parser.add_argument("esac_id", help=ARG_HELP_STRINGS["esac_id"])
parser.add_argument("contract_year", help=ARG_HELP_STRINGS["contract_year"])
args = parser.parse_args()

ET.register_namespace("opencost", "https://opencost.de")
xpath_publication_with_doi_tmpl = "opencost:publication/opencost:primary_identifier/opencost:doi[.='{}']../.."

institutions_modified = []

tree = ET.parse(args.oapk_xml_file)
root = tree.getroot()
with open(args.gold_dois) as doi_file:
    for doi in doi_file:
        doi = doi.strip().lower()
        oat.print_c("Processing DOI " + doi + "...")
        xpath_publication_with_doi = xpath_publication_with_doi_tmpl.format(doi)
        publication = root.find(xpath_publication_with_doi, namespaces)
        if publication is not None:
            oat.print_g("    Found an openCost publication element with matching DOI.")
        else:
            oat.print_r("ERROR: Could not find an openCost publication element with matching DOI")
            continue
        ror_id_element = publication.find("opencost:institution/opencost:id/opencost:type[.='ror']../opencost:value", namespaces)
        if ror_id_element is not None:
            ror_id = ror_id_element.text
            if ror_id in ins_map:
                oat.print_g("    ROR ID extracted ({}), it belongs to {}.".format(ror_id, ins_map[ror_id]["institution"]))
            group_id = ror_id[16:] + "_" + args.esac_id + "_" + args.contract_year
            oat.print_g("    The generated group_id is: {}".format(group_id))
        else:
            oat.print_r("ERROR: Could not find a ROR ID inside the publication element")
            continue
        existing_poc = publication.find("opencost:cost_data/opencost:part_of_contract", namespaces)
        if existing_poc is not None:
            oat.print_r("ERROR: publication already has a part_of_contract")
            continue
        cost_data = publication.find("opencost:cost_data", namespaces)
        part_of_contract = ET.SubElement(cost_data, 'opencost:part_of_contract')
        primary_identifier = ET.SubElement(part_of_contract, 'opencost:primary_identifier')
        value = ET.SubElement(primary_identifier, 'opencost:value')
        value.text = args.esac_id
        id_type = ET.SubElement(primary_identifier, 'opencost:type')
        id_type.text = "ESAC"
        group_id_element = ET.SubElement(part_of_contract, 'opencost:group_id')
        group_id_element.text = group_id
        oat.print_g("part_of_contract appended successfully")
        institutions_modified.append(ins_map[ror_id]["institution"])
ET.indent(tree, '  ')
tree.write("out.xml", encoding="unicode", xml_declaration=True)
oat.print_c("At least one publication from the following institutions was re-assigned to DEAL: " + ", ".join(list(set(institutions_modified))))

