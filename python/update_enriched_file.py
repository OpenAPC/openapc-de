#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import sys

from shutil import copy

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "input_file": "The enriched file to update against the data collections",
    "in_place": "Modify the file in place instead on generating an out file",
    "file_type": "The type of the input file (ta or apc)"
}

def get_first_mismatch(list_a, list_b):
    index = 0
    while(True):
        if index >= len(list_a) and index >= len(list_b):
            return False
        if index >= len(list_a):
            return [index, "None", list_b[index]]
        if index >= len(list_b):
            return [index, list_a[index], "None"]
        if list_a[index] != list_b[index]:
            return [index, list_a[index], list_b[index]]
        index += 1

def is_empty_line(line):
    for column in line:
        if oat.has_value(column):
            return False
    return True

parser = argparse.ArgumentParser()
parser.add_argument("input_file", help=ARG_HELP_STRINGS["input_file"])
parser.add_argument("-i", "--in_place", action="store_true", help=ARG_HELP_STRINGS["in_place"])
parser.add_argument("type", help=ARG_HELP_STRINGS["file_type"], choices=["apc", "ta"])
args = parser.parse_args()

new_content = {
    "apc": {
        "file": "../data/apc_de.csv",
        "lines": [],
        "header": None,
        "assigned_lines": 0,
        "mod_lines": 0,
        "lookup": {},
        "doi_index": None,
        "url_index": None,
        "empty_line": None,
    },
    "ta": {
        "file": "../data/transformative_agreements/transformative_agreements.csv",
        "lines": [],
        "header": None,
        "assigned_lines": 0,
        "mod_lines": 0,
        "lookup": {},
        "doi_index": None,
        "url_index": None,
        "empty_line": None,
    }
}

for collection, metadata in new_content.items():
    oat.print_c("Processing " + collection + " file and preparing lookup table...")
    metadata["header"], content = oat.get_csv_file_content(metadata["file"], enc='utf-8')
    metadata["doi_index"] = metadata["header"][0].index("doi")
    oat.print_c("Index of DOI column in file: " + str(metadata["doi_index"]))
    metadata["url_index"] = metadata["header"][0].index("url")
    metadata["empty_line"] = ["" for x in metadata["header"][0]]
    oat.print_c("Index of URL column file: " + str(metadata["url_index"]))
    for line in content:
        doi = line[metadata["doi_index"]]
        if oat.has_value(doi):
            metadata["lookup"][doi] = line
        else:
            url = line[metadata["url_index"]]
            metadata["lookup"][url] = line
            #oat.print_b("entry does not have a doi, using url as identifer instead: " + url

oat.print_c("Processing input file...")
file_header, file_content = oat.get_csv_file_content(args.input_file, enc='utf-8')
file_doi_index = file_header[0].index("doi")
oat.print_c("Index of DOI column in input file: " + str(file_doi_index))
file_url_index = None
try:
    file_url_index = file_header[0].index("url")
    oat.print_c("Index of URL column in input file: " + str(file_url_index))
except ValueError:
    oat.print_c("Input file does not have a url column")
comp_header = new_content[args.type]["header"][0]

mismatch = get_first_mismatch(file_header[0], comp_header)
if mismatch != False:
    msg = "Headers are different, fist mismatch occured at index {} ({} vs {})"
    oat.print_y(msg.format(mismatch[0], mismatch[1], mismatch[2]))
    file_header = [list(comp_header)]
empty_lines = 0

for line_num, line in enumerate(file_content):
    real_num = line_num + 2
    if is_empty_line(line):
        new_content["ta"]["lines"].append(line)
        new_content["apc"]["lines"].append(line)
        empty_lines += 1
        continue
    doi = line[file_doi_index]
    if not oat.has_value(doi) and file_url_index:
        doi = line[file_url_index]
    comp_line_found = False
    for collection, metadata in new_content.items():
        comp_line = metadata["lookup"].get(doi)
        if comp_line is not None:
            comp_line_found = True
            mismatch = get_first_mismatch(line, comp_line)
            if mismatch == False:
                msg = "Line {}: Identifier {} was found in {} file without any modifications"
                oat.print_g(msg.format(real_num, doi, collection))
            else:
                msg = "Line {}: Identifier {} was found in {} file, line differs (first difference encountered at index {}: {}: {} vs {}: {})"
                index = mismatch[0]
                f_h = file_header[0]
                c_h = metadata["header"][0]
                oat.print_y(msg.format(real_num, doi, collection, index, f_h[index], mismatch[1], c_h[index], mismatch[2]))
                metadata["mod_lines"] += 1
            metadata["lines"].append(comp_line)
            metadata["assigned_lines"] += 1
        else:
            metadata["lines"].append(list(metadata["empty_line"]))
    if not comp_line_found:
        msg = "Line {}: ERROR: Identifier {} was not found in any collection - this issue has to be fixed first!"
        oat.print_r(msg.format(real_num, doi))
        sys.exit()

oat.print_c("\nResults:\n")
if empty_lines > 0:
    msg = "  - {} lines were empty"
    oat.print_c(msg.format(empty_lines))
for collection, metadata in new_content.items():
    file_name = "out_" + collection + ".csv"
    res_name = "({})".format(file_name)
    in_place = ", the original file will be replaced"
    if metadata["assigned_lines"] == 0 or metadata["assigned_lines"] + empty_lines == len(file_content) and metadata["mod_lines"] == 0:
        res = "No out file will be generated."
    else:
        res = "An out file {} will be generated".format(res_name)
        with open(file_name, 'w') as out:
            mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
            writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
            writer.write_rows(metadata["header"] + metadata["lines"])
        if args.in_place:
            res += in_place
            copy(file_name, args.input_file)
    msg = "  - {}/{} lines were found in the {} file, {} of those were modified => {}"
    oat.print_c(msg.format(metadata["assigned_lines"], len(file_content), collection, metadata["mod_lines"], res))


