#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import re

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "apc_file": "The apc csv file to be enriched with linking issns. Must " +
                "conform to the OpenAPC data schema 3.0.",
    "issn_l_file": "The issn_l mapping file which can be downloaded at " +
                    "issn.org. This script needs the 'ISSN-to-ISSN-L variant.",
    "encoding": "The encoding of the apc file. Setting this argument will " +
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

def reformat_issn(issn):
    if "-" not in issn:
        return issn[:4] + "-"  + issn[4:]
    return issn

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("apc_file", help=ARG_HELP_STRINGS["apc_file"])
    parser.add_argument("issn_l_file", help=ARG_HELP_STRINGS["issn_l_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-q", "--quotemask", help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-o", "--openapc_quote_rules", 
                        help=ARG_HELP_STRINGS["openapc_quote_rules"],
                        action="store_true", default=False)
    
    args = parser.parse_args()
    
    quote_rules = args.openapc_quote_rules

    mask = None
    if args.quotemask:
        reduced = args.quotemask.replace("f", "").replace("t", "")
        if len(reduced) > 0:
            print ("Error: A quotemask may only contain the letters 't' and"  +
                   "'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]
    
    enc = None
    
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            oat.print_g(msg.format(args.encoding, codec.name))
            enc = args.encoding
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()
        
    header, content = oat.get_csv_file_content(args.apc_file, enc)
    
    oat.print_g("Preparing mapping table...")
    itself = other = 0
    issn_l_re = re.compile("^(?P<issn>\d{4}-\d{3}[\dxX])\t(?P<issn_l>\d{4}-\d{3}[\dxX])$")
    issn_l_file = open(args.issn_l_file, "r")
    issn_l_dict = {}
    for i, line in enumerate(issn_l_file):
        if i % 100000 == 0:
            print(str(i) + " lines processed.")
        match = issn_l_re.match(line)
        if match:
            match_dict = match.groupdict()
            issn_l_dict[match_dict['issn']] = match_dict['issn_l']
            if match_dict['issn'] == match_dict['issn_l']:
                itself += 1
            else:
                other += 1
    print(str(itself) + " ISSNs pointing to itself as ISSN-L, " + str(other) + " to another value.")
    oat.print_g("Starting enrichment...")
    
    issn_matches = issn_p_matches = issn_e_matches = unmatched = different = corrections = 0
    enriched_lines = []
    for line in content:
        if len(line) == 0:
            enriched_lines.append(line)
            continue
        issn = reformat_issn(line[7])
        issn_p = reformat_issn(line[8])
        issn_e = reformat_issn(line[9])
        target = None
        if issn in issn_l_dict:
            target = issn_l_dict[issn]
            corrected_target = oat.get_corrected_issn_l(target)
            if corrected_target != target:
                corrections += 1
            line[10] = corrected_target
            issn_matches += 1
        elif issn_p in issn_l_dict:
            target = issn_l_dict[issn_p]
            corrected_target = oat.get_corrected_issn_l(target)
            if corrected_target != target:
                corrections += 1
            line[10] = corrected_target
            issn_p_matches += 1
        elif issn_e in issn_l_dict:
            target = issn_l_dict[issn_e]
            corrected_target = oat.get_corrected_issn_l(target)
            if corrected_target != target:
                corrections += 1
            line[10] = corrected_target
            issn_e_matches += 1
        else:
            unmatched += 1
        if target is not None and target not in [issn, issn_p, issn_e]:
            different += 1
        enriched_lines.append(line)
    
    msg = ("{} issn_l values mapped by issn, {} by issn_p, {} by issn_e. {} " +
           "could not be assigned.\n{} issn_l values were corrected during " +
           "the process.\n In {} cases the ISSN-L was different from all " +
           "existing ISSN values")
    print(msg.format(issn_matches, issn_p_matches, issn_e_matches, 
                     unmatched, corrections, different))

    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, True)
        writer.write_rows(header + enriched_lines)
            

if __name__ == '__main__':
    main()
