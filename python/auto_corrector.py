#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import copy
import csv
import os
import sys

import openapc_toolkit as oat

from test import whitelists as wl

ARG_HELP_STRINGS = {
    "csv_file": "The enriched file to check for errors",
}

APC_DE_FILE = "../data/apc_de.csv"
TA_FILE = "../data/transformative_agreements/transformative_agreements.csv"

ISSN_DICTS = {
    "issn": {},
    "issn_print": {},
    "issn_electronic": {},
    "issn_l": {}
}

MISMATCH_MSG = ('Line {}: Detected a mismatch in the {} field for {} {}:\n' +
                '  period             : {}\n' +
                '  is_hybrid          : {}\n' +
                '  publisher          : {}\n' +
                '  journal_full_title : {}\n' +
                '  ISSN-L             : {}\n' +
                'The journal occurs {} times in all OpenAPC collections with the following metadata:\n' +
                '  is_hybrid          : {}\n' +
                '  publisher          : {}\n' +
                '  journal_full_title : {}\n' +
                '  ISSN-L             : {}\n')

CORRECT_MSG = ("How do you want to proceed?\n" +
               "1) Correct {} to {}\n" +
               "2) Correct {} to {} and abort (saving all changes to out.csv)\n" +
               "3) Do nothing\n" +
               "4) Do nothing and abort (saving all changes to out.csv)\n" +
               "5) Get additional information from the EZB\n> ")

WL_ENTRY_WARNING = ("WARNING: At least one of the issn values ({}) is already present " +
                    "in the JOURNAL_OWNER_CHANGED whitelist. You might have to add additional " +
                    "entries for other issn types (print, electronic or linking) if they differ "+
                    "from the regular issn value.\n")

OUT_ASK = ("Please select a target file for the results.\n" +
           "1) out.csv\n" +
           "2) Source file {} - WARNING: Make sure the file has already been commited to git!" )

QUOTE_MASK = [True, False, False, True, True, True, True, True, True, True, True,
              True, True, True, True, True, True, True, True]


EZBS = oat.EZBSrcaping()

def _prepare_ezb_info(issn):
    info = EZBS.get_ezb_info(issn)
    if not info["success"]:
        msg = "\n\nNo Information could be obtained from the EZB for ISSN " + issn
        return msg
    msg = "\n\nThe following additional information could be obtained from the EZB for ISSN " + issn + ":\n"
    for record in info["data"]:
        msg += "Title:      " + record["title"] + "\n"
        msg += "Access:     " + oat.colorize(record["access_msg"], record["access_color"]) + "\n"
        msg += "Comments:   " + str(record["remarks"]) + "\n"
        msg += "Categories: " + ", ".join(record["categories"]) + "\n" if record["categories"] else ""
        msg += "DOAJ:       " + record["doaj_link"] + "\n" if record["doaj_link"] else ""
        msg += "-------------------------------------------------------\n"        
    return msg

