#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import logging
import os
import sys

import openapc_toolkit as oat

TARGET_DIR = "opencost_out"
TA_FILE = "../data/transformative_agreements/transformative_agreements.csv"
WILEY_OPT_OUT_FILE = "../data/transformative_agreements/deal_germany_opt_out/deal_wiley_germany_opt_out.csv"
SPRINGER_OPT_OUT_FILE = "../data/transformative_agreements/deal_germany_opt_out/deal_springer_nature_germany_opt_out.csv"

ROR_MAP = {}

INS_STR = {
    "sn2020deal": "DEAL Springer Nature Germany",
    "wiley2019deal": "DEAL Wiley Germany",
    "els2023deal": "DEAL Elsevier Germany",
    "ov_hdr": "=== Overview: Contract group IDs ===\n\n",
    "ov_report": "{} has reported {} cost data for the {} period, total costs: {} €. (group_id: {})\n",
    "ov_articles": "{} articles without publication-level costs were linked to this group id. A preliminary EAPC of {} / {} = {} was assigned to each of them.\nCONTROL: First new article in group ({}) has an 'euro' value of {} €. ==> {}.\n",
    "ov_no_articles": "There were no articles without publication-level costs linked to this group id.\n",
    "ov_ta_data": "IMPORTANT: The institution has already reported TA DEAL data for the given period and publisher ({} articles, EAPC: {} €). EAPC needs to be updated, see below.\n",
    "ov_other_group": "IMPORTANT: There is another invoice group with cost data for the given institution, period and publisher. EAPC needs to be updated, see below.\n",
    "ins_hdr": "=== Update instructions ===\n\n",
    "ins_clear": "There is no conflicting cost data for invoice group '{}', the calculated EAPC is valid.\n ==> The data file ({}, {}, {}) can be directly enriched and processed.\n\n",
    "ins_no_articles": "There are no articles linked to the cost data in all invoice groups related to {} {} and no matching TA data exists.\n ==> Nothing to do here.\n\n",
    "ins_not_clear": "There is existing TA DEAL data and/or additional invoice groups for the agreement period {} {}.\n ==> EAPC needs to be updated.\n\n",
    "recalc_hdr": "  data_source                                            num_articles         total_costs (€)\n",
    "recalc_hbar": "  -------------------------------------------------------------------------------------------\n",
    "recalc_res": "  New EAPC: {} / {} = {}\n\n",
    "recalc_update_ta": " ==> Existing DEAL data ({}, {}, {}) has to be updated with the new EAPC ({}) as euro value ({} articles in original file(s), enriched file(s) and TA collection).\n",
    "recalc_opt_out": " IMPORTANT: Please note that some articles are located in the {} opt-out file, those have to be updated as well.\n",
    "recalc_update_group": " ==> New DEAL data ({}, {}, {}) has to be updated with the new EAPC ({}) as euro value before enrichment ({} articles).\n",
}

