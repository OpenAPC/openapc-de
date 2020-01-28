#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "enriched_file": "A fully enriched file to extract hybrid Wiley articles from"
}

EMPTY_LINE_CORE = ["" for i in range(17)]
EMPTY_LINE_TA = ["" for i in range(18)]

# Wiley and imprints
PUBLISHER_LIST = ["Wiley-Blackwell", "EMBO", "American Geophysical Union (AGU)"]

AGREEMENT_NAME = "DEAL Wiley Germany"

QUOTE_MASK = [True, False, False, True, True, True, True, True, True, True, True, True, True, True,
              True, True, True, True, True]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("enriched_file", help=ARG_HELP_STRINGS["enriched_file"])
    args = parser.parse_args()
    
    header, content = oat.get_csv_file_content(args.enriched_file, enc="utf-8", force_header=True)
    header_line = header[0]
    
    core_content = [list(header_line)]
    ta_content = [list(header_line) + ["agreement"]]
    print(core_content)
    print(ta_content)
    
    for line in content:
        if line[4] == "TRUE" and line[5] in PUBLISHER_LIST:
            core_content.append(list(EMPTY_LINE_CORE))
            ta_content.append(line + [AGREEMENT_NAME])
        else:
            core_content.append(line)
            ta_content.append(list(EMPTY_LINE_TA))

    with open("out_orig.csv", "w") as out:
        writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
        writer.write_rows(core_content)
    with open("out_deal_wiley.csv", "w") as out:
        writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
        writer.write_rows(ta_content)
    
if __name__ == '__main__':
    main()
