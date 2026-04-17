#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
from collections import OrderedDict
import datetime
import locale
import logging
import os
import shutil
import sys

import openapc_toolkit as oat
from openapc_toolkit import CSVColumn
            
# This reflects the OpenAPC update strategy for the core data / TransAgree files.
# In general, only article-related data will be updated retroactively, while journal-related
# data is persistent after first enrichment. Note that the values for ut and issn_l are only
# listed for the sake of completenness, as they are not touched by the enrichment script anyway. 
OVERWRITE_STRATEGY = {
    "institution": CSVColumn.OW_NEVER,
    "period": CSVColumn.OW_NEVER,
    "euro": CSVColumn.OW_NEVER,
    "doi": CSVColumn.OW_NEVER,
    "is_hybrid": CSVColumn.OW_NEVER,
    "opt_out": CSVColumn.OW_NEVER,
    "publisher": CSVColumn.OW_NEVER,
    "journal_full_title": CSVColumn.OW_NEVER,
    "issn": CSVColumn.OW_NEVER,
    "issn_print": CSVColumn.OW_NEVER,
    "issn_electronic": CSVColumn.OW_NEVER,
    "issn_l": CSVColumn.OW_ALWAYS,
    "license_ref": CSVColumn.OW_ALWAYS,
    "indexed_in_crossref": CSVColumn.OW_NEVER,
    "pmid": CSVColumn.OW_ALWAYS,
    "pmcid": CSVColumn.OW_ALWAYS,
    "ut": CSVColumn.OW_ALWAYS,
    "url": CSVColumn.OW_NEVER,
    "doaj": CSVColumn.OW_NEVER,
    "agreement": CSVColumn.OW_NEVER,
    "group_id": CSVColumn.OW_NEVER,
    "book_title": CSVColumn.OW_NEVER,
    "isbn": CSVColumn.OW_NEVER,
    "isbn_print": CSVColumn.OW_NEVER,
    "isbn_electronic": CSVColumn.OW_NEVER,
    "backlist_oa": CSVColumn.OW_NEVER,
    "colour charge": CSVColumn.OW_NEVER,
    "cover charge": CSVColumn.OW_NEVER,
    "page charge": CSVColumn.OW_NEVER,
    "permission": CSVColumn.OW_NEVER,
    "reprint": CSVColumn.OW_NEVER,
    "submission fee": CSVColumn.OW_NEVER,
    "payment fee": CSVColumn.OW_NEVER,
    "other": CSVColumn.OW_NEVER,
}

