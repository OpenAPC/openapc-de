#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import os
import sys

from pathlib import Path

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "first_file": "The first CSV file to compare",
    "second_file": "The second CSV file to compare",
    "first_index": "The index of the CSV column which contains the " + 
                   "comparison values in the first file. The leftmost " +
                   "column has index 0.",
    "second_index": "The index of the CSV column which contains the " + 
                   "comparison values in the second file. The leftmost " +
                   "column has index 0.",
    "doi_normalisation": "Apply standard OpenAPC DOI normalisation to " +
                         "the compare values.",
    "encoding": "The encoding of the first file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "other_encoding": "The encoding of the second file."
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("first_file", help=ARG_HELP_STRINGS["first_file"])
    parser.add_argument("first_index", type=int, help='first_index')
    parser.add_argument("second_file", help=ARG_HELP_STRINGS["second_file"])
    parser.add_argument("second_index", type=int, help='second_index')
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-e2", "--other_encoding", help=ARG_HELP_STRINGS["other_encoding"])
    parser.add_argument("-d", "--doi_normalisation", action="store_true", help=ARG_HELP_STRINGS["doi_normalisation"])

    args = parser.parse_args()

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

    first_header, first_content = oat.get_csv_file_content(args.first_file, enc=encs[0])
    second_header, second_content = oat.get_csv_file_content(args.second_file, enc=encs[1])

    files = {
        "first_file": {
            "name": Path(args.first_file).stem,
            "content": first_content,
            "index": args.first_index,
            "header": first_header,
            "mapping": {},
            "na_lines": []
        },
        "second_file": {
            "name":  Path(args.second_file).stem,
            "content": second_content,
            "index": args.second_index,
            "header": second_header,
            "mapping": {},
            "na_lines": []
        }
    }

    for file_name, file_data in files.items():
        index = file_data["index"]
        for line in file_data["content"]:
            value = line[index]
            if not oat.has_value(value):
                file_data["na_lines"].append(line)
                continue
            if args.doi_normalisation:
                value = oat.get_normalised_DOI(value)
            if value in file_data["mapping"]:
                file_data["mapping"][value].append(line)
            else:
                file_data["mapping"][value] = [line]

    matches = list(
        set(files["first_file"]["mapping"].keys()) & 
        set(files["second_file"]["mapping"].keys())
    )

    for match in matches:
        first_file_lines = files["first_file"]["mapping"][match]
        second_file_lines = files["second_file"]["mapping"][match]
        if len(first_file_lines) > 1 or len(second_file_lines) > 1:
            msg = ('WARNING: Duplicate found. The value "{}" occurs {} ' +
                   'times in "{}" and {} times in "{}".')
            msg = msg.format(value, 
                             len(first_file_lines),
                             files["first_file"]["name"],
                             len(second_file_lines),
                             files["second_file"]["name"],
            )
            oat.print_y(msg)
        del(files["first_file"]["mapping"][match])
        del(files["second_file"]["mapping"][match])

    for file_name, file_data in files.items():
        target_name = "only_in_" + file_data["name"] + ".csv"
        with open(target_name, 'w') as out:
            content = []
            for value, lines in file_data["mapping"].items():
                content += lines
            writer = oat.OpenAPCUnicodeWriter(out, None, True, True)
            writer.write_rows(file_data["header"] + content)

if __name__ == '__main__':
    main()
