#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "source_file": "The source csv file",
    "source_file_key_column": "The numerical index of the key column " +
                               "in the source file",
    "source_file_value_column": "The numerical index of the value column " +
                                 "in the source file",
    "target_file": "The csv file to enrich with values",
    "target_file_key_column": "The numerical index of the key column " +
                               "in the target file",
    "target_file_value_column": "The numerical index of the value column " +
                                 "in the target file",
    "strict": "keys with ambiguous values will be dropped from the " +
              "mapping table (without this, the last encountered value will be used)",
    "force_overwrite": "Replace existing values (otherwise only " +
                       "empty and NA fields will be replaced)", 
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "other_encoding": "The optional encoding of the source CSV file.",
    "quotemask": "A quotemask to apply to the result file after the action " +
                 "has been performed. A quotemask is a string consisting " +
                 "only of the letters 't' and 'f' (true/false) and has " +
                 "the same length as there are columns in the (resulting) " +
                 "csv file. Only the columns where the index is 't' will be " +
                 "quoted.",
    "openapc_quote_rules": "Determines if the special openapc quote rules " +
                           "should be applied, meaning that the keywords " +
                           "NA, TRUE and FALSE will never be quoted. If in " +
                           "conflict with a quotemask, openapc_quote_rules " +
                           "will take precedence."
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("source_file_key_column", type=int, help=ARG_HELP_STRINGS["source_file_key_column"])
    parser.add_argument("source_file_value_column", type=int, help=ARG_HELP_STRINGS["source_file_value_column"])
    parser.add_argument("target_file", help=ARG_HELP_STRINGS["target_file"])
    parser.add_argument("target_file_key_column", type=int, help=ARG_HELP_STRINGS["target_file_key_column"])
    parser.add_argument("target_file_value_column", type=int, help=ARG_HELP_STRINGS["target_file_value_column"])
    parser.add_argument("-s", "--strict", action="store_true", help=ARG_HELP_STRINGS["strict"])
    parser.add_argument("-f", "--force_overwrite", action="store_true", help=ARG_HELP_STRINGS["force_overwrite"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-e2", "--other_encoding", help=ARG_HELP_STRINGS["other_encoding"])
    parser.add_argument("-q", "--quotemask", help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-o", "--openapc_quote_rules", 
                        help=ARG_HELP_STRINGS["openapc_quote_rules"],
                        action="store_true", default=False)
    
    args = parser.parse_args()
    
    quote_rules = args.openapc_quote_rules
    
    encs = [] #CSV file encodings
    
    for encoding in [args.encoding, args.other_encoding]:
        if encoding:
            try:
                codec = codecs.lookup(encoding)
                msg = "Encoding '{}' found in Python's codec collection as '{}'"
                print(msg.format(encoding, codec.name))
                enc = args.encoding
            except LookupError:
                print ("Error: '" + encoding + "' not found Python's " +
                       "codec collection. Either look for a valid name here " +
                       "(https://docs.python.org/2/library/codecs.html#standard-" +
                       "encodings) or omit this argument to enable automated " +
                       "guessing.")
                sys.exit()
        encs.append(encoding)
        
    mask = None
    if args.quotemask:
        reduced = args.quotemask.replace("f", "").replace("t", "")
        if len(reduced) > 0:
            print ("Error: A quotemask may only contain the letters 't' and" +
                   "'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]
    
    source_header, source_content = oat.get_csv_file_content(args.source_file, enc=encs[0])
    
    key_column_name = "column " + str(args.source_file_key_column)
    value_column_name = "column " + str(args.source_file_value_column)
    if source_header:
        header = source_header[0]
        key_column_name = header[args.source_file_key_column]
        value_column_name = header[args.source_file_value_column]
    msg = u"Creating mapping table ({} -> {}) for source file {}...".format(key_column_name, value_column_name, args.source_file)
    oat.print_g(msg)
    mapping_table = {}
    ambiguous_keys = []
    for line in source_content:
        if line:
            key = line[args.source_file_key_column]
            if key == 'NA':
                continue
            value = line[args.source_file_value_column]
            if key not in mapping_table:
                mapping_table[key] = value
            else:
                if mapping_table[key] != value:
                    if not args.strict:
                        msg = u"WARNING: Replacing existing value '{}' for key '{}' with new value '{}'".format(mapping_table[key], key, value)
                        mapping_table[key] = value
                        oat.print_y(msg)
                    else:
                        if key not in ambiguous_keys:
                            ambiguous_keys.append(key)
    if args.strict:
        for key in ambiguous_keys:
            del(mapping_table[key])
            msg = u"INFO: Ambiguous key '{}' dropped from mapping table".format(key)
            oat.print_b(msg)
    
    oat.print_g("mapping table created, contains " + str(len(mapping_table)) + " entries")
    
    target_header, target_content = oat.get_csv_file_content(args.target_file, enc=encs[1])
    
    
    line_num = 0 if not target_header else 1
    
    replace_msg = u"Line {}: Found matching key '{}', replaced old value '{}' by '{}'"
    modified_content = []
    for line in target_content:
        key = line[args.target_file_key_column]
        if key in mapping_table:
            new_value = mapping_table[key]
            old_value = line[args.target_file_value_column]
            if old_value != new_value:
                if len(old_value) == 0 or old_value == "NA":
                    line[args.target_file_value_column] = new_value
                    msg = replace_msg.format(line_num, key, old_value, new_value)
                    oat.print_g(msg)
                else:
                    if args.force_overwrite:
                        line[args.target_file_value_column] = new_value
                        msg = replace_msg.format(line_num, key, old_value, new_value)
                        oat.print_y(msg)
        modified_content.append(line)
        line_num += 1
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, False)
        writer.write_rows(target_header + modified_content)


if __name__ == '__main__':
    main()
