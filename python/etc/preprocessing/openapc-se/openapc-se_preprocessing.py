#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from os import path
import sys

ARG_HELP_STRINGS = {
    "apc_se_file": 'Path to the openapc-se core data file (usually named "apc_se.csv")',
    "org_acronym_file": 'Path to the openapc-se institutional acronym mapping table (usually ' +
                        'named "org_acronym_name_map.tsv")',
    "transagree_file": 'Path to the openapc-de transformative agreements file',
    "duplicates_file": 'Path to the openapc-de unresolved duplicates file'
}

INSTITUTIONAL_MAPPINGS = {}
TRANSAGREE_DOIS = []
DUPLICATES_DOIS = []

EMPTY_LINE = ["" for x in range(18)]

QUOTE_MASK = [True, False, False, True, True, True, True, True, True, True, True, True, True,
               True, True, True, True, True]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("apc_se_file", help=ARG_HELP_STRINGS["apc_se_file"])
    parser.add_argument("org_acronym_file", help=ARG_HELP_STRINGS["org_acronym_file"])
    parser.add_argument("transagree_file", help=ARG_HELP_STRINGS["transagree_file"])
    parser.add_argument("duplicates_file", help=ARG_HELP_STRINGS["duplicates_file"])
    args = parser.parse_args()

    _, acronyms = oat.get_csv_file_content(args.org_acronym_file, "utf-8", True)
    
    for line in acronyms:
        INSTITUTIONAL_MAPPINGS[line[0]] = line[1]
        
    oat.print_b("Loading transformative agreements file...")
    _, transagree_content = oat.get_csv_file_content(args.transagree_file, "utf-8", True)
    for line in transagree_content:
        doi = line[3]
        if oat.has_value(doi):
            TRANSAGREE_DOIS.append(line[3])
    oat.print_b("Done, " + str(len(TRANSAGREE_DOIS)) + " DOIs extracted from transformative agreements file.")
    
    oat.print_b("Loading unresolved duplicates file...")
    _, duplicates_content = oat.get_csv_file_content(args.duplicates_file, "utf-8", True)
    for line in duplicates_content:
        doi = line[3]
        if oat.has_value(doi) and doi not in DUPLICATES_DOIS:
            DUPLICATES_DOIS.append(doi)
    oat.print_b("Done, " + str(len(DUPLICATES_DOIS)) + " unique DOIs extracted from unresolved duplicates file.")

    apc_se_header, apc_se_content = oat.get_csv_file_content(args.apc_se_file, "utf-8", True)
    stats = {
        "offsetting_duplicates": 0,
        "unresolved_duplicates": 0,
        "no_positive_euro_value": 0
    }
    modified_content = []
    for line in apc_se_content:
        if line[3] in TRANSAGREE_DOIS:
            modified_content.append(list(EMPTY_LINE))
            stats["offsetting_duplicates"] += 1
            continue
        if line[3] in DUPLICATES_DOIS:
            modified_content.append(list(EMPTY_LINE))
            stats["unresolved_duplicates"] += 1
            continue
        euro = float(line[2])
        if not euro > 0:
            modified_content.append(list(EMPTY_LINE))
            stats["no_positive_euro_value"] += 1
            continue
        try:
            line[0] = INSTITUTIONAL_MAPPINGS[line[0]]
            modified_content.append(line)
        except KeyError:
            oat.print_r("Error: No mapping found for institutional acronym '" + line[0] + "'!")
            sys.exit()
    print(modified_content[0:100])
    with open("apc_se_preprocessed.csv", "w") as f:
        writer = oat.OpenAPCUnicodeWriter(f, QUOTE_MASK, True, True)
        writer.write_rows(apc_se_header + modified_content)
    msg = "Preprocessed file written, {} offsetting duplicates removed, {} zero-cost articles removed, {} articles marked as unresolved duplicates removed."
    oat.print_g(msg.format(stats["offsetting_duplicates"], stats["no_positive_euro_value"], stats["unresolved_duplicates"]))
    

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))))
    import openapc_toolkit as oat
    main()
