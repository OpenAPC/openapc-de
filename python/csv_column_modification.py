#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The csv file where columns should be modified",
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
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-q", "--quotemask", help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-o", "--openapc_quote_rules", 
                        help=ARG_HELP_STRINGS["openapc_quote_rules"],
                        action="store_true", default=False)
    subparsers = parser.add_subparsers(help='The column operation to perform')
    
    delete_parser = subparsers.add_parser("delete", help="delete help")
    delete_parser.add_argument("column_index", type=int, help='bar help')
    delete_parser.set_defaults(func=delete_column)
    
    insert_parser = subparsers.add_parser("insert", help="insert help")
    insert_parser.add_argument("target_index", type=int, help='bar help')
    insert_parser.add_argument("column_name", help='bar help')
    insert_parser.add_argument("default_value", help='bar help')
    insert_parser.set_defaults(func=insert_column)
    
    move_parser = subparsers.add_parser("move", help="move help")
    move_parser.add_argument("column_index", type=int, help='bar help')
    move_parser.add_argument("target_index", type=int, help='bar help')
    move_parser.set_defaults(func=move_column)
    
    copy_parser = subparsers.add_parser("copy", help="copy help")
    copy_parser.set_defaults(func=copy)
    
    args = parser.parse_args()
    
    quote_rules = args.openapc_quote_rules
    
    enc = None #CSV file encoding
    
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            print(msg.format(args.encoding, codec.name))
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
            print ("Error: A quotemask may only contain the letters 't' and"  +
                   "'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]
    
    new_rows = args.func(header, content, args)
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, True)
        writer.write_rows(new_rows)
        
def quote_column(header, content, args):
    new_rows = header
    for row in content:
        row[args.column_index] = '"' + row[args.column_index] + '"'
        new_rows.append(row)
    return new_rows

def unquote_column(header, content, args):
    new_rows = header
    for row in content:
        value = row[args.column_index]
        if value.startswith('"'):
            value = value[1:]
        if value.endswith('"'):
            value = value[:-1]
        row[args.column_index] = value
        new_rows.append(row)
    return new_rows
    
def move_column(header, content, args):
    new_rows = []
    merged = header + content
    for row in merged:
        if len(row) > 0:
            row.insert(args.target_index, row.pop(args.column_index))
        new_rows.append(row)
    return new_rows
    
def delete_column(header, content, args):
    new_rows = []
    merged = header + content
    for row in merged:
        if len(row) > 0:
            row.pop(args.column_index)
        new_rows.append(row)
    return new_rows
    
def insert_column(header, content, args):
    header[0].insert(args.target_index, args.column_name)
    new_rows = header
    for row in content:
        row.insert(args.target_index, args.default_value)
        new_rows.append(row)
    return new_rows
    
def copy(header, content, _):
    new_rows = header
    for row in content:
        new_rows.append(row)
    return new_rows

if __name__ == '__main__':
    main()
