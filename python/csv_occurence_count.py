#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
from collections import OrderedDict
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "source_file": "The source csv file",
    "count_column": "The numerical index of the column where values " +
                    "should be counted",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "sort": "sort results by occurence count"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("count_column", type=int, help=ARG_HELP_STRINGS["count_column"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-s", "--sort", action="store_true", help=ARG_HELP_STRINGS["sort"])

    args = parser.parse_args()

    enc = None
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            print(msg.format(args.encoding, codec.name))
            enc = args.encoding
        except LookupError:
            oat.print_r("Error: '" + args.encoding + "' not found Python's " +
                        "codec collection. Either look for a valid name here " +
                        "(https://docs.python.org/2/library/codecs.html#standard-" +
                        "encodings) or omit this argument to enable automated " +
                        "guessing.")
            sys.exit()

    header, content = oat.get_csv_file_content(args.source_file, enc)

    column_name = "column " + str(args.count_column)
    if header:
        header_line = header[0]
        column_name = header_line[args.count_column]

    oat.print_g("Performing occurence count in column '" + column_name + "'")
    occurence_dict = OrderedDict()

    for line in content:
        try:
            value = line[args.count_column]
        except IndexError as ie:
            oat.print_y("IndexError ({}) at line {}, skipping...".format(ie.message, line))
            continue
        if value not in occurence_dict:
            occurence_dict[value] = 1
        else:
            occurence_dict[value] += 1

    if args.sort:
        occurence_dict = OrderedDict(sorted(occurence_dict.items(), key=lambda x: x[1],
                                            reverse=True))

    for item in occurence_dict.items():
        print(item[0] + ": " + str(item[1]))

if __name__ == '__main__':
    main()
