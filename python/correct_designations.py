#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import re
import sys

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "The OpenAPC-conforming file where journal and publisher " +
                "names should be updated should be updated",
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
    
    args = parser.parse_args()
    
    quote_rules = args.openapc_quote_rules
    
    enc = None
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            codec_msg = "Encoding '{}' found in Python's codec collection as '{}'"
            oat.print_g(codec_msg.format(args.encoding, codec.name))
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

    line_num = 1
    for line in content:
        publisher = line[5]
        journal = line[6]
        journal_new = oat.get_unified_journal_title(journal)
        publisher_new = oat.get_unified_publisher_name(publisher)
        if publisher_new != publisher:
            line[5] = publisher_new
            msg = u"Line {}: Updated publisher name ({} -> {})"
            oat.print_g(msg.format(line_num, publisher, publisher_new))
        if journal_new != journal:
            line[6] = journal_new
            msg = u"Line {}: Updated journal_full_title ({} -> {})"
            oat.print_g(msg.format(line_num, journal, journal_new))
        line_num += 1
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, True)
        writer.write_rows(header + content)

if __name__ == '__main__':
    main()