ARG_HELP_STRINGS = {
    "csv_file": "CSV file containing your APC data. It must contain at least " +
                "the 5 mandatory columns defined by the OpenAPC data schema: " +
                "institution, period, euro, doi and is_hybrid (in no " +
                "particular order).",
    "ta": 'Treats the input file as containing articles published under a ' +
          'transformative agreement.',
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "verbose": "Be more verbose during the enrichment process.",
    "locale": "Set the locale context used by the script. You might want to " +
              "set this if your system locale differs from the locale the " +
              "CSV file was created in (Example: Using en_US as your system " +
              "locale might become a problem if the file contains numeric " +
              "values with ',' as decimal mark character)",
    "ignore_header": "Ignore any CSV headers (if present) and try to " +
                     "determine relevant columns heuristically.",
    "force_header": "Interpret the file's first line as a header even if the " +
                    "automatic analysis did not detect one.",
    "force": "Force the script to continue even if not all mandatory columns " +
             "have been identified",
    "bypass": "Force the script to bypass TLS certificate verification when " +
              "querying metadata APIs. Not recommended, but might be " +
              "necessary if run under windows (where python does not use the " +
              "cert store of the OS)",
    "unknown_columns": "Attach any unidentified columns to the generated " +
                       "csv file",
    "dialect": "Ignore results of the automated CSV dialect sniffing and use " +
               "a built-in dialect instead",
    "overwrite": "Always overwrite existing data with imported data " +
                 "(instead of asking on the first conflict)",
    "update": "Enforce the OpenAPC update strategy on imported data. This mode is " +
              "meant to work with already enriched APC files.",
    "round_monetary": "Automatically round monetary values with more than two digits " +
                      "after the decimal mark",
    "no_crossref": "Do not import metadata from crossref. Since journal ISSN " +
                   "numbers are imported from crossref, this will also make " +
                   "a DOAJ lookup impossible if no ISSN fields are present in " +
                   "the input data.",
    "unindexed_only": "Skip a line if the article has been found in crossref already. " +
                      "This mode is meant to work with already enriched APC files " +
                      "as it relies on the 'indexed_in_crossref' column",
    "no_pubmed": "Do not import metadata from pubmed.",
    "no_doaj": "Do not look up journals for being listended in the DOAJ.",
    "institution": "Manually identify the 'institution' column if the script " +
                   "fails to detect it automatically. The value is the " +
                   "numerical column index in the CSV file, with the " +
                   "leftmost column being 0.",
    "period": "Manually identify the 'period' column if the script fails to " +
              "detect it automatically. The value is the numerical column " +
              "index in the CSV file, with the leftmost column being 0.",
    "doi": "Manually identify the 'doi' column if the script fails to " +
           "detect it automatically. The value is the numerical column index " +
           "in the CSV file, with the leftmost column being 0.",
    "euro": "Manually identify the 'euro' column if the script fails to " +
            "detect it automatically. The value is the numerical column " +
            "index in the CSV file, with the leftmost column being 0.",
    "is_hybrid": "Manually identify the 'is_hybrid' column if the script " +
                 "fails to detect it automatically. The value is the " +
                 "numerical column index in the CSV file, with the leftmost " +
                 "column being 0.",
    "opt_out": "Manually identify the 'opt_out' column if the script " +
               "fails to detect it automatically. The value is the " +
               "numerical column index in the CSV file, with the leftmost " +
               "column being 0.",
    "publisher": "Manually identify the 'publisher' column if the script " +
                 "fails to detect it automatically. The value is the " +
                 "numerical column index in the CSV file, with the leftmost " +
                 "column being 0. This is an optional column, identifying it " +
                 "is required if there are articles without a DOI in the file.",
    "journal_full_title": "Manually identify the 'journal_full_title' column " +
                          "if the script fails to detect it automatically. " +
                          "The value is the numerical column index in the " +
                          "CSV file, with the leftmost column being 0. This " +
                          "is an optional column, identifying it is required " +
                          "if there are articles without a DOI in the file.",
    "book_title": "Manually identify the 'book_title' column if the script fails " +
                  "to detect it automatically. The value is the numerical column " +
                  "index in the CSV file, with the leftmost column being 0. This " +
                  "is a non-reqired column, identifying it may be helpful for cases " +
                  "where both Crossref and DOAB lookup provide no results",
    "issn": "Manually identify the 'issn' column if the script fails to " +
            "detect it automatically. The value is the numerical column " +
            "index in the CSV file, with the leftmost column being 0. This " +
            "is an optional column, identifying it is required if there are " +
            "articles without a DOI in the file.",
    "isbn": "Manually identify the 'isbn' column if the script fails to " +
            "detect it automatically. The value is the numerical column " +
            "index in the CSV file, with the leftmost column being 0. This " +
            "is an optional column, identifying it is required if there are " +
            "books without a DOI in the file.",
    "backlist_oa": "Manually identify the 'backlist_oa' column if the script " +
                   "fails to detect it automatically. The value is the " +
                   "numerical column index in the CSV file, with the leftmost " +
                   "column being 0.",
    "additional_isbns": "Identify more optional columns containing ISBN "+
                        "values in addition to isbn, isbn_print and isbn_electronic. " +
                        "The value is a whitespace-separated list of numerical column " +
                        "indexes in the CSV file, with the leftmost column being 0. " +
                        "Providing additional ISBNs for other variants/editions of a " +
                        "book can be helpful during metadata discovery. These columns won't " +
                        "be mapped to the output file.",
    "crossref_max_retries": "Maximum number of attempts to retry a crossref " +
                            "query for a single line if a 504 Error (Gateway " +
                            "Timeout) is encountered",
    "no_preprint_lookup" : "Do not try to discover DOIs for final versions of " +
                           "preprint papers automatically",
    "preprint_auto_accept": "When a match is found during preprint lookup, accept " +
                            "the DOI automatically if the title similarity is at " +
                            "least 0.9 ('good' matches). Can not be used together with " +
                            "no_preprint_lookup",
    "url": "Manually identify the 'url' column if the script fails to detect " +
           "it automatically. The value is the numerical column index in the " +
           "CSV file, with the leftmost column being 0. This is an optional " +
           "column, identifying it is required if there are articles without " +
           "a DOI in the file.",
    "start": "Do not process the whole file, but start from this line " +
             "number. May be used together with '-end' to select a specific " +
             "segment.",
    "end": "Do not process the whole file, but end at this line number. May " +
           "be used together with '-start' to select a specific segment."
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-T", "--ta_mode", action="store_true", help=ARG_HELP_STRINGS["ta"])
    parser.add_argument("-b", "--bypass-cert-verification", action="store_true",
                        help=ARG_HELP_STRINGS["bypass"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-f", "--force", action="store_true",
                        help=ARG_HELP_STRINGS["force"])
    parser.add_argument("-i", "--ignore-header", action="store_true",
                        help=ARG_HELP_STRINGS["ignore_header"])
    parser.add_argument("-j", "--force-header", action="store_true",
                        help=ARG_HELP_STRINGS["force_header"])
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-a", "--add-unknown-columns", action="store_true",
                        help=ARG_HELP_STRINGS["unknown_columns"])
    parser.add_argument("-d", "--dialect", choices=["excel", "excel-tab", "unix"],
                        help=ARG_HELP_STRINGS["dialect"])
    parser.add_argument("-v", "--verbose", action="store_true",
                        help=ARG_HELP_STRINGS["verbose"])
    parser.add_argument("-o", "--overwrite", action="store_true",
                        help=ARG_HELP_STRINGS["overwrite"])
    parser.add_argument("-u", "--update", action="store_true",
                        help=ARG_HELP_STRINGS["update"])
    parser.add_argument("-U", "--unindexed_only", action="store_true",
                        help=ARG_HELP_STRINGS["unindexed_only"])
    parser.add_argument("-r", "--round_monetary", action="store_true",
                        help=ARG_HELP_STRINGS["round_monetary"])
    parser.add_argument("-p", "--no-preprint-lookup", action="store_true",
                        help=ARG_HELP_STRINGS["no_preprint_lookup"])
    parser.add_argument("-P", "--preprint_auto_accept", action="store_true",
                        help=ARG_HELP_STRINGS["preprint_auto_accept"])
    parser.add_argument("--no-crossref", action="store_true",
                        help=ARG_HELP_STRINGS["no_crossref"])
    parser.add_argument("--no-pubmed", action="store_true",
                        help=ARG_HELP_STRINGS["no_pubmed"])
    parser.add_argument("--no-doaj", action="store_true",
                        help=ARG_HELP_STRINGS["no_doaj"])
    parser.add_argument("-institution", "--institution_column", type=int,
                        help=ARG_HELP_STRINGS["institution"])
    parser.add_argument("-period", "--period_column", type=int,
                        help=ARG_HELP_STRINGS["period"])
    parser.add_argument("-doi", "--doi_column", type=int,
                        help=ARG_HELP_STRINGS["doi"])
    parser.add_argument("-euro", "--euro_column", type=int,
                        help=ARG_HELP_STRINGS["euro"])
    parser.add_argument("-is_hybrid", "--is_hybrid_column", type=int,
                        help=ARG_HELP_STRINGS["is_hybrid"])
    parser.add_argument("-opt_out", "--opt_out_column", type=int,
                        help=ARG_HELP_STRINGS["opt_out"])
    parser.add_argument("-publisher", "--publisher_column", type=int,
                        help=ARG_HELP_STRINGS["publisher"])
    parser.add_argument("-journal_full_title", "--journal_full_title_column",
                        type=int, help=ARG_HELP_STRINGS["journal_full_title"])
    parser.add_argument("-book_title", "--book_title_column",
                        type=int, help=ARG_HELP_STRINGS["book_title"])
    parser.add_argument("-issn", "--issn_column",
                        type=int, help=ARG_HELP_STRINGS["issn"])
    parser.add_argument("-isbn", "--isbn_column",
                        type=int, help=ARG_HELP_STRINGS["isbn"])
    parser.add_argument("-backlist_oa", "--backlist_oa_column",
                        type=int, help=ARG_HELP_STRINGS["backlist_oa"])
    parser.add_argument("-additional_isbns", "--additional_isbn_columns", type=int, nargs='+',
                        help=ARG_HELP_STRINGS["additional_isbns"])
    parser.add_argument("-url", "--url_column",
                        type=int, help=ARG_HELP_STRINGS["url"])
    parser.add_argument("-c", "--crossref_max_retries", type=int, default=3,
                        help=ARG_HELP_STRINGS["crossref_max_retries"])
    parser.add_argument("-start", type=int, help=ARG_HELP_STRINGS["start"])
    parser.add_argument("-end", type=int, help=ARG_HELP_STRINGS["end"])

    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(oat.ANSIColorFormatter())
    bufferedHandler = oat.BufferedErrorHandler(handler)
    bufferedHandler.setFormatter(oat.ANSIColorFormatter())
    logging.root.addHandler(handler)
    logging.root.addHandler(bufferedHandler)
    logging.root.setLevel(logging.INFO)

    if args.locale:
        norm = locale.normalize(args.locale)
        if norm != args.locale:
            msg = "locale '{}' not found, normalised to '{}'".format(
                  args.locale, norm)
            oat.print_y(msg)
        try:
            loc = locale.setlocale(locale.LC_ALL, norm)
            oat.print_g("Using locale " + loc)
        except locale.Error as loce:
            msg = "Setting locale to {} failed: {}".format(norm, loce.message)
            oat.print_r(msg)
            sys.exit()

    enc = None # CSV file encoding
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = ("Encoding '{}' found in Python's codec collection " +
                   "as '{}'").format(args.encoding, codec.name)
            oat.print_g(msg)
            enc = args.encoding
        except LookupError:
            msg = ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            oat.print_r(msg)
            sys.exit()

    result = oat.analyze_csv_file(args.csv_file, enc=enc)
    if result["success"]:
        csv_analysis = result["data"]
        print(csv_analysis)
    else:
        print(result["error_msg"])
        sys.exit()

    if args.dialect:
        dialect = args.dialect
        oat.print_g('Dialect sniffing results ignored, using built-in CSV dialect "' + dialect + '"')
    else:
        dialect = csv_analysis.dialect

    if enc is None:
        enc = csv_analysis.enc
    has_header = csv_analysis.has_header or args.force_header

    if enc is None:
        print("Error: No encoding given for CSV file and automated " +
              "detection failed. Please set the encoding manually via the " +
              "--enc argument")
        sys.exit()

    csv_file = open(args.csv_file, "r", encoding=enc)
    reader = csv.reader(csv_file, dialect=dialect)

    first_row = next(reader)
    num_columns = len(first_row)
    print("\nCSV file has {} columns.".format(num_columns))

    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect=dialect)

    if args.update and args.overwrite:
        oat.print_r("Error: Either use the -u or the -o option, not both.")
        sys.exit()

    if args.overwrite:
        for column in OVERWRITE_STRATEGY.keys():
             OVERWRITE_STRATEGY[column] = CSVColumn.OW_ALWAYS
    elif not args.update:
        for column in OVERWRITE_STRATEGY.keys():
             OVERWRITE_STRATEGY[column] = CSVColumn.OW_ASK

    if args.no_preprint_lookup and args.preprint_auto_accept:
        oat.print_r("Error: Either use the -P or the -p option, not both.")
        sys.exit()

    additional_isbn_columns = []
    if args.additional_isbn_columns:
        for index in args.additional_isbn_columns:
            if index > num_columns:
                msg = "Error: Additional ISBN column index {} exceeds number of columns ({})."
                oat.print_r(msg.format(index, num_columns))
                sys.exit()
            else:
                additional_isbn_columns.append(index)

    column_map = {
        "institution": CSVColumn("institution",
            {
                "articles": CSVColumn.MANDATORY,
                "ta": CSVColumn.MANDATORY,
                "books": CSVColumn.MANDATORY
            },
            args.institution_column, overwrite=OVERWRITE_STRATEGY["institution"]),
        "period": CSVColumn("period",
            {
                "articles": CSVColumn.MANDATORY,
                "ta": CSVColumn.MANDATORY,
                "books": CSVColumn.MANDATORY
            },
            args.period_column, overwrite=OVERWRITE_STRATEGY["period"]),
        "euro": CSVColumn("euro",
            {
                "articles": CSVColumn.MANDATORY,
                "ta": CSVColumn.DEFAULT_NA,
                "books": CSVColumn.MANDATORY,
            },
            args.euro_column, overwrite=OVERWRITE_STRATEGY["euro"]),
        "doi": CSVColumn("doi",
            {
                "articles": CSVColumn.MANDATORY,
                "ta": CSVColumn.MANDATORY,
                "books": CSVColumn.MANDATORY
            },
            args.doi_column, overwrite=OVERWRITE_STRATEGY["doi"]),
        "is_hybrid": CSVColumn("is_hybrid",
            {
                "articles": CSVColumn.DEFAULT_NA,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            args.is_hybrid_column, overwrite=OVERWRITE_STRATEGY["is_hybrid"]),
        "opt_out": CSVColumn("opt_out",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.DEFAULT_FALSE,
                "books": CSVColumn.NONE
            },
            args.opt_out_column, overwrite=OVERWRITE_STRATEGY["opt_out"]),
        "publisher": CSVColumn("publisher",
            {
                "articles": CSVColumn.BACKUP,
                "ta": CSVColumn.BACKUP,
                "books": CSVColumn.NONE
            },
            args.publisher_column, overwrite=OVERWRITE_STRATEGY["publisher"]),
        "journal_full_title": CSVColumn("journal_full_title",
            {
                "articles": CSVColumn.BACKUP,
                "ta": CSVColumn.BACKUP,
                "books": CSVColumn.NONE
            },
            args.journal_full_title_column, overwrite=OVERWRITE_STRATEGY["journal_full_title"]),
        "issn": CSVColumn("issn",
            {
                "articles": CSVColumn.BACKUP,
                "ta": CSVColumn.BACKUP,
                "books": CSVColumn.NONE
            },
            args.issn_column, overwrite=OVERWRITE_STRATEGY["issn"]),
        "issn_print": CSVColumn("issn_print",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["issn_print"]),
        "issn_electronic": CSVColumn("issn_electronic",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["issn_electronic"]),
        "issn_l": CSVColumn("issn_l",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["issn_l"]),
        "license_ref": CSVColumn("license_ref",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["license_ref"]),
        "indexed_in_crossref": CSVColumn("indexed_in_crossref",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["indexed_in_crossref"]),
        "pmid": CSVColumn("pmid",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["pmid"]),
        "pmcid": CSVColumn("pmcid",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["pmcid"]),
        "ut": CSVColumn("ut",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["ut"]),
        "url": CSVColumn("url",
            {
                "articles": CSVColumn.BACKUP,
                "ta": CSVColumn.BACKUP,
                "books": CSVColumn.NONE
            },
            args.url_column, overwrite=OVERWRITE_STRATEGY["url"]),
        "doaj": CSVColumn("doaj",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["doaj"]),
        "agreement": CSVColumn("agreement",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.BACKUP,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["agreement"]),
        "group_id": CSVColumn("group_id",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["group_id"]),
        "book_title": CSVColumn("book_title",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.RECOMMENDED
            },
            args.book_title_column, overwrite=OVERWRITE_STRATEGY["book_title"]),
        "backlist_oa": CSVColumn("backlist_oa",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.DEFAULT_FALSE
            },
            args.backlist_oa_column, overwrite=OVERWRITE_STRATEGY["backlist_oa"]),
        "isbn": CSVColumn("isbn",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.BACKUP
            },
            args.isbn_column, overwrite=OVERWRITE_STRATEGY["isbn"]),
        "isbn_print": CSVColumn("isbn_print",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["isbn_print"]),
        "isbn_electronic": CSVColumn("isbn_electronic",
            {
                "articles": CSVColumn.NONE,
                "ta": CSVColumn.NONE,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["isbn_electronic"]),
        "colour charge": CSVColumn("colour charge",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["colour charge"]),
        "cover charge": CSVColumn("cover charge",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["cover charge"]),
        "page charge": CSVColumn("page charge",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["page charge"]),
        "permission": CSVColumn("permission",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["permission"]),
        "reprint": CSVColumn("reprint",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["reprint"]),
        "submission fee": CSVColumn("submission fee",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["submission fee"]),
        "payment fee": CSVColumn("payment fee",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["payment fee"]),
        "other": CSVColumn("other",
            {
                "articles": CSVColumn.ADDITIONAL_COSTS,
                "ta": CSVColumn.ADDITIONAL_COSTS,
                "books": CSVColumn.NONE
            },
            None, overwrite=OVERWRITE_STRATEGY["other"]),
    }

    header = None
    if has_header:
        for row in reader:
            if not row: # Skip empty lines
                continue
            header = row # First non-empty row should be the header
            if args.ignore_header:
                print("Skipping header analysis due to command line argument.")
                break
            else:
                print("\n    *** Analyzing CSV header ***\n")
            for (index, item) in enumerate(header):
                if index in additional_isbn_columns:
                    msg = "Column named '{}' at index {} is designated as additional ISBN column"
                    print(msg.format(item, index))
                    continue
                column_type = oat.get_column_type_from_whitelist(item)
                if column_type is not None and column_map[column_type].index is None:
                    column_map[column_type].index = index
                    column_map[column_type].column_name = item
                    found_msg = ("Found column named '{}' at index {}, " +
                                 "assuming this to be the '{}' column.")
                    print(found_msg.format(item, index, column_type))
            break


    print("\n    *** Starting heuristical analysis ***\n")
    for row in reader:
        if not row: # Skip empty lines
            # We analyze the first non-empty line, a possible header should
            # have been processed by now.
            continue
        column_candidates = {
            "doi": [],
            "period": [],
            "euro": []
        }
        found_msg = "The entry in column {} looks like a potential {}: {}"
        for (index, entry) in enumerate(row):
            if index in [csvcolumn.index for csvcolumn in column_map.values()] + additional_isbn_columns:
                # Skip columns already assigned
                continue
            entry = entry.strip()
            # Search for a DOI
            if column_map['doi'].index is None:
                if oat.DOI_RE.match(entry):
                    column_id = str(index)
                    # identify column either numerically or by column header
                    if header:
                        column_id += " ('" + header[index] + "')"
                    print(found_msg.format(column_id, "DOI", entry))
                    column_candidates['doi'].append(index)
                    continue
            # Search for a potential year string
            if column_map['period'].index is None:
                try:
                    maybe_period = int(entry)
                    now = datetime.date.today().year
                    # Should be a wide enough margin
                    if maybe_period >= 2000 and maybe_period <= now + 2:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print(found_msg.format(column_id, "year", entry))
                        column_candidates['period'].append(index)
                        continue
                except ValueError:
                    pass
            # Search for a potential monetary amount
            if column_map['euro'].index is None:
                try:
                    maybe_euro = locale.atof(entry)
                    if maybe_euro >= 10 and maybe_euro <= 10000:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print (found_msg.format(column_id, "euro amount", entry))
                        column_candidates['euro'].append(index)
                        continue
                except ValueError:
                    pass
        for column_type, candidates in column_candidates.items():
            if column_map[column_type].index is not None:
                continue
            if len(candidates) > 1:
                print("Could not reliably identify the '" + column_type +
                      "' column - more than one possible candiate!")
            elif len(candidates) < 1:
                print("No candidate found for column '" + column_type + "'!")
            else:
                index = candidates.pop()
                column_map[column_type].index = index
                if header:
                    column_id = header[index]
                    column_map[column_type].column_name = column_id
                else:
                    column_id = index
                msg = "Assuming column '{}' to be the '{}' column."
                print(msg.format(column_id, column_type))
                column_map[column_type].index = index
        break

    print("\n    *** CSV file analysis summary ***\n")

    index_dict = {csvc.index: csvc for csvc in column_map.values()}

    for index in range(num_columns):
        column_name = ""
        if header:
            column_name = header[index]
        if index in index_dict:
            column = index_dict[index]
            msg = u"column number {} ({}) is the '{}' column ({})".format(
                index, column_name, column.column_type, column.get_req_description())
            print(msg)
        elif index in additional_isbn_columns:
            msg = u"column number {} ({}) is an additional ISBN column".format(index, column_name)
            oat.print_c(msg)
        else:
            if args.add_unknown_columns:
                msg = (u"column number {} ({}) is an unknown column, it will be " +
                       "appended to the generated CSV file")
                print(msg.format(index, column_name))
                if not column_name:
                    # Use a generic name
                    column_name = "unknown"
                while column_name in column_map.keys():
                    # TODO: Replace by a numerical, increasing suffix
                    column_name += "_"
                column_map[column_name] = CSVColumn("added_unknown_column", None, index, column_name)
            else:
                msg = (u"column number {} ({}) is an unknown column, it will be " +
                       "ignored")
                print(msg.format(index, column_name))

    print()
    for column in column_map.values():
        if column.index is None and column.column_type != "unknown_column":
            msg = "The '{}' column could not be identified ({})"
            print(msg.format(column.column_type, column.get_req_description()))
    print()

    article_mand_missing = [x.column_type for x in column_map.values() if x.requirement["articles"] == CSVColumn.MANDATORY and x.index is None]
    article_back_missing = [x.column_type for x in column_map.values() if x.requirement["articles"] == CSVColumn.BACKUP and x.index is None]
    ta_mand_missing = [x.column_type for x in column_map.values() if x.requirement["ta"] == CSVColumn.MANDATORY and x.index is None]
    ta_back_missing = [x.column_type for x in column_map.values() if x.requirement["ta"] == CSVColumn.BACKUP and x.index is None]
    book_mand_missing = [x.column_type for x in column_map.values() if x.requirement["books"] == CSVColumn.MANDATORY and x.index is None]
    book_back_missing = [x.column_type for x in column_map.values() if x.requirement["books"] == CSVColumn.BACKUP and x.index is None]

    if article_mand_missing:
        msg = "Article enrichment is not possible - mandatory columns are missing ({})"
        oat.print_y(msg.format(", ".join(article_mand_missing)))
    elif article_back_missing:
        msg = "Article enrichment is possible, but backup columns are missing ({})"
        oat.print_b(msg.format(", ".join(article_back_missing)))
    else:
        oat.print_g("Article enrichment is possible with all backup columns in place")
    if ta_mand_missing:
        msg = "TA enrichment is not possible - mandatory columns are missing ({})"
        oat.print_y(msg.format(", ".join(article_mand_missing)))
    elif ta_back_missing:
        msg = "TA enrichment is possible, but backup columns are missing ({})"
        oat.print_b(msg.format(", ".join(article_back_missing)))
    else:
        oat.print_g("Article enrichment is possible with all backup columns in place")
    if book_mand_missing:
        msg = "Book enrichment is not possible - mandatory columns are missing ({})"
        oat.print_y(msg.format(", ".join(book_mand_missing)))
    elif book_back_missing:
        msg = "Book enrichment is possible, but backup columns are missing ({})"
        oat.print_b(msg.format(", ".join(book_back_missing)))
    else:
        oat.print_g("Book enrichment is possible with all backup columns in place")
    print()

    if article_mand_missing and book_mand_missing and ta_mand_missing:
        if not args.force:
            oat.print_r("ERROR: Could not detect the minimum mandatory data set for any " + 
                  "publication type. There are 2 ways to fix this:")
            if not header:
                print("1) Add a header row to your file and identify the " +
                      "column(s) by assigning them an appropiate column name.")
            else:
                print("1) Identify the missing column(s) by assigning them " +
                      "a different column name in the CSV header (You can " +
                      "use the column name(s) mentioned in the message above)")
            print("2) Use command line parameters when calling this script " +
                  "to identify the missing columns (use -h for help) ")
            sys.exit()
        else:
            oat.print_y("WARNING: Could not detect the minimum mandatory data set for any " + 
                  "publication type - forced to continue.")

    if args.unindexed_only and column_map["indexed_in_crossref"].index is None:
        oat.print_r("ERROR: Unindexed update mode (-U) requires the 'indexed_in_crossref' column!")
        sys.exit()

    start = input("\nStart metadata aggregation? (y/n):")
    while start not in ["y", "n"]:
        start = input("Please type 'y' or 'n':")
    if start == "n":
        sys.exit()

    print("\n    *** Starting metadata aggregation ***\n")

    enriched_content = {}
    for record_type, fields in oat.COLUMN_SCHEMAS.items():
        # add headers
        header = list(fields)
        for _, column in column_map.items():
            if column.column_type == "added_unknown_column":
                header.append(column.column_name)
        enriched_content[record_type] = {
            "count": 0,
            "content": [header]
        }

    if not os.path.isdir("tempfiles"):
        os.mkdir("tempfiles")
    isbn_handling = oat.ISBNHandling()
    doab_analysis = oat.DOABAnalysis(isbn_handling, "tempfiles/DOAB.csv", verbose=False)
    doaj_analysis = oat.DOAJAnalysis(max_mdays=30, verbose=True)
    issnl_handling = None
    try:
        issnl_handling = oat.ISSNLHandling()
    except Exception as e:
        msg = ("WARNING: An exception occured while trying to set up " +
               "the ISSN-L handling: \n{}\nISSN-L enrichment during " +
               "processing will not work.")
        oat.print_y(msg.format(e))

    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect=dialect)
    header_processed = False
    row_num = 0

    ac_value_found = False

    for row in reader:
        row_num += 1
        if not row:
            continue # skip empty lines
        if not header_processed:
            header_processed = True
            if has_header:
                # If the CSV file has a header, we are currently there - skip it
                # to get to the first data row
                continue
        if args.start and args.start > row_num:
            continue
        if args.end and args.end < row_num:
            continue
        print("---Processing line number " + str(row_num) + "---")
        no_crossref = args.no_crossref
        no_pubmed = args.no_pubmed
        no_doaj = args.no_doaj
        if args.unindexed_only:
            indexed = row[column_map["indexed_in_crossref"].index]
            if indexed == "TRUE":
                logging.info("Record already looked up in crossref, skipping...")
                no_crossref = True
                no_pubmed = True
                no_doaj = True
        enriched_rows = oat.process_row(row, row_num, column_map, num_columns, additional_isbn_columns, doab_analysis, doaj_analysis,
                                        issnl_handling, no_crossref, no_pubmed, no_doaj, args.no_preprint_lookup, args.preprint_auto_accept,
                                        args.round_monetary, args.ta_mode, args.csv_file, args.crossref_max_retries)
        if not ac_value_found and "additional_costs" in enriched_rows:
            for index in range(1, len(enriched_rows["additional_costs"])): # index 0 is the DOI
                if oat.has_value(enriched_rows["additional_costs"][index]):
                    ac_value_found = True
        for record_type, value in enriched_content.items():
            if record_type in enriched_rows:
                value["content"].append(enriched_rows[record_type])
                value["count"] += 1
            elif record_type != "contracts":
                empty_line = ["" for x in value["content"][0]]
                value["content"].append(empty_line)
    csv_file.close()

    if "contracts" in enriched_content:
        dedup_list = []
        previous = len(enriched_content["contracts"]["content"])
        for row in enriched_content["contracts"]["content"]:
            if row not in dedup_list:
                dedup_list.append(row)
        enriched_content["contracts"]["content"] = dedup_list
        msg = "Creating out_contracts.csv (automatically deduplicated from {} to {} entries)"
        oat.print_g(msg.format(previous - 1, len(dedup_list) - 1))

    num_different_record_types = 0
    last_out_file_name = None
    for record_type, value in enriched_content.items():
        if value["count"] > 0:
            quotemask = oat.QUOTEMASKS.get(record_type, oat.QUOTEMASKS.get("journal-article"))
            if record_type != "additional_costs":
                num_different_record_types += 1
                last_out_file_name = 'out_' + record_type + '.csv'
            with open('out_' + record_type + '.csv', 'w') as out:
                writer = oat.OpenAPCUnicodeWriter(out, quotemask,
                                                  True, True, True)
                writer.write_rows(value["content"])

    if not bufferedHandler.buffer:
        oat.print_g("Metadata enrichment successful, no errors occured")
        # Directly created an enriched file if there were no errors and only a single record type
        if num_different_record_types == 1:
            path, file_name = os.path.split(args.csv_file)
            file_parts = file_name.split(".")
            if file_parts[0].endswith("_postprocessed"):
                file_parts[0] = file_parts[0][:-14]
            file_parts[0] += "_enriched"
            enriched_name = ".".join(file_parts)
            enriched_path = os.path.join(path, enriched_name)
            if not os.path.isfile(enriched_path):
                msg = "Enriched file will be created automatically: '{}'"
                oat.print_g(msg.format(enriched_path))
                shutil.copy2(last_out_file_name, enriched_path)
            else:
                msg = "Could not create enriched file '{}' - file exists!"
                oat.print_y(msg.format(enriched_path))
    else:
        oat.print_r("There were errors during the enrichment process:\n")

    # closing will implicitly flush the handler and print any buffered
    # messages to stderr
    bufferedHandler.close()
    if ac_value_found:
        oat.print_m("ATTENTION: Non-zero additional costs found in table - file out_additional_costs.csv should be appended and squashed.")

if __name__ == '__main__':
    main()