def create_deal_update_instructions(args, ta_data, new_data, invoice_groups):
    deal_map = {}
    instructions = {}
    # Create a unified lookup structure containing all cost data (new group_ids and old TA data) for any ins/period/agreement combo.
    for group in invoice_groups:
        if group["contract_id"] not in ["sn2020deal", "wiley2019deal", "els2023deal"]:
            continue
        ror_id = group["institution_ror"]
        ins_name = ROR_MAP[ror_id]
        period = group["period"]
        agreement = INS_STR[group["contract_id"]]
        group_id = group["group_id"]
        total_cost = group["group_total_costs"]
        if ins_name not in deal_map:
            deal_map[ins_name] = {}
        if period not in deal_map[ins_name]:
            deal_map[ins_name][period] = {}
        if agreement not in deal_map[ins_name][period]:
            deal_map[ins_name][period][agreement] = {
                "groups": [],
                "ta_data": None
            }
        articles = new_data.get(ins_name, {}).get(period, {}).get(agreement, [])
        deal_map[ins_name][period][agreement]["groups"].append({
            "num_articles": len(articles),
            "total_cost": total_cost,
            "group_id": group_id
        })
        if deal_map[ins_name][period][agreement]["ta_data"] is None:
            old_articles = ta_data.get(ins_name, {}).get(period, {}).get(agreement, {}).get("data", [])
            if len(old_articles) > 0:
                old_eapc = float(old_articles[0]["euro"])
                deal_map[ins_name][period][agreement]["ta_data"] = {
                    "num_articles": len(old_articles),
                    "total_cost": len(old_articles) * old_eapc,
                    "opt_out": ta_data[ins_name][period][agreement]["opt_out_articles"]
                }
        # Report on all invoice groups
        if ins_name not in instructions:
            instructions[ins_name] = INS_STR["ov_hdr"]
        ins_txt = INS_STR["ov_report"].format(ins_name, INS_STR[group["contract_id"]], period, total_cost, group_id)
        if len(articles) > 0:
            eapc = round(float(total_cost) / len(articles), 2)
            passed = "passed" if int(eapc) == int(articles[0]["euro"]) else "FAILED!"
            ins_txt += INS_STR["ov_articles"].format(len(articles), total_cost, len(articles), eapc, articles[0]["doi"], articles[0]["euro"], passed)
        else:
            ins_txt += INS_STR["ov_no_articles"]
        if len(old_articles) > 0:
            ins_txt += INS_STR["ov_ta_data"].format(len(old_articles), old_eapc)
        if len(deal_map[ins_name][period][agreement]["groups"]) > 1:
            ins_txt += INS_STR["ov_other_group"]
        instructions[ins_name] += ins_txt + "\n"

    # Create update instructions
    for ins_name, periods in deal_map.items():
        instructions[ins_name] += INS_STR["ins_hdr"]
        ins_index = 0
        for period, agreements in periods.items():
            for agreement, data in agreements.items():
                # sum up data and generate preliminary EAPC Recalculation text
                ins_index += 1
                total_costs = 0.0
                total_articles = 0
                groups_total_articles = 0
                ta_total_articles = 0
                calc_str = INS_STR["ins_not_clear"].format(agreement, period)
                calc_str += " = Recalculation = \n" + INS_STR["recalc_hdr"] + INS_STR["recalc_hbar"]
                for group in data["groups"]:
                    total_costs += group["total_cost"]
                    total_articles += group["num_articles"]
                    groups_total_articles += group["num_articles"]
                    calc_str += "  " + group["group_id"].ljust(55) + str(group["num_articles"]).ljust(20) + str(group["total_cost"]) + "\n"
                if data["ta_data"] is not None:
                    ta = data["ta_data"]
                    total_costs += ta["total_cost"]
                    total_articles += ta["num_articles"]
                    ta_total_articles = ta["num_articles"]
                    calc_str += "  " + "TA data".ljust(55) + str(ta["num_articles"]).ljust(20) + str(ta["total_cost"]) + "\n"
                calc_str += INS_STR["recalc_hbar"]
                calc_str += "  " + "Sum".ljust(55) + str(total_articles).ljust(20) + str(total_costs) + "\n\n"
                if total_articles > 0:
                    new_eapc = round(total_costs / total_articles, 2)
                    calc_str += INS_STR["recalc_res"].format(total_costs, total_articles, new_eapc)
                    if ta_total_articles > 0:
                        calc_str += INS_STR["recalc_update_ta"].format(ins_name, agreement, period, new_eapc, ta_total_articles)
                        if data["ta_data"]["opt_out"]:
                            calc_str += INS_STR["recalc_opt_out"].format(agreement)
                    if groups_total_articles > 0:
                        calc_str += INS_STR["recalc_update_group"].format(ins_name, agreement, period, new_eapc, groups_total_articles)
                    calc_str += "\n"
                instructions[ins_name] += str(ins_index) + ") "
                if total_articles == 0:
                    instructions[ins_name] += INS_STR["ins_no_articles"].format(agreement, period)
                elif len(data["groups"]) == 1 and data["ta_data"] is None:
                    instructions[ins_name] += INS_STR["ins_clear"].format(data["groups"][0]["group_id"], ins_name, agreement, period)
                else:
                    instructions[ins_name] += calc_str

    for ins_name, ins_txt in instructions.items():
        ins_file_name = ins_name.lower().replace(" ", "_")
        ins_file_name += "_DEAL_calculations.txt"
        with open(os.path.join(TARGET_DIR, args.prefix + ins_file_name), "w") as handle:
            handle.write(ins_txt)

parser = argparse.ArgumentParser()
parser.add_argument("xml_files", nargs="+", help="One or more openCost XML files which should validate against the official openCost XSD schema")
parser.add_argument("-v", "--version", choices=["v1", "v2"], default="v1")
parser.add_argument("-p", "--prefix", default="", help="An optional prefix for generated file names")
parser.add_argument("-l", "--log_level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Set the log level of the underlying openCost toolkit library")

args = parser.parse_args()

if args.version == "v1":
    import opencost_toolkit as octk
else:
    import opencost_toolkit_v2 as octk

xml_content_strings = []

for path in args.xml_files:
    if os.path.isfile(path):
        with open(path) as f:
            content = f.read()
            xml_content_strings.append(content)
            
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(oat.ANSIColorFormatter())
bufferedHandler = oat.BufferedErrorHandler(handler)
bufferedHandler.setFormatter(oat.ANSIColorFormatter())
logging.root.addHandler(handler)
logging.root.addHandler(bufferedHandler)
logging.root.setLevel(args.log_level)
logging.debug("Logger initialized.")

articles, invoice_groups = octk.process_opencost_xml(*xml_content_strings)
articles = octk.apply_contract_data(articles, invoice_groups)

with open(oat.INSTITUTIONS_FILE, "r") as ins_file:
    reader = csv.DictReader(ins_file)
    for line in reader:
        ROR_MAP[line["ror_id"]] = line["institution"]

