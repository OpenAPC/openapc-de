#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse

import openapc_toolkit as oat

def has_costs(line):
    if line[6] == "NA" and line[7] == "NA":
        return False
    return True

ARG_HELP_STRINGS = {
    "contract_file": "The base contracts file, will be sorted in place. Defaults to the OpenAPC standard contracts file",
    "add_file": "The file to add to the base contracts file",
    "deduplicate": "Remove unnecessary entries without costs"
}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contracts_file", help=ARG_HELP_STRINGS["contract_file"], default="../data/transformative_agreements/contracts.csv")
parser.add_argument("-a", "--add_file", help=ARG_HELP_STRINGS["add_file"])
parser.add_argument("-d", "--deduplicate", help=ARG_HELP_STRINGS["deduplicate"], action="store_true")
args = parser.parse_args()

add_content = []
if args.add_file is not None:
    add_header, add_content = oat.get_csv_file_content(args.add_file, enc="utf-8")
    
header, content = oat.get_csv_file_content(args.contracts_file)
content += add_content

if args.deduplicate:
    # Deduplication rules:
    # 1) Keep only one costless line per group_id (euro == NA and cost_type == NA)
    # 2) If there is at least one line with costs for a group_id, drop any costless line
    group_dict = {}
    for line in content:
        group_id = line[8]
        if group_id not in group_dict:
            group_dict[group_id] = {"with_costs": [], "without_costs": None}
        if has_costs(line):
            group_dict[group_id]["with_costs"].append(line)
        else:
            group_dict[group_id]["without_costs"] = line
    dedup_content = []
    for group_id, lines in group_dict.items():
        if len(lines["with_costs"]) > 0:
            dedup_content += lines["with_costs"]
        else:
            dedup_content.append(lines["without_costs"])
    content = dedup_content

for sort_column in [5, 4, 2, 0]: # sort by period_to, period_from,, contract_name, institution
    content = sorted(content, key=lambda x: x[sort_column]) 

with open(args.contracts_file, "w") as out:
    writer = oat.OpenAPCUnicodeWriter(out, oat.QUOTEMASKS["contracts"], True, True)
    writer.write_rows(header + content)
