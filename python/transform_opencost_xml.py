#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import os

import openapc_toolkit as oat

TARGET_DIR = "opencost_out"

parser = argparse.ArgumentParser()
parser.add_argument("xml_files", nargs="+", help="One or more openCost XML files which should validate against the official openCost XSD schema")
args = parser.parse_args()

xml_content_strings = []

for path in args.xml_files:
    with open(path) as f:
        content = f.read()
        xml_content_strings.append(content)

articles = oat.process_opencost_xml(*xml_content_strings)

ror_map = {}
with open(oat.INSTITUTIONS_FILE, "r") as ins_file:
    reader = csv.DictReader(ins_file)
    for line in reader:
        ror_map[line["ror_id"]] = line["institution"]

for article in articles:
    ror_id = article["institution_ror"]
    if oat.has_value(ror_id) and ror_id not in ror_map:
        ror_request = oat.get_metadata_from_ror(ror_id)
        if ror_request["success"]:
            ror_map[ror_id] = ror_request["data"]["institution"]
            print("{};{}".format(ror_id, ror_request["data"]["institution"]))
        else:
            oat.print_r(ror_request["error_msg"])
    article["institution"] = ror_map.get(ror_id, "")

fieldnames = ["institution"] + list(oat.OPENCOST_EXTRACTION_FIELDS.keys())

if not os.path.isdir(TARGET_DIR):
    os.mkdir(TARGET_DIR)

csv_writers = {}
handles = []

all_articles_path = os.path.join(TARGET_DIR, "all_articles.csv")

with open(all_articles_path, "w") as out:
    main_writer = csv.DictWriter(out, fieldnames)
    main_writer.writeheader()
    for article in articles:
        institution = article["institution"]
        invoice_id = article["contract_invoice_id"]
        pub_type = article["type"]
        ins_name = institution.lower().replace(" ", "_")
        if oat.has_value(invoice_id):
            ins_name += "_DEAL"
        elif pub_type == "book":
            ins_name += "_BPC"
        if ins_name not in csv_writers:
            path = os.path.join(TARGET_DIR, ins_name + ".csv")
            handle = open(path, "w")
            handles.append(handle)
            csv_writers[ins_name] = csv.DictWriter(handle, fieldnames)
            csv_writers[ins_name].writeheader()
        csv_writers[ins_name].writerow(article)
        main_writer.writerow(article)

for handle in handles:
    handle.close()
