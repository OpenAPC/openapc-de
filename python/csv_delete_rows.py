#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import copy
import csv
import os
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The file to delete lines from",
    "index": "The index of the column to test for the delete condition",
    "value": "A single value to trigger a line deletion on. Either " +
             "this argument or a file (using the -f option) must be given",
    "file": "A file containing multiple values to trigger a line " +
            "deletion on. Values must be given line by line, blank lines " +
            "will be ignored. Either this argument or a single value " +
            "(using the -v option) must be given",
    "full_delete": "Fully delete the line, reducing the total number " +
                   "of rows in the result file. Otherwise, the line " +
                   "is replaced by a row of emtpy values. ",
    "ignore_case": "Ignore case when comparing values",
    "results_file": "Write deleted entries to a separate " + 
                    "out file ('del.csv')",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
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
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("index", type=int, help=ARG_HELP_STRINGS["index"])
    parser.add_argument("-v", "--value", help=ARG_HELP_STRINGS["value"])
    parser.add_argument("-f", "--file", help=ARG_HELP_STRINGS["file"])
    parser.add_argument("-d", "--full_delete", action="store_true", help=ARG_HELP_STRINGS["full_delete"])
    parser.add_argument("-i", "--ignore_case", action="store_true", help=ARG_HELP_STRINGS["ignore_case"])
    parser.add_argument("-r", "--results_file", action="store_true", help=ARG_HELP_STRINGS["results_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-q", "--quotemask", help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-o", "--openapc_quote_rules", 
                        help=ARG_HELP_STRINGS["openapc_quote_rules"],
                        action="store_true", default=False)
    
    args = parser.parse_args()
    if args.value is None and args.file is None:
        parser.error("Either a single value (-v option) or a file of " +
                     "multiple values (-f option) must be given.")
    
    values = []
    if args.file:
        if not os.path.isfile(args.file):
            print("Error: '" + args.file + "' is no valid file!")
            sys.exit() 
        with open(args.file, "r") as f:
            for line in f:
                if len(line) > 0:
                    value = line.strip("\r\n")
                    if args.ignore_case:
                        values.append(value.lower())
                    else:
                        values.append(value)
        oat.print_g(str(len(values)) + " values read from file")
    
    if args.value is not None:
        if args.ignore_case:
            values.append(args.value.lower())
        else:
            values.append(args.value)
        if args.file:
            oat.print_y("Value argument given in addition to file " +
                        "argument, adding value to file imports...")
    
    quote_rules = args.openapc_quote_rules
    
    enc = None
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            print (msg.format(args.encoding, codec.name))
            enc = args.encoding
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()
            
    header, content = oat.get_csv_file_content(args.csv_file, enc)
        
    mask = None
    if args.quotemask:
        reduced = args.quotemask.replace("f", "").replace("t", "")
        if len(reduced) > 0:
            print ("Error: A quotemask may only contain the letters 't' and" +
                   "'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]
    
    empty_line = ['' for element in content[0]]
    column_name = "column " + str(args.index)
    if header:
        header_line = header[0]
        column_name = header_line[args.index]
        empty_line = ['' for element in header_line]
    msg = u"Performing line deletion on condition '{}' in {}".format(column_name, values)
    oat.print_g(msg)
    
    modified_content = []
    deleted_lines = []
    num_total_lines = num_deleted_lines = 0
    for line in content:
        if len(line) == 0:
            continue
        num_total_lines += 1
        current_value = line[args.index]
        if args.ignore_case:
            current_value = current_value.lower()
        if current_value not in values:
            modified_content.append(line)
        else:
            num_deleted_lines += 1
            if not args.full_delete:
                modified_content.append(list(empty_line))
            if args.results_file:
                deleted_lines.append(line)
            
    msg = u"Process complete, deleted {} out of {} total lines"        
    oat.print_g(msg.format(num_deleted_lines, num_total_lines))
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, False)
        writer.write_rows(copy.deepcopy(header) + modified_content)

    if args.results_file and len(deleted_lines) > 0:
        with open('del.csv', 'w') as out:
            writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, False)
            writer.write_rows(copy.deepcopy(header) + deleted_lines)


if __name__ == '__main__':
    main()
