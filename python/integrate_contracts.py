#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "contract_file": "The base contracts file, will be sorted in place. Defaults to the OpenAPC standard contracts file",
    "add_file": "The file to add to the base contracts file",
}

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contracts_file", help=ARG_HELP_STRINGS["contract_file"], default="../data/transformative_agreements/contracts.csv")
parser.add_argument("-a", "--add_file", help=ARG_HELP_STRINGS["add_file"])
args = parser.parse_args()

add_content = []
if args.add_file is not None:
    add_header, add_content = oat.get_csv_file_content(args.add_file)
    
header, content = oat.get_csv_file_content(args.contracts_file)
content += add_content
for sort_column in [5, 4, 2, 0]: # sort by period_to, period_from,, contrac_name, institution
    content = sorted(content, key=lambda x: x[sort_column]) 

with open(args.contracts_file, "w") as out:
    writer = oat.OpenAPCUnicodeWriter(out, oat.QUOTEMASKS["contracts"], True, True)
    writer.write_rows(header + content)
