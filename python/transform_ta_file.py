#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import re
import sys

import openapc_toolkit as oat

from mappings import AGREEMENT_PUBLISHER_MAP

ins_lookup = {}
print("Processing institutions file...")
with open("../data/institutions.csv", encoding="utf-8") as ins_file:
    reader = csv.DictReader(ins_file)
    for line in reader:
        ins_lookup[line["institution"]] = line
print("...Done")

esac_lookup = {}
print("Processing ESAC Registry file...")
with open("ESAC_Registry.csv", encoding="utf-8") as ins_file:
    reader = csv.DictReader(ins_file)
    for line in reader:
        esac_lookup[line["ID"]] = line
print("...Done")

group_dict = {}

source_header, source_content = oat.get_csv_file_content("../data/transformative_agreements/transformative_agreements.csv", enc='utf-8')
source_header[0][20] = "group_id"

for line in source_content:
    esac_id = contract_id = line[20]
    agreement = line[19]
    doi = line[3]
    consortium = esac_lookup.get(esac_id, {}).get("Organization", "NA")
    publisher = AGREEMENT_PUBLISHER_MAP.get(line[6], line[6])
    if esac_id == 'NA':
        esac_id = agreement.replace(" ", "").replace("-", "").lower()
        esac_id = re.sub(r'\(.*?\)', '', esac_id)
        contract_id = 'NA'
    ins = line[0]
    ror = ins_lookup[ins]["ror_id"]
    if ror != 'NA':
        ror = ror[16:]
    else:
        ror = ins.replace(" ", "").replace("-", "").lower()
    period = line[1]
    group_id = ror + "_" + esac_id + "_" + period
    try:
        euro = float(line[2])
    except ValueError:
        euro = "NA"
    if ins == "FWF - Austrian Science Fund":
        euro = "NA" # FWF data cannot be reliably assigned to contracts - cost data will be kept at article level
    existing_group_id =  group_dict.get(ror, {}).get(period, {}).get(agreement, {}).get('group_id')
    if existing_group_id is not None and existing_group_id != group_id:
        msg = "ERROR: Different group ids ({} <-> {}) generated for combo ({},{},{}) ({})!"
        print(msg.format(existing_group_id, group_id, ror, period, agreement, doi))
        sys.exit()
    if ror not in group_dict:
        group_dict[ror] = {}
    if period not in group_dict[ror]:
        group_dict[ror][period] = {}
    if agreement not in group_dict[ror][period]:
        cost_type = 'NA' if euro == 'NA' else 'publish and read'
        group_dict[ror][period][agreement] = {
            "institution": ins,
            "group_id": group_id,
            "euro": euro,
            "consortium": consortium,
            "contract_name": agreement,
            "identifier": contract_id,
            "period_from": period,
            "period_to": period,
            "cost_type": cost_type,
        }
    else:
        if group_dict[ror][period][agreement]["euro"] != 'NA':
            try:
                group_dict[ror][period][agreement]["euro"] += euro
            except TypeError:
                print(ins, ror, period, agreement, doi)
    if ins != "FWF - Austrian Science Fund":
        line[2] = "NA"
    line[20] = group_id

header = ["institution", "consortium", "contract_name", "identifier", "period_from", "period_to", "cost_type", "euro", "group_id"]
content = [header]
for ror, ror_data in group_dict.items():
    for period, period_data in ror_data.items():
        for agreement, agreement_data in period_data.items():
            try:
                agreement_data["euro"] = str(round(agreement_data["euro"], 2))
            except TypeError:
                pass
            line = [agreement_data[x] for x in header]
            content.append(line)

with open('out_contract.csv', 'w') as out:
    mask = [True, True, True, True, False, False, True, False, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(content)

with open('out_ta.csv', 'w') as out:
    mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(source_header + source_content)  
