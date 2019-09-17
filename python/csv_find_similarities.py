#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import sys

from Levenshtein import ratio

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The csv input file",
    "index": "The index of the column to find similarities in",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "min_ratio": "The minimum Levenshtein distance ratio between two entities to appear in the " +
                 "results list"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("index", type=int, help=ARG_HELP_STRINGS["index"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-m", "--min_ratio", type=float, help=ARG_HELP_STRINGS["min_ratio"],
                        default=0.0)

    args = parser.parse_args()

    if args.min_ratio < 0.0 or args.min_ratio > 1.0:
        oat.print_r("Error: min_ratio parameter must be a float between 0.0 and 1.0")
        sys.exit()

    enc = None
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            print(msg.format(args.encoding, codec.name))
            enc = args.encoding
        except LookupError:
            print("Error: '" + args.encoding + "' not found Python's " +
                  "codec collection. Either look for a valid name here " +
                  "(https://docs.python.org/2/library/codecs.html#standard-" +
                  "encodings) or omit this argument to enable automated " +
                  "guessing.")
            sys.exit()

    header, content = oat.get_csv_file_content(args.csv_file, enc)
    header = header.pop()

    entities = []
    line_num = 0
    msg = "Processed {} entries in column '{}', {} unique entities found."
    last_msg = None
    for line in content:
        line_num += 1
        if line[args.index] not in entities:
            entities.append(line[args.index])
        if line_num == len(content) or line_num % 100 == 0:
            last_msg = msg.format(line_num, header[args.index], len(entities))
            print(last_msg, end="\r")
    print(last_msg)

    sim_pairs = []
    n = len(entities) - 1
    num_pairs = int((n*n + n) / 2)
    msg = ("Calculated Levenshtein ratio for {} out of {} possible entity combinations ({}%), " +
           "{} have passed the minimum ratio so far.")
    last_msg = None
    num_calcs = 0
    while entities:
        first_part = entities.pop(0)
        for second_part in entities:
            lev_ratio = ratio(first_part, second_part)
            num_calcs += 1
            if lev_ratio >= args.min_ratio:
                sim_pairs.append([first_part, second_part, str(lev_ratio)])
            if num_calcs == num_pairs or num_calcs % 100 == 0:
                last_msg = msg.format(num_calcs, num_pairs, round(num_calcs/num_pairs * 100, 1),
                                      len(sim_pairs))
                print(last_msg, end="\r")
    print(last_msg)

    sim_pairs.sort(key=lambda x: x[2], reverse=True)
    sim_pairs.insert(0, ["first_item", "second_item", "levenshtein_ratio"])
    with open("out.csv", "w") as out_file:
        writer = oat.OpenAPCUnicodeWriter(out_file)
        writer.write_rows(sim_pairs)


if __name__ == '__main__':
    main()
