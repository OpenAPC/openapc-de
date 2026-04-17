#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from copy import deepcopy
from datetime import datetime
import csv
import re
import sys

import openapc_toolkit as oat

# from openapc-olap: 
DEAL_WILEY_START_YEAR = datetime(2019, 1, 1)
DEAL_SPRINGER_START_YEAR = datetime(2020, 1, 1)
DEAL_IMPRINTS = {
    "Wiley-Blackwell": ["Wiley-Blackwell", "EMBO", "American Geophysical Union (AGU)", "International Union of Crystallography (IUCr)", "The Econometric Society"],
    "Springer Nature": ["Springer Nature", "Zhejiang University Press"]
}

CONTRACTS_WILEY_TMPL = [
    "Muenchen LMU",
    "Projekt DEAL Consortium",
    "DEAL Wiley Germany",
    "wiley2019deal",
    "2019",
    "2019",
    "NA",
    "NA",
    "05591te55_wiley2019deal_2019"
]

CONTRACTS_SPRINGER_TMPL = [
    "Muenchen LMU",
    "Projekt DEAL Consortium",
    "DEAL Springer Nature Germany",
    "sn2020deal",
    "2020",
    "2020",
    "NA",
    "NA",
    "05591te55_sn2020deal_2020"
]

GERMAN_NON_DEAL_INSTITUTIONS = ["Leibniz-Fonds"]

ins_lookup = {}
print("Processing institutions file...")
with open("../data/institutions.csv", encoding="utf-8") as ins_file:
    reader = csv.DictReader(ins_file)
    for line in reader:
        ins_lookup[line["institution"]] = line
print("...Done")

ta_header, ta_content = oat.get_csv_file_content("../data/transformative_agreements/transformative_agreements.csv", enc='utf-8')
apc_header, apc_content = oat.get_csv_file_content("../data/apc_de.csv", enc='utf-8')
contracts_header, contracts_content = oat.get_csv_file_content("../data/transformative_agreements/contracts.csv", enc='utf-8')

group_id_list = []
for row in contracts_content:
    if row[8] not in group_id_list:
        group_id_list.append(row[8])

modified_apc_content = []
new_contracts = []

institutions_articles = {}

for line in apc_content:
    ins = line[0]
    period = line[1]
    is_hybrid = line[4]
    publisher = line[5]
    ror = ins_lookup[ins]["ror_id"]
    if ror != 'NA':
        ror = ror[16:]
    else:
        ror = ins.replace(" ", "").replace("-", "").lower()
    country = ins_lookup[ins]["country"]
    if country != "DEU" or is_hybrid != "FALSE" or ins in GERMAN_NON_DEAL_INSTITUTIONS:
        modified_apc_content.append(line)
        continue
    if publisher in DEAL_IMPRINTS["Wiley-Blackwell"] and datetime.strptime(period, "%Y") >= DEAL_WILEY_START_YEAR:
        # group_id: 01y9bpm73_wiley2019deal_2023
        esac_id = "_wiley2019deal_" if int(period) < 2024 else "_wiley2024deal_"
        group_id = ror + esac_id + period
        line.insert(5, "FALSE") # opt-out
        line.insert(19, "DEAL Wiley Germany") 
        line.insert(20, group_id)
        ta_content.append(line)
        if ins not in institutions_articles:
            institutions_articles[ins] = {}
        if publisher not in institutions_articles[ins]:
            institutions_articles[ins][publisher] = 0
        institutions_articles[ins][publisher] += 1
        if group_id not in group_id_list:
            contract_line = deepcopy(CONTRACTS_WILEY_TMPL)
            contract_line[0] = ins
            contract_line[3] = esac_id.strip("_")
            contract_line[4] = period
            contract_line[5] = period
            contract_line[8] = group_id
            new_contracts.append(contract_line)
            group_id_list.append(group_id)
        continue
    if publisher in DEAL_IMPRINTS["Springer Nature"] and datetime.strptime(period, "%Y") >= DEAL_SPRINGER_START_YEAR:
        esac_id = "_sn2020deal_" if int(period) < 2024 else "_sn2024deal_"
        group_id = ror + esac_id + period
        line.insert(5, "FALSE") # opt-out
        line.insert(19, "DEAL Springer Nature Germany")
        line.insert(20, group_id)
        ta_content.append(line)
        if ins not in institutions_articles:
            institutions_articles[ins] = {}
        if publisher not in institutions_articles[ins]:
            institutions_articles[ins][publisher] = 0
        institutions_articles[ins][publisher] += 1
        if group_id not in group_id_list:
            contract_line = deepcopy(CONTRACTS_SPRINGER_TMPL)
            contract_line[0] = ins
            contract_line[3] = esac_id.strip("_")
            contract_line[4] = period
            contract_line[5] = period
            contract_line[8] = group_id
            new_contracts.append(contract_line)
            group_id_list.append(group_id)
        continue
    modified_apc_content.append(line)

print("DEAL articles moved:")
for ins, pub_dict in institutions_articles.items():
    print(ins)
    for pub, count in pub_dict.items():
        print("   " + pub + ": " + str(count))
        
print("\n" + str(len(new_contracts)) + " new contract lines generated.")

with open('out_apc_de.csv', 'w') as out:
    mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(apc_header + modified_apc_content)

with open('out_ta.csv', 'w') as out:
    mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(ta_header + ta_content)  
    
with open('out_contracts.csv', 'w') as out:
    mask = [True, True, True, True, False, False, True, False, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(contracts_header + new_contracts)  