for collection in [articles, invoice_groups]:
    for element in collection:
        ror_id = element["institution_ror"]
        new_ror_msg = "Encountered a ROR ID ({}) which is not present in the institutions table. {}"
        if oat.has_value(ror_id) and ror_id not in ROR_MAP:
            ror_request = oat.get_metadata_from_ror(ror_id)
            if ror_request["success"]:
                institution = ror_request["data"]["institution"]
                ROR_MAP[ror_id] = institution
                msg = new_ror_msg.format(ror_id, "It belongs to this institution: ")
                msg += institution
                logging.info(msg)
            else:
                msg = new_ror_msg.format(ror_id, "A ROR lookup failed: ")
                msg += ror_request["error_msg"]
                logging.error(msg)
        element["institution"] = ROR_MAP.get(ror_id, "")

fieldnames = list(octk.OPENCOST_EXTRACTION_FIELDS.keys())

if not os.path.isdir(TARGET_DIR):
    os.mkdir(TARGET_DIR)

csv_writers = {}

all_articles_path = os.path.join(TARGET_DIR, "all_articles.csv")

with open(all_articles_path, "w") as out:
    main_writer = csv.DictWriter(out, fieldnames)
    main_writer.writeheader()
    for article in articles:
        main_writer.writerow(article)
        institution = article["institution"]
        esac_id = article["contract_primary_identifier"]
        pub_type = article["type"]
        ins_name = institution.lower().replace(" ", "_")
        period = article["period"]
        deal_data = None
        if pub_type == "book":
            ins_name += "_BPC"
        elif article["is_hybrid"] == "TRUE":
            if esac_id == "sn2020deal":
                ins_name += "_DEAL_Springer_" + period
                deal_data = {
                    "period": period,
                    "institution": institution,
                    "agreement": "DEAL Springer Nature Germany"
                }
            elif esac_id == "wiley2019deal":
                ins_name += "_DEAL_Wiley_" + period
                deal_data = {
                    "period": period,
                    "institution": institution,
                    "agreement": "DEAL Wiley Germany"
                }
            elif esac_id == "els2023deal":
                ins_name += "_DEAL_Elsevier_" + period
                deal_data = {
                    "period": period,
                    "institution": institution,
                    "agreement": "DEAL Elsevier Germany"
                }
            elif oat.has_value(esac_id):
                # Skip contracts other than DEAL
                continue
        if ins_name not in csv_writers:
            path = os.path.join(TARGET_DIR, args.prefix + ins_name + ".csv")
            handle = open(path, "w")
            csv_writers[ins_name] = {
                "writer": csv.DictWriter(handle, fieldnames),
                "handle": handle,
                "articles": [],
                "deal_data": deal_data
            }
            csv_writers[ins_name]["writer"].writeheader()
        csv_writers[ins_name]["articles"].append(article)

ta_deal_data = {}
# Extract existing DEAL data and create a nested lookup dict
for source in [TA_FILE, WILEY_OPT_OUT_FILE, SPRINGER_OPT_OUT_FILE]:
    with open(source, "r") as ta_file:
        reader = csv.DictReader(ta_file)
        for line in reader:
            institution = line["institution"]
            agreement = line["agreement"]
            if line["is_hybrid"] != "TRUE":
                continue
            if agreement not in ["DEAL Springer Nature Germany", "DEAL Wiley Germany", "DEAL Elsevier Germany"]:
                continue
            period = str(line["period"])
            if institution not in ta_deal_data:
                ta_deal_data[institution] = {}
            if period not in ta_deal_data[institution]:
                ta_deal_data[institution][period] = {}
            if agreement not in ta_deal_data[institution][period]:
                ta_deal_data[institution][period][agreement] = {
                    "data": [],
                    "opt_out_articles": False,
                }
            ta_deal_data[institution][period][agreement]["data"].append(line)
            if source in [WILEY_OPT_OUT_FILE, SPRINGER_OPT_OUT_FILE]:
                ta_deal_data[institution][period][agreement]["opt_out_articles"] = True

new_deal_data = {}
# Also create a nested lookup dict for incoming DEAL data
for _, data in csv_writers.items():
    if data["deal_data"] is None:
        continue
    ins = data["deal_data"]["institution"]
    period = data["deal_data"]["period"]
    agreement = data["deal_data"]["agreement"]
    if ins not in new_deal_data:
        new_deal_data[ins] = {}
    if period not in new_deal_data[ins]:
        new_deal_data[ins][period] = {}
    if agreement not in new_deal_data[ins][period]:
        new_deal_data[ins][period][agreement] = data["articles"]

# Create institutional output files
for writer_name, writer_data in csv_writers.items():
    for article in writer_data["articles"]:
        writer_data["writer"].writerow(article)
    writer_data["handle"].close()

create_deal_update_instructions(args, ta_deal_data, new_deal_data, invoice_groups)

# Flush buffered log messages
bufferedHandler.close()
