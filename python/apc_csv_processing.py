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
import sys

import openapc_toolkit as oat

class CSVColumn(object):

    MANDATORY = "mandatory"
    OPTIONAL = "optional"
    NONE = "non-required"

    OW_ALWAYS = 0
    OW_ASK = 1
    OW_NEVER = 2

    _OW_MSG = (u"\033[91mConflict\033[0m: Existing non-NA value " +
               u"\033[93m{ov}\033[0m in column \033[93m{name}\033[0m is to be " +
               u"replaced by new value \033[93m{nv}\033[0m.\nAllow overwrite?\n" +
               u"1) Yes\n2) Yes, and always replace \033[93m{ov}\033[0m by "+
               "\033[93m{nv}\033[0m in this column\n3) Yes, and always " +
               "overwrite in this column\n4) No\n5) No, and never replace " +
               "\033[93m{ov}\033[0m by \033[93m{nv}\033[0m in this " +
               "column\n6) No, and never overwrite in this column\n>")

    def __init__(self, column_type, requirement, index=None, column_name="", overwrite=OW_ASK):
        self.column_type = column_type
        self.requirement = requirement
        self.index = index
        self.column_name = column_name
        self.overwrite = overwrite
        self.overwrite_whitelist = {}
        self.overwrite_blacklist = {}

    def check_overwrite(self, old_value, new_value):
        if old_value == new_value:
            return old_value
        # Priority: Empty or NA values will always be overwritten.
        if old_value == "NA":
            return new_value
        if old_value.strip() == "":
            return new_value
        # Do not replace an existing old value with NA
        if new_value == "NA":
            return old_value
        if self.overwrite == CSVColumn.OW_ALWAYS:
            return new_value
        if self.overwrite == CSVColumn.OW_NEVER:
            return old_value
        if old_value in self.overwrite_blacklist:
            if self.overwrite_blacklist[old_value] == new_value:
                return old_value
        if old_value in self.overwrite_whitelist:
            return new_value
        msg = CSVColumn._OW_MSG.format(ov=old_value, name=self.column_name,
                                       nv=new_value)
        ret = input(msg)
        while ret not in ["1", "2", "3", "4", "5", "6"]:
            ret = input("Please select a number between 1 and 5:")
        if ret == "1":
            return new_value
        if ret == "2":
            self.overwrite_whitelist[old_value] = new_value
            return new_value
        if ret == "3":
            self.overwrite = CSVColumn.OW_ALWAYS
            return new_value
        if ret == "4":
            return old_value
        if ret == "5":
            self.overwrite_blacklist[old_value] = new_value
            return old_value
        if ret == "6":
            self.overwrite = CSVColumn.OW_NEVER
            return old_value

