#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import sys

import Levenshtein

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "source_file": "The source csv file",
    "source_file_key_column": "The numerical index of the key column " +
                               "to build a mapping for",
    "existing_mapping": "An optional existing mapping table which will be " +
                        "extended. Should be a two-column csv file, with the " +
                        "first column containing the original values and the " +
                        "second one the mapping targets",
    
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "map_encoding": "The encoding of the optional mapping file"
}

UNMAPPED_ITEM = 'Found value "{}" which has no entry in the mapping table'

NO_SUGGESTION = " Unable to find a suitable target candidate in the current mapping table"
SUGGESTION = " The mapping target with the highest similarity is '{}' ({})"

ASK_MSG = ("How do you want to proceed?\n" +
           "  1) Create an identity mapping ({} -> {})\n" +
           "  2) Skip value {} for this run and continue\n" +
           "  3) Skip value {} and end this run, writing a new mapping file\n" +
           "  4) Try to find an existing mapping target via Levenshtein distance\n"
          )

PROPOSAL = "  5) Use the suggested target and create a mapping ({} -> {})\n"

mapping = {}
skipped_values = []

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("source_file_key_column", type=int, help=ARG_HELP_STRINGS["source_file_key_column"])
    parser.add_argument("-m", "--mapping_file", help=ARG_HELP_STRINGS["existing_mapping"])
    parser.add_argument("-e", "--encoding", default="utf-8", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-em", "--map_encoding", default="utf-8", help=ARG_HELP_STRINGS["map_encoding"])
    
    args = parser.parse_args()
       
    encs = {} #CSV file encodings
    
    for enc_type in ["encoding", "map_encoding"]:
        encoding = getattr(args, enc_type)
        if encoding:
            try:
                codec = codecs.lookup(encoding)
                msg = "Encoding '{}' found in Python's codec collection as '{}'"
                print(msg.format(encoding, codec.name))
                encs[enc_type] = codec.name
            except LookupError:
                print ("Error: '" + encoding + "' not found Python's " +
                       "codec collection. Either look for a valid name here " +
                       "(https://docs.python.org/2/library/codecs.html#standard-" +
                       "encodings) or omit this argument to enable automated " +
                       "guessing.")
                sys.exit()

    source_header, source_content = oat.get_csv_file_content(args.source_file, enc=encs["encoding"])

    if source_header:
        header = source_header[0]
        key_column_name = header[args.source_file_key_column]
    msg = "Creating mappings for column {} in source file {}...".format(key_column_name, args.source_file)
    oat.print_g(msg)

    if args.mapping_file:
        msg = "Trying to import existing mapping from file {}"
        oat.print_g(msg.format(args.mapping_file))
        map_header, map_content = oat.get_csv_file_content(args.mapping_file, enc=encs["map_encoding"], force_header=True)
        if map_header:
            header = map_header[0]
            key_column_name = header[0]
            target_column_name = header[1]
            msg = 'Extracting mapping ("{}" -> "{}")...'
            oat.print_g(msg.format(key_column_name, target_column_name))
        stats = {"self": 0, "other": 0}
        for line in map_content:
            mapping[line[0]] = line[1]
            if line[0] == line[1]:
                stats["self"] += 1
            else:
                stats["other"] += 1
        msg = "{} mapping rules imported, {} values pointing to themselves"
        oat.print_g(msg.format(stats["self"] + stats["other"], stats["self"]))
    else:
        msg = "No mappings file selected, a new one will be created (as out.csv)"
        oat.print_g(msg)

    for line in source_content:
        value = line[args.source_file_key_column]
        if value in skipped_values:
            continue
        if value in mapping:
            msg = 'Mapping already exists for value "{}" (mapped to "{}"), skipping entry...'
            print(msg.format(value, mapping[value]))
        else:
            oat.print_y(UNMAPPED_ITEM.format(value))
            candidates = get_mapping_candidates(value)
            if candidates:
                ratio = round(candidates[0][1], 2)
                suggestion = SUGGESTION.format(candidates[0][0], ratio)
                print(_colorize_by_ratio(suggestion, ratio))
            ask_msg = ASK_MSG.format(value, value, value, value)
            suggest_msg = ""
            options = ["1", "2", "3", "4"]
            if candidates:
                suggest_msg = PROPOSAL.format(value, candidates[0][0])
                options.append("5")
            ask_msg += suggest_msg + "> "
            ret = input(ask_msg)
            while ret not in options:
                repeat_msg = "Please select an option from {} to {} > "
                ret = input(repeat_msg.format(options[0], options[-1:]))
            if ret == "1":
                mapping[value] = value
            elif ret == "2":
                skipped_values.append(value)
            elif ret == "3":
                break
            elif ret == "4":
                ask_for_mapping(value, candidates)
            elif ret == "5":
                mapping[value] = candidates[0][0]

    mapping_header = [["old_value", "target_value"]]
    mapping_content = [[key, value] for key, value in mapping.items()]
    mapping_content.sort(key=lambda x: x[0])

    with open('out.csv', 'w') as out:
        mask = [True, True]
        writer = oat.OpenAPCUnicodeWriter(out, mask, False, True)
        writer.write_rows(mapping_header + mapping_content)

def ask_for_mapping(value, candidates):
    last_option = 1
    options = []
    ask_text = 'The most similar mapping targets for "{}" are:\n'.format(value)
    for target, ratio in candidates:
        txt = '{}) "{}" ({})\n'.format(last_option, target, round(ratio, 2))
        ask_text += txt
        options.append(str(last_option))
        last_option += 1
    skip_txt = '{}) None of the above, skip value "{}" for this run\n >'
    ask_text += skip_txt.format(last_option, value)
    options.append(str(last_option))
    ret = input(ask_text)
    while ret not in options:
        repeat_msg = "Please select an option from {} to {} > "
        ret = input(repeat_msg.format(options[0], options[-1:]))
    if ret == str(last_option):
        skipped_values.append(value)
    else:
        index = int(ret) - 1
        selected_candidate = candidates[index]
        mapping[value] = selected_candidate[0]

def _colorize_by_ratio(text, ratio):
    if ratio == 1.0:
        return oat.colorize(text, "cyan")
    elif ratio >= 0.9:
        return oat.colorize(text, "green")
    elif ratio >= 0.8:
        return oat.colorize(text, "yellow")
    else:
        return oat.colorize(text, "red")

def get_mapping_candidates(value, suggestions=5, min_ratio=0.0):
    candidates = {}
    for target in mapping.values():
        if target not in candidates: 
            ratio = Levenshtein.ratio(target, value)
            candidates[target] = ratio
    candidate_list = [(name, ratio) for name, ratio in candidates.items() if ratio >= min_ratio]
    candidate_list.sort(key=lambda x: x[1], reverse=True)
    return candidate_list[:suggestions]

if __name__ == '__main__':
    main()
