#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The file to delete lines from",
    "index": "The index of the column to test for the delete condition",
    "value": "The value on which to trigger a line deletion",
    "full_delete": "Fully delete the line, reducing the total number " +
                   "of rows in the result file. Otherwise, the line " +
                   "is replaced by a row of emtpy values. ", 
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
    parser.add_argument("value", help=ARG_HELP_STRINGS["value"])
    parser.add_argument("-f", "--full_delete", action="store_true", help=ARG_HELP_STRINGS["full_delete"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-q", "--quotemask", help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-o", "--openapc_quote_rules", 
                        help=ARG_HELP_STRINGS["openapc_quote_rules"],
                        action="store_true", default=False)
    
    args = parser.parse_args()
    
    quote_rules = args.openapc_quote_rules
    
    enc = None
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            print ("Encoding '{}' found in Python's codec collection " +
                   "as '{}'").format(args.encoding, codec.name)
            enc = args.encoding
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()
        
    mask = None
    if args.quotemask:
        reduced = args.quotemask.replace("f", "").replace("t", "")
        if len(reduced) > 0:
            print ("Error: A quotemask may only contain the letters 't' and" +
                   "'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]
    
    header, content = oat.get_csv_file_content(args.csv_file, enc)
    
    emtpy_line = [u'' for element in content[0]]
    column_name = "column " + str(args.index)
    if header:
        header_line = header[0]
        column_name = header_line[args.index]
        emtpy_line = [u'' for element in header_line]
    msg = u"Performing line deletion on condition {} == {}".format(column_name, args.value)
    oat.print_g(msg)
    
    modified_content = []
    total_lines = deleted_lines = 0
    for line in content:
        total_lines += 1
        if line[args.index] != args.value:
            modified_content.append(line)
        else:
            deleted_lines += 1
            if not args.full_delete:
                modified_content.append(list(emtpy_line))
            
    msg = u"Process complete, deleted {} out of {} total lines".format(deleted_lines, total_lines)            
    oat.print_g(msg)
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, False)
        writer.write_rows(header + modified_content)


if __name__ == '__main__':
    main()
