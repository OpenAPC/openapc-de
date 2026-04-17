#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import logging
import os
import sys

from copy import deepcopy

import openapc_toolkit as oat

TARGET_DIR = "opencost_out"
TA_FILE = "../data/transformative_agreements/transformative_agreements.csv"
WILEY_OPT_OUT_FILE = "../data/transformative_agreements/deal_germany_opt_out/deal_wiley_germany_opt_out.csv"
SPRINGER_OPT_OUT_FILE = "../data/transformative_agreements/deal_germany_opt_out/deal_springer_nature_germany_opt_out.csv"

ROR_MAP = {}

parser = argparse.ArgumentParser()
parser.add_argument("xml_files", nargs="+", help="One or more openCost XML files which should validate against the official openCost XSD schema")
parser.add_argument("-v", "--version", choices=["v1", "v2"], default="v2")
parser.add_argument("-p", "--prefix", default="", help="An optional prefix for generated file names")
parser.add_argument("-l", "--log_level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Set the log level of the underlying openCost toolkit library")
parser.add_argument("-i", "--institution", help="Transform data for a specific institution only")
parser.add_argument("--no_collected_file", action="store_true", help="Do not generate a collected file (all_articles.csv)")

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
fileHandler = logging.FileHandler("oapk_transform_" + args.log_level.lower() + ".log")
logging.root.addHandler(handler)
logging.root.addHandler(bufferedHandler)
logging.root.addHandler(fileHandler)
logging.root.setLevel(args.log_level)
logging.debug("Logger initialized.")

esac_lookup = oat.ESACHandling()
contracts_lookup = oat.ContractsLookup()

articles, invoice_groups = octk.process_opencost_xml(*xml_content_strings)
invoice_groups = octk.detect_invoice_group_duplicates(invoice_groups)

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

article_fieldnames = list(octk.OPENCOST_EXTRACTION_FIELDS.keys())
contract_fieldnames = oat.COLUMN_SCHEMAS["contracts"]

if not os.path.isdir(TARGET_DIR):
    os.mkdir(TARGET_DIR)

csv_writers = {}
unicode_writers = {}

if not args.no_collected_file:
    all_articles_path = os.path.join(TARGET_DIR, "all_articles.csv")
    main_handle = open(all_articles_path, "w")
    main_writer = csv.DictWriter(main_handle, article_fieldnames, extrasaction="ignore")
    main_writer.writeheader()

for article in articles:
    institution = article["institution"]
    if args.institution is not None and args.institution != institution:
        continue
    if not args.no_collected_file:
        main_writer.writerow(article)
    if institution == '':
        continue # Skip articles silently which have already been omitted by the oc toolkit (usually cost splitting cases)
    esac_id = article["contract_primary_identifier"]
    pub_type = article["type"]
    target_file = institution.lower().replace(" ", "_").replace("/", "_")
    period = article["period"]
    publication_level_costs = False
    try:
        euro_value = float(article["euro"])
        if euro_value > 0.0:
            publication_level_costs = True
            article["euro"] = round(euro_value, 2)
        else:
            article["euro"] = "NA"
    except ValueError:
        pass
    for field in oat.COLUMN_SCHEMAS["additional_costs"]:
        try:
            euro_value = float(article[field])
            article[field] = round(euro_value, 2)
        except ValueError:
            pass
    if pub_type == "book":
        target_file += "_BPC"
    elif oat.has_value(esac_id):
        target_file += "_TA"
        if article["is_hybrid"] == 'NA':
            msg = 'Skipped a record (linked to a contract) which had no valid cost type combination. Cost type must be either "hybrid-oa", "gold-oa" or "publication charge" (with a value of 0) ({})'
            logging.warning(msg.format(article["doi"]))
            continue
    else: #APC
        if pub_type != "journal article":
            msg = 'Skipped a record (not linked to a contract) which was no journal article ({}, {}, {}€, {}, {}, {}, {}))'
            logging.warning(msg.format(article["institution"], article["period"], article["euro"], article["doi"], article["is_hybrid"], pub_type, esac_id))
            continue
        if not publication_level_costs:
            msg = 'Skipped a record (not linked to a contract) which had no publication level costs ({}, {}, {}€, {}, {}, {}, {}))'
            logging.warning(msg.format(article["institution"], article["period"], article["euro"], article["doi"], article["is_hybrid"], pub_type, esac_id))
            continue
    if target_file not in csv_writers:
        path = os.path.join(TARGET_DIR, args.prefix + target_file + ".csv")
        handle = open(path, "w")
        csv_writers[target_file] = {
            "writer": csv.DictWriter(handle, article_fieldnames, extrasaction="ignore"),
            "handle": handle,
            "lines": [],
        }
        csv_writers[target_file]["writer"].writeheader()
    csv_writers[target_file]["lines"].append(article)

for invoice_group in invoice_groups:
    institution = invoice_group["institution"]
    if args.institution is not None and args.institution != institution:
        continue
    target_file = institution.lower().replace(" ", "_").replace("/", "_") + "_contracts"
    esac_id = invoice_group["contract_id"]
    # Preferred way is to get consortium/contract name from contracts.csv
    consortium = "NA"
    contract_name = "NA"
    contract_entry = contracts_lookup.get_by_identifier(esac_id)
    if contract_entry is not None:
        contract_name = contract_entry["contract_name"][0]
        consortium = contract_entry["consortium"][0]
        msg = "ESAC ID {} found in contracts.csv, importing consortium/contract name ({}/{})"
        logging.info(msg.format(esac_id, consortium, contract_name))
    else:
        contract_name = invoice_group["contract_name"]
        esac_entry = esac_lookup.get_esac_entry(esac_id)
        if esac_entry is not None:
            consortium = esac_entry["Organization"]
        msg = "ESAC ID {} not found in contracts.csv, using consortium from ESAC Registry and contract name from openCost data ({}/{})"
        logging.info(msg.format(esac_id, consortium, contract_name))
    if target_file not in unicode_writers:
        path = os.path.join(TARGET_DIR, args.prefix + target_file + ".csv")
        handle = open(path, "w")
        unicode_writers[target_file] = {
            "writer": oat.OpenAPCUnicodeWriter(handle, quotemask=oat.QUOTEMASKS["contracts"]),
            "handle": handle,
            "lines": [],
        }
        unicode_writers[target_file]["lines"].append(list(contract_fieldnames))
    line_tmpl = {
        "institution": institution,
        "consortium": consortium,
        "contract_name": contract_name,
        "identifier": invoice_group["contract_id"],
        "group_id": invoice_group["group_id"],
        "period_from": invoice_group["period"],
        "period_to": invoice_group["period"],
    }
    for invoice in invoice_group["invoices"]:
        for cost_type, amount in invoice["costs"]:
            line = deepcopy(line_tmpl)
            line["cost_type"] = cost_type
            line["euro"] = str(round(amount, 2))
            line_as_list = [line.get(column, "NA") for column in contract_fieldnames]
            unicode_writers[target_file]["lines"].append(line_as_list)

if not args.no_collected_file:
    main_handle.close()

# Create article output files
for writer_name, writer_data in csv_writers.items():
    for line in writer_data["lines"]:
        writer_data["writer"].writerow(line)
    writer_data["handle"].close()

# Create contract output files
for writer_name, writer_data in unicode_writers.items():
    writer_data["writer"].write_rows(writer_data["lines"])

# Flush buffered log messages
bufferedHandler.close()
