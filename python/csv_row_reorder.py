#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The csv file where rows should be reordered",
    "column": "The numerical index of the column to be used as sorting key",
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
                           "will take precedence.",
    "other_csv_file": "An optional second csv file. If given, the rows in " +
                      "the first file will not be sorted alphabetically. " +
                      "Instead, they will be rearranged so that the values in " +
                      "the denoted column mirror their order " +
                      "of occurence in the given column of the second file " +
                      "(this will obviously only make sense if the columns " +
                      "have common values and the values represent some sort " +
                      "of key). Rows with a column value not occuring in the " +
                      "second file will be appended to the end of the " +
                      "output file in original order.",
    "other_column": "The numerical index of the column to use in the second " +
                    "file. If omitted, the same index as in the first file " +
                    "is used.",
    "other_encoding": "The optional encoding of the second CSV file.",
    "ignore_case": "Ignore case when comparing values for reordering between two files"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("column", type=int, help=ARG_HELP_STRINGS["column"])
    parser.add_argument("other_csv_file", nargs="?", help=ARG_HELP_STRINGS["other_csv_file"])
    parser.add_argument("other_column", type=int, nargs="?", help=ARG_HELP_STRINGS["other_column"])
    parser.add_argument("-e2", "--other_encoding", help=ARG_HELP_STRINGS["other_encoding"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-i", "--ignore_case", action="store_true", default=False,
                        help=ARG_HELP_STRINGS["ignore_case"])
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
            except LookupError:
                print("Error: '" + encoding + "' not found Python's " +
                      "codec collection. Either look for a valid name here " +
                      "(https://docs.python.org/2/library/codecs.html#standard-" +
                      "encodings) or omit this argument to enable automated " +
                      "guessing.")
                sys.exit()
        encs.append(encoding)

    mask = None
    if args.quotemask:
        reduced = args.quotemask.replace("f", "").replace("t", "")
        if reduced:
            print("Error: A quotemask may only contain the letters 't' and 'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]

    header, content = oat.get_csv_file_content(args.csv_file, enc=encs[0])
    column = args.column

    if not args.other_csv_file:
        rearranged_content = header + sorted(content, key=lambda x: x[column])
    else:
        rearranged_content = []
        _, second_content = oat.get_csv_file_content(args.other_csv_file, enc=encs[1])
        other_column = column # default: use same column index as in first file
        if args.other_column:
            other_column = args.other_column

        for other_row in second_content:
            if args.ignore_case:
                matching_rows = [row for row in content if row[column].lower() == other_row[other_column].lower()]
            else:
                matching_rows = [row for row in content if row[column] == other_row[other_column]]
            rearranged_content += matching_rows
            for matching_row in matching_rows:
                content.remove(matching_row)
        unmatched_msg = ("{} rows could not be rearranged (unmatched in second csv file) " +
                         "and were appended to the end of the result file " +
                         "in original order.")
        if content:
            oat.print_y(unmatched_msg.format(len(content)))
        else:
            oat.print_g("All rows matched.")
        rearranged_content = header + rearranged_content + content # append any unmatched rows

    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, False)
        writer.write_rows(rearranged_content)

if __name__ == '__main__':
    main()
