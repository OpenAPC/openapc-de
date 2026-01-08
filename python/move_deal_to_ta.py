#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
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

modified_apc_content = []

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
        continue
    modified_apc_content.append(line)

print("DEAL articles moved:")
for ins, pub_dict in institutions_articles.items():
    print(ins)
    for pub, count in pub_dict.items():
        print("   " + pub + ": " + str(count))

with open('out_apc_de.csv', 'w') as out:
    mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(apc_header + modified_apc_content)

with open('out_ta.csv', 'w') as out:
    mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(ta_header + ta_content)  
