#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The csv file where columns should be reordered",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding."
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    subparsers = parser.add_subparsers(help='The column operation to perform')
    
    quote_parser = subparsers.add_parser("quote", help="quote help")
    quote_parser.add_argument("column_index", type=int, help='bar help')
    quote_parser.set_defaults(func=quote_column)
    
    unquote_parser = subparsers.add_parser("unquote", help="unquote help")
    unquote_parser.add_argument("column_index", type=int, help='bar help')
    unquote_parser.set_defaults(func=unquote_column)
    
    unquote_parser = subparsers.add_parser("delete", help="delete help")
    unquote_parser.add_argument("column_index", type=int, help='bar help')
    unquote_parser.set_defaults(func=delete_column)
    
    insert_parser = subparsers.add_parser("insert", help="insert help")
    insert_parser.add_argument("target_index", type=int, help='bar help')
    insert_parser.add_argument("column_name", help='bar help')
    insert_parser.add_argument("default_value", help='bar help')
    insert_parser.set_defaults(func=insert_column)
    
    move_parser = subparsers.add_parser("move", help="move help")
    move_parser.add_argument("column_index", type=int, help='bar help')
    move_parser.add_argument("target_index", type=int, help='bar help')
    move_parser.set_defaults(func=move_column)
    
    args = parser.parse_args()
    
    print args
    
    enc = None #CSV file encoding
    
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
    
    result = oat.analyze_csv_file(args.csv_file)
    if result["success"]:
        csv_analysis = result["data"]
        print csv_analysis
    else:
        print result["error_msg"]
        sys.exit()
    
    if enc is None:
        enc = csv_analysis.enc
    
    if enc is None:
        print ("Error: No encoding given for CSV file and automated " +
               "detection failed. Please set the encoding manually via the " +
               "--enc argument")
        sys.exit()
        
    dialect = csv_analysis.dialect
    dialect.quoting = csv.QUOTE_NONE # No modification of quotes while reading
    
    csv_file = open(args.csv_file, "r")

    reader = oat.UnicodeReader(csv_file, dialect=dialect, encoding=enc)
    new_rows = args.func(reader, args)
    csv_file.close()
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, None, False, False)
        writer.write_rows(new_rows)
        
def quote_column(csv_reader, args):
    new_rows = []
    for row in csv_reader:
        row[args.column_index] = '"' + row[args.column_index] + '"'
        new_rows.append(row)
    return new_rows

def unquote_column(csv_reader, args):
    new_rows = []
    for row in csv_reader:
        value = row[args.column_index]
        if value.startswith('"'):
            value = value[1:]
        if value.endswith('"'):
            value = value[:-1]
        row[args.column_index] = value
        new_rows.append(row)
    return new_rows
    
def move_column(csv_reader, args):
    new_rows = []
    for row in csv_reader:
        row.insert(args.target_index, row.pop(args.column_index))
        new_rows.append(row)
    return new_rows
    
def delete_column(csv_reader, args):
    new_rows = []
    for row in csv_reader:
        row.pop(args.column_index)
        new_rows.append(row)
    return new_rows
    
def insert_column(csv_reader, args):
    header = csv_reader.next()
    header.insert(args.target_index, args.column_name)
    new_rows = [header]
    for row in csv_reader:
        row.insert(args.target_index, args.default_value)
        new_rows.append(row)
    return new_rows

if __name__ == '__main__':
    main()