ARG_HELP_STRINGS = {
    "csv_file": "CSV file containing your APC data. It must contain at least " +
                "the 5 mandatory columns defined by the OpenAPC data schema: " +
                "institution, period, euro, doi and is_hybrid (in no " +
                "particular order).",
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
    "overwrite": "Always overwrite existing data with imported data " +
                 "(instead of asking on the first conflict)",
    "round_monetary": "Automatically round monetary values with more than two digits " +
                      "after the decimal mark",
    "no_crossref": "Do not import metadata from crossref. Since journal ISSN " +
                   "numbers are imported from crossref, this will also make " +
                   "a DOAJ lookup impossible if no ISSN fields are present in " +
                   "the input data.",
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
    "issn": "Manually identify the 'issn' column if the script fails to " +
            "detect it automatically. The value is the numerical column " +
            "index in the CSV file, with the leftmost column being 0. This " +
            "is an optional column, identifying it is required if there are " +
            "articles without a DOI in the file.",
    "url": "Manually identify the 'url' column if the script fails to detect " +
           "it automatically. The value is the numerical column index in the " +
           "CSV file, with the leftmost column being 0. This is an optional " +
           "column, identifying it is required if there are articles without " +
           "a DOI in the file.",
    "offline_doaj": "Use an offline copy of the DOAJ database. This might " +
                    "be useful when processing large files as the DOAJ API " +
                    "is not too responsive at times and might pose a " +
                    "bottleneck. This option expects the CSV you can usually " +
                    "download at https://doaj.org/csv as argument. " +
                    "Obviously, this copy should be as up-to-date as possible.",
    "offline_doaj_download": "Like -d, but will downloaded the needed csv file " +
                             "automatically. Expects a file name which does not " +
                             "exist already.",
    "start": "Do not process the whole file, but start from this line " +
             "number. May be used together with '-end' to select a specific " +
             "segment.",
    "end": "Do not process the whole file, but end at this line number. May " +
           "be used together with '-start' to select a specific segment.",
    "quotemask": "A quotemask to apply to the result file after the " + 
                 "enrichment has been performed. A quotemask is a string " +
                 "consisting only of the letters 't' and 'f' (true/false) " +
                 "and has the same length as there are columns in the " +
                 "resulting csv file. Only the columns where the index is 't' "
                 "will be quoted.",
    "no_openapc_quote_rules": "Do not apply the special openapc quote rules " +
                              "(never quoting NA, TRUE and FALSE to maintain " +
                              "compatibility with R scripts)."
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-b", "--bypass-cert-verification", action="store_true",
                        help=ARG_HELP_STRINGS["bypass"])
    parser.add_argument("-d", "--offline_doaj",
                        help=ARG_HELP_STRINGS["offline_doaj"])
    parser.add_argument("-D", "--offline_doaj_download",
                        help=ARG_HELP_STRINGS["offline_doaj_download"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-f", "--force", action="store_true",
                        help=ARG_HELP_STRINGS["force"])
    parser.add_argument("-i", "--ignore-header", action="store_true",
                        help=ARG_HELP_STRINGS["ignore_header"])
    parser.add_argument("-j", "--force-header", action="store_true",
                        help=ARG_HELP_STRINGS["force_header"])
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-u", "--add-unknown-columns", action="store_true",
                        help=ARG_HELP_STRINGS["unknown_columns"])
    parser.add_argument("-v", "--verbose", action="store_true",
                        help=ARG_HELP_STRINGS["verbose"])
    parser.add_argument("-o", "--overwrite", action="store_true",
                        help=ARG_HELP_STRINGS["overwrite"])
    parser.add_argument("-r", "--round_monetary", action="store_true",
                        help=ARG_HELP_STRINGS["round_monetary"])
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
    parser.add_argument("-publisher", "--publisher_column", type=int,
                        help=ARG_HELP_STRINGS["publisher"])
    parser.add_argument("-journal_full_title", "--journal_full_title_column",
                        type=int, help=ARG_HELP_STRINGS["journal_full_title"])
    parser.add_argument("-issn", "--issn_column",
                        type=int, help=ARG_HELP_STRINGS["issn"])
    parser.add_argument("-url", "--url_column",
                        type=int, help=ARG_HELP_STRINGS["url"])
    parser.add_argument("-start", type=int, help=ARG_HELP_STRINGS["start"])
    parser.add_argument("-end", type=int, help=ARG_HELP_STRINGS["end"])
    parser.add_argument("-q", "--quotemask", default="tffttttttttttttttt",
                        help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-n", "--no-openapc-quote-rules", 
                        help=ARG_HELP_STRINGS["no_openapc_quote_rules"],
                        action="store_true", default=False)

    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(oat.ANSIColorFormatter())
    bufferedHandler = oat.BufferedErrorHandler(handler)
    bufferedHandler.setFormatter(oat.ANSIColorFormatter())
    logging.root.addHandler(handler)
    logging.root.addHandler(bufferedHandler)
    logging.root.setLevel(logging.INFO)
    
    if args.offline_doaj and args.offline_doaj_download:
        oat.print_r("Error: Either use the -d or the -D option, not both.")
        sys.exit()

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

    if enc is None:
        enc = csv_analysis.enc
    dialect = csv_analysis.dialect
    has_header = csv_analysis.has_header or args.force_header

    if enc is None:
        print("Error: No encoding given for CSV file and automated " +
              "detection failed. Please set the encoding manually via the " +
              "--enc argument")
        sys.exit()

    reduced = args.quotemask.replace("f", "").replace("t", "")
    if len(reduced) > 0:
        print("Error: A quotemask may only contain the letters 't' and "  +
              "'f'!")
        sys.exit()
    mask = [True if x == "t" else False for x in args.quotemask]

    doaj_offline_analysis = None
    if args.offline_doaj:
        if os.path.isfile(args.offline_doaj):
            doaj_offline_analysis = oat.DOAJOfflineAnalysis(args.offline_doaj)
        else:
            oat.print_r("Error: " + args.offline_doaj + " does not seem "
                        "to be a file!")
            sys.exit()
    elif args.offline_doaj_download:
        if os.path.isfile(args.offline_doaj_download):
            oat.print_r("Error: Target file '" + args.offline_doaj_download + "' already exists!")
            sys.exit()
        doaj_offline_analysis = oat.DOAJOfflineAnalysis(args.offline_doaj_download, download=True)

    csv_file = open(args.csv_file, "r", encoding=enc)
    reader = csv.reader(csv_file, dialect=dialect)

    first_row = next(reader)
    num_columns = len(first_row)
    print("\nCSV file has {} columns.".format(num_columns))

    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect=dialect)

    if args.overwrite:
        ow_strategy = CSVColumn.OW_ALWAYS
    else:
        ow_strategy = CSVColumn.OW_ASK

    column_map = OrderedDict([
        ("institution", CSVColumn("institution", CSVColumn.MANDATORY, args.institution_column, overwrite=ow_strategy)),
        ("period", CSVColumn("period", CSVColumn.MANDATORY, args.period_column, overwrite=ow_strategy)),
        ("euro", CSVColumn("euro", CSVColumn.MANDATORY, args.euro_column, overwrite=ow_strategy)),
        ("doi", CSVColumn("doi", CSVColumn.MANDATORY, args.doi_column, overwrite=ow_strategy)),
        ("is_hybrid", CSVColumn("is_hybrid", CSVColumn.MANDATORY, args.is_hybrid_column, overwrite=ow_strategy)),
        ("publisher", CSVColumn("publisher", CSVColumn.OPTIONAL, args.publisher_column, overwrite=ow_strategy)),
        ("journal_full_title", CSVColumn("journal_full_title", CSVColumn.OPTIONAL,
                                         args.journal_full_title_column, overwrite=ow_strategy)),
        ("issn", CSVColumn("issn", CSVColumn.OPTIONAL, args.issn_column, overwrite=ow_strategy)),
        ("issn_print", CSVColumn("issn_print", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("issn_electronic", CSVColumn("issn_electronic", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("issn_l", CSVColumn("issn_l", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("license_ref", CSVColumn("license_ref", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("indexed_in_crossref", CSVColumn("indexed_in_crossref", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("pmid", CSVColumn("pmid", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("pmcid", CSVColumn("pmcid", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("ut", CSVColumn("ut", CSVColumn.NONE, None, overwrite=ow_strategy)),
        ("url", CSVColumn("url", CSVColumn.OPTIONAL, args.url_column, overwrite=ow_strategy)),
        ("doaj", CSVColumn("doaj", CSVColumn.NONE, None, overwrite=ow_strategy))
    ])

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
                column_type = oat.get_column_type_from_whitelist(item)
                if column_type is not None and column_map[column_type].index is None:
                    column_map[column_type].index = index
                    column_map[column_type].column_name = item
                    found_msg = ("Found column named '{}' at index {}, " +
                                 "assuming this to be the {} column.")
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
            if index in [csvcolumn.index for csvcolumn in column_map.values()]:
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

    # Wrap up: Check if there any mandatory column types left which have not
    # yet been identified - we cannot continue in that case (unless forced).
    unassigned = [x for x in iter(column_map.items()) if x[1].requirement == CSVColumn.MANDATORY and x[1].index is None]
    if unassigned:
        for item in unassigned:
            print("The {} column is still unidentified.".format(item[0]))
        if header:
            print("The CSV header is:\n" + dialect.delimiter.join(header))
        if not args.force:
            print("ERROR: We cannot continue because not all mandatory " +
                  "column types in the CSV file could be automatically " +
                  "identified. There are 2 ways to fix this:")
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
            print("WARNING: Not all mandatory column types in the CSV file " +
                  "could be automatically identified - forced to continue.")

    print("\n    *** CSV file analysis summary ***\n")

    index_dict = {csvc.index: csvc for csvc in column_map.values()}

    for index in range(num_columns):
        column_name = ""
        if header:
            column_name = header[index]
        if index in index_dict:
            column = index_dict[index]
            msg = u"column number {} ({}) is the {} column '{}'".format(
                index, column_name, column.requirement, column.column_type)
            if column.requirement in [CSVColumn.MANDATORY, CSVColumn.OPTIONAL]:
                oat.print_g(msg)
            else:
                oat.print_b(msg)
        else:
            if args.add_unknown_columns:
                msg = (u"column number {} ({}) is an unknown column, it will be " +
                       "appended to the generated CSV file")
                oat.print_y(msg.format(index, column_name))
                if not column_name:
                    # Use a generic name
                    column_name = "unknown"
                while column_name in column_map.keys():
                    # TODO: Replace by a numerical, increasing suffix
                    column_name += "_"
                column_map[column_name] = CSVColumn(column_name, CSVColumn.NONE, index)
            else:
                msg = (u"column number {} ({}) is an unknown column, it will be " +
                       "ignored")
                oat.print_y(msg.format(index, column_name))

    print()
    for column in column_map.values():
        if column.index is None:
            msg = "The {} column '{}' could not be identified."
            print(msg.format(column.requirement, column.column_type))


    # Check for unassigned optional column types. We can continue but should
    # issue a warning as all entries will need a valid DOI in this case.
    unassigned = filter(lambda k, v: v.requirement == CSVColumn.OPTIONAL and v.index is None,
                        column_map.items())
    if unassigned:
        print ("\nWARNING: Not all optional column types could be " +
               "identified. Metadata aggregation is still possible, but " +
               "every entry in the CSV file will need a valid DOI.")

    start = input("\nStart metadata aggregation? (y/n):")
    while start not in ["y", "n"]:
        start = input("Please type 'y' or 'n':")
    if start == "n":
        sys.exit()

    print("\n    *** Starting metadata aggregation ***\n")

    enriched_content = []

    csv_file.seek(0)
    reader = csv.reader(csv_file, dialect=dialect)
    header_processed = False
    row_num = 0

    for row in reader:
        row_num += 1
        if not row:
            continue # skip empty lines
        if not header_processed:
            header_processed = True
            enriched_content.append(list(column_map.keys()))
            if has_header:
                # If the CSV file has a header, we are currently there - skip it
                # to get to the first data row
                continue
        if args.start and args.start > row_num:
            continue
        if args.end and args.end < row_num:
            continue
        print("---Processing line number " + str(row_num) + "---")
        enriched_row = oat.process_row(row, row_num, column_map, num_columns,
                                       args.no_crossref, args.no_pubmed,
                                       args.no_doaj, doaj_offline_analysis, args.round_monetary)
        enriched_content.append(enriched_row)

    csv_file.close()

    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, 
                                          not args.no_openapc_quote_rules, True,
                                          True)
        writer.write_rows(enriched_content)

    if not bufferedHandler.buffer:
        oat.print_g("Metadata enrichment successful, no errors occured")
    else:
        oat.print_r("There were errors during the enrichment process:\n")
    # closing will implicitly flush the handler and print any buffered
    # messages to stderr
    bufferedHandler.close()

if __name__ == '__main__':
    main()
