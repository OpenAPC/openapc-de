#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import os
import sys

import json

import openapc_toolkit as oat

UD_FILE = "../data/unresolved_duplicates.csv"

EMPTY_LINE = ["NA","","NA","NA","NA","NA","NA","NA","NA","NA","NA","NA","FALSE","NA","NA","NA","NA","NA"]
QUOTE_MASK = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
REPLACEMENT = "---replace---"

ARG_HELP_STRINGS = {
    "new_file": "The new data file to be integrated into the target data file. Must be duplicate-free itself.",
    "target_file": "The target file, usually the OpenAPC core data or TA file. Must be duplicate-free itself.",
    "enriched_files": "One or more enriched files were duplicates are expected to originate from. Changes to target file will be mirrored there.",
    "batch": "Number of duplicates to resolve per run (default: unlimited)",
    "cost_tolerance": " A fraction indicating how much the cost values between two articles may diverge to be still treated as 'equal'. The Formula is (higer_cost - lower_cost) / higher_cost."
}

ENRICHED_FILES = {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("new_file", help=ARG_HELP_STRINGS["new_file"])
    parser.add_argument("target_file", help=ARG_HELP_STRINGS["new_file"])
    parser.add_argument('cost_tolerance', type=float, help=ARG_HELP_STRINGS["cost_tolerance"])
    parser.add_argument('enriched_files', nargs='+', help=ARG_HELP_STRINGS["enriched_files"])
    parser.add_argument('-b', '--batch', type=int, help=ARG_HELP_STRINGS["batch"])
    
    args = parser.parse_args()
    
    target_file_name = get_filename(args.target_file)
    new_file_name = get_filename(args.new_file)
    
    
    for path in args.enriched_files:
        if not os.path.isfile(path):
            oat.print_r('Error: "' + path + '" is no valid file path!')
            sys.exit()
        ENRICHED_FILES[path] = {"modified": False, "file_name": get_filename(path)}
        ENRICHED_FILES[path]["header"], ENRICHED_FILES[path]["content"] = oat.get_csv_file_content(path, enc="utf-8", force_header=True)
        
    
    target_header, target_content = oat.get_csv_file_content(args.target_file, enc="utf-8", force_header=True)
    new_header, new_content = oat.get_csv_file_content(args.new_file, enc="utf-8", force_header=True)
    ud_header, ud_content = oat.get_csv_file_content(UD_FILE, enc="utf-8", force_header=True)
    
    duplicates = []
    target_dois = [line[3] for line in target_content]
    
    for new_index, line in enumerate(new_content):
        doi = line[3]
        if doi == "NA" or doi not in target_dois:
            continue
        else:
            target_index = get_duplicate_index(target_content, doi)
            duplicates.append((new_index, target_index))
    
    count = 0
    for pair in duplicates:
        new_line = new_content[pair[0]]
        target_line = target_content[pair[1]]
        doi = target_line[3]
        new_cost = float(new_line[2])
        target_cost = float(target_line[2])
        if new_cost >= target_cost:
            deviation = (new_cost - target_cost) / new_cost
        else:
            deviation = (target_cost - new_cost) / target_cost
        oat.print_b("Duplicate found:")
        print("In new file " + new_file_name + ":")
        print(",".join(new_line))
        print("In target file " + target_file_name + ":")
        print(",".join(target_line))
        if new_line[0] != target_line[0]:
            msg = 'Institutional mismatch "{}"/"{}". Lines will be deleted and added to the unresolved duplicates file.'
            oat.print_r(msg.format(new_line[0],target_line[0]))
            new_content[pair[0]] = list(EMPTY_LINE)
            target_content[pair[1]] = REPLACEMENT
            ud_content += [target_line]
            ud_content += [new_line]
            path, index = find_in_enriched_files(doi)
            ENRICHED_FILES[path]["content"][index] = list(EMPTY_LINE)
            ENRICHED_FILES[path]["modified"] = True
        elif deviation <= args.cost_tolerance:
            msg = "Cost deviation between {} and {} is below tolerance threshold ({} <= {}). Entries are treated as equal, only the new one will be deleted."
            oat.print_g(msg.format(new_cost, target_cost, deviation, args.cost_tolerance))
            new_content[pair[0]] = list(EMPTY_LINE)
        else:
            msg = "Cost deviation between {} and {} exceeds tolerance threshold ({} > {}). Entries are treated as different, both will be deleted."
            oat.print_y(msg.format(new_cost, target_cost, deviation, args.cost_tolerance))
            new_content[pair[0]] = list(EMPTY_LINE)
            target_content[pair[1]] = REPLACEMENT
            path, index = find_in_enriched_files(doi)
            ENRICHED_FILES[path]["content"][index] = list(EMPTY_LINE)
            ENRICHED_FILES[path]["modified"] = True
        count += 1
        if args.batch and count >= args.batch:
            break

    while REPLACEMENT in target_content:
        target_content.remove(REPLACEMENT)
    
    with open(args.target_file, 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
        writer.write_rows(target_header + target_content)
    with open(args.new_file, 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
        writer.write_rows(new_header + new_content)
    with open(UD_FILE, 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
        writer.write_rows(ud_header + ud_content)
    for path, enriched_file in ENRICHED_FILES.items():
        if enriched_file["modified"]:
            with open(path, 'w') as out:
                writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
                writer.write_rows(enriched_file["header"] + enriched_file["content"])
    
        
def get_filename(path):
    base_name = os.path.basename(path)
    return os.path.splitext(base_name)[0]
    
def find_in_enriched_files(doi):
    for path, enriched_file in ENRICHED_FILES.items():
        for index, line in enumerate(enriched_file["content"]):
            if line[3] == doi:
                msg = "DOI {} found in enriched file {}".format(doi, enriched_file["file_name"])
                oat.print_b(msg)
                return (path, index)
    raise ValueError("DOI " + doi + " not found in any enriched file!")
        
def get_duplicate_index(content, doi):
    for index, line in enumerate(content):
        if line[3] == doi:
            return index
    raise ValueError("DOI " + doi + " not found while searching for index.")

if __name__ == '__main__':
    main()