def _build_wl_suggestion(field_type, new_value, established_value, issn, issn_p, issn_e, issn_l, journal_full_title):
    entry = ""
    if field_type == "publisher":
        line = '"{}": ["{}", "{}"], # {} {}'
        for issn_value in [issn, issn_p, issn_e, issn_l]:
            if issn_value in wl.JOURNAL_OWNER_CHANGED:
                msg = WL_ENTRY_WARNING.format(issn_value)
                return oat.colorize(msg, "yellow")
        entry = "A possible entry for the JOURNAL_OWNER_CHANGED whitelist would look like this:\n\n"
        entry += line.format(issn, established_value, new_value, journal_full_title, "")
        processed_issns = [issn]
        for other_issns in [(issn_p, "print"), (issn_e,"electronic"), (issn_l, "linking")]:
            if oat.has_value(other_issns[0]) and other_issns[0] not in processed_issns:
                entry += "\n"
                entry += line.format(other_issns[0], established_value, new_value, journal_full_title, "(" + other_issns[1] + ")")
                processed_issns.append(other_issns[0])
        entry += "\n"
    elif field_type == "is_hybrid":
        line = '"{}", # {}, {} OA since \n'
        entry = "A possible entry for the JOURNAL_HYBRID_STATUS_CHANGED whitelist would look like this:\n\n"
        new_status = "Gold" if new_value == "FALSE" else "Hybrid"
        entry += line.format(issn, journal_full_title, new_status)
    return entry

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    args = parser.parse_args()
    
    for file_path in [APC_DE_FILE, TA_FILE]:
        with open(file_path, "r") as path:
            reader = csv.DictReader(path)
            oat.print_b("Preparing mapping tables from " + file_path + "...")
            for line in reader:
                data = {
                    "journal_full_title": line["journal_full_title"],
                    "publisher": line["publisher"],
                    "is_hybrid": line["is_hybrid"],
                    "issn_l": line["issn_l"],
                    "count": 1
                }
                for issn_type in ISSN_DICTS.keys():
                    issn = line[issn_type]
                    if issn not in ISSN_DICTS[issn_type]:
                        ISSN_DICTS[issn_type][issn] = data
                    else:
                        ISSN_DICTS[issn_type][issn]["count"] += 1
                if reader.line_num % 10000 == 0:
                    oat.print_b(str(reader.line_num) + " lines processed")

    modified_content = []
    header = None
    changes_made = False
    with open(args.csv_file) as csv_file:
        reader = csv.DictReader(csv_file)
        header = list(reader.fieldnames)
        stopped = False
        for line in reader:
            if stopped:
                modified_content.append(line)
                continue
            skip_line = False
            for issn_type in ISSN_DICTS.keys():
                if skip_line:
                    break
                issn = line[issn_type]
                if not oat.has_value(issn):
                    continue
                if issn in ISSN_DICTS[issn_type]:
                    for field_type in ["is_hybrid", "publisher", "journal_full_title", "issn_l"]:
                        new_value = line[field_type]
                        established_value = ISSN_DICTS[issn_type][issn][field_type]
                        if new_value != established_value and not is_whitelisted(field_type, new_value, established_value, line["issn"], line["issn_print"], line["issn_electronic"], line["issn_l"]):
                            msg = MISMATCH_MSG.format(reader.line_num, oat.colorize(field_type, "cyan"), issn_type, issn, line["period"], line["is_hybrid"],
                                                      line["publisher"], line["journal_full_title"], line["issn_l"], oat.colorize(str(ISSN_DICTS[issn_type][issn]["count"]), "cyan"),
                                                      ISSN_DICTS[issn_type][issn]["is_hybrid"], ISSN_DICTS[issn_type][issn]["publisher"],
                                                      ISSN_DICTS[issn_type][issn]["journal_full_title"], ISSN_DICTS[issn_type][issn]["issn_l"])
                            print(msg)
                            print(_build_wl_suggestion(field_type, new_value, established_value, line["issn"], line["issn_print"], line["issn_electronic"], line["issn_l"], line["journal_full_title"]))
                            ask_msg = CORRECT_MSG.format(field_type, oat.colorize(established_value, "green"), 
                                                         field_type, oat.colorize(established_value, "green"))
                            ezb_msg = None
                            ret = input(ask_msg)
                            while ret not in ["1", "2", "3", "4"]:
                                if ret == "5":
                                    if ezb_msg is None:
                                        ezb_msg = _prepare_ezb_info(issn)
                                    print(ezb_msg)
                                ret = input("Please select an option from 1 to 5 > ")
                            print("\n\n\n\n")
                            if ret in ["1", "2"]:
                                changes_made = True
                                line[field_type] = established_value
                            if ret in ["3", "4"]:
                                skip_line = True
                            if ret in ["2", "4"]:
                                stopped = True
                                break
            modified_content.append(line)
    modified_lines = [header]
    for line in modified_content:
        modified_lines.append(list(line.values()))
    if not changes_made:
        print("No changes made, skipping result file generation")
        sys.exit()
    ret = input(OUT_ASK.format(args.csv_file))
    while ret not in ["1", "2"]:
        ret = input('Please select either "1" or "2"')
    target = "out.csv"
    if ret == "2":
        target = args.csv_file
    with open(target, 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True, False)
        writer.write_rows(modified_lines)

def is_whitelisted(field_type, new_value, established_value, issn, issn_p, issn_e, issn_l):
    # The JOURNAL_HYBRID_STATUS_CHANGED wl only lists one of the issns, 
    # so we have to compare all issn types for a match.
    if field_type == "is_hybrid":
        if len({issn, issn_p, issn_e, issn_l}.intersection(wl.JOURNAL_HYBRID_STATUS_CHANGED)) > 0:
            return True
        return False
    # The publisher wls, on the other hand, list all issn types, so we have
    # implement a different kind of logic
    if field_type == "publisher":
        for issn_type in [issn, issn_p, issn_e, issn_l]:
            if oat.has_value(issn_type) and not wl.in_whitelist(issn_type, established_value, new_value):
                return False
        return True
    return False

if __name__ == '__main__':
    main()
