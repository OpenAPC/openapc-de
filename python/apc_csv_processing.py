#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
from collections import OrderedDict
from copy import copy
import csv
import datetime
import locale
import sys

import openapc_toolkit as oat

class CSVColumn(object):

    def __init__(self, column_type, mandatory, index=None, column_name=""):
        self.column_type = column_type
        self.mandatory = mandatory
        self.index = index
        self.column_name = column_name


ARG_HELP_STRINGS = {
    "csv_file": "CSV file containing your APC data. It must contain at least " +
                "the 4 mandatory columns defined by the OpenAPC data schema: " +
                "institution, doi, period and euro (in no particular order).",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "locale": "Set the locale context used by the script. You might want to " +
              "set this if your system locale differs from the locale the " +
              "CSV file was created in (Example: Using en_US as your system " +
              "locale might become a problem if the file contains numeric " +
              "values with ',' as decimal point character)",
    "headers": "Ignore any CSV headers (if present) and try to determine " +
               "relevant columns heuristically.",
    "force": "Force the script to continue even if not all mandatory columns " +
             "have been identified",
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
           "a DOI in the file."
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-i", "--ignore-header", action="store_true",
                        help=ARG_HELP_STRINGS["headers"])
    parser.add_argument("-f", "--force", action="store_true",
                        help=ARG_HELP_STRINGS["force"])
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

    args = parser.parse_args()
    enc = None # CSV file encoding

    if args.locale:
        norm = locale.normalize(args.locale)
        if norm != args.locale:
            print "locale '{}' not found, normalized to '{}'".format(
                args.locale, norm)
        try:
            loc = locale.setlocale(locale.LC_ALL, norm)
            print "Using locale", loc
        except locale.Error as loce:
            print "Setting locale to " + norm + " failed: " + loce.message
            sys.exit()

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
    dialect = csv_analysis.dialect
    has_header = csv_analysis.has_header

    if enc is None:
        print ("Error: No encoding given for CSV file and automated " +
               "detection failed. Please set the encoding manually via the " +
               "--enc argument")
        sys.exit()

    csv_file = open(args.csv_file, "r")
    reader = oat.UnicodeReader(csv_file, dialect=dialect, encoding=enc)

    first_row = reader.next()
    num_columns = len(first_row)
    print "\nCSV file has {} columns.".format(num_columns)

    csv_file.seek(0)
    reader = oat.UnicodeReader(csv_file, dialect=dialect, encoding=enc)

    column_map = {
        "institution": CSVColumn("institution", True, args.institution_column),
        "period": CSVColumn("period", True, args.period_column),
        "euro": CSVColumn("euro", True, args.euro_column),
        "doi": CSVColumn("doi", True, args.doi_column),
        "is_hybrid": CSVColumn("is_hybrid", True, args.is_hybrid_column),
        "publisher": CSVColumn("publisher", False, args.publisher_column),
        "journal_full_title": CSVColumn("journal_full_title", False,
                                        args.journal_full_title_column),
        "issn": CSVColumn("issn", False, args.issn_column),
        "url": CSVColumn("url", False, args.url_column)
    }

    # This list will store info about additional (unknown) columns found in
    # the CSV file as CSVColumn objects.
    additional_columns = []

    csv_columns = OrderedDict([
        ("institution", "NA"),
        ("period", "NA"),
        ("euro", "NA"),
        ("doi", "NA"),
        ("is_hybrid", "NA"),
        ("publisher", "NA"),
        ("journal_full_title", "NA"),
        ("issn", "NA"),
        ("issn_print", "NA"),
        ("issn_electronic", "NA"),
        ("license_ref", "NA"),
        ("indexed_in_crossref", "NA"),
        ("pmid", "NA"),
        ("pmcid", "NA"),
        ("ut", "NA"),
        ("url", "NA"),
        ("doaj", "NA")
    ])

    # Do not quote the values in the 'period' and 'euro' columns
    quotemask = [
        True,
        False,
        False,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    ]

    header = None
    if has_header:
        for row in reader:
            if not row: # Skip empty lines
                continue
            header = row # First non-empty row should be the header
            if args.ignore_header:
                print "Skipping header analysis due to command line argument."
                break
            else:
                print "\n    *** Analyzing CSV header ***\n"
            for (index, item) in enumerate(header):
                column_type = oat.get_column_type_from_whitelist(item)
                if column_type is not None and column_map[column_type].index is None:
                    column_map[column_type].index = index
                    column_map[column_type].column_name = item
                    print ("Found column named '{}' at index {}, " +
                           "assuming this to be the {} column.").format(
                               item, index, column_type)
            break


    print "\n    *** Starting heuristical analysis ***\n"
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
        for (index, entry) in enumerate(row):
            if index in [csvcolumn.index for csvcolumn in column_map.values()]:
                # Skip columns already assigned
                continue
            entry = entry.strip()
            # Search for a DOI
            if column_map['doi'].index is None:
                if oat.DOI_RE.match(entry):
                    column_id = str(index)
                    # identify column either numerical or by column header
                    if header:
                        column_id += " ('" + header[index] + "')"
                    print ("The entry in column {} looks like a " +
                           "DOI: {}").format(column_id, entry)
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
                        print ("The entry in column {} looks like a " +
                               "potential period: {}").format(column_id, entry)
                        column_candidates['period'].append(index)
                        continue
                except ValueError:
                    pass
            # Search for a potential monetary amount
            if column_map['euro'].index is None:
                try:
                    maybe_euro = locale.atof(entry)
                    # Are there APCs above 6000€ ??
                    if maybe_euro >= 10 and maybe_euro <= 6000:
                        column_id = str(index)
                        if header:
                            column_id += " ('" + header[index] + "')"
                        print ("The entry in column {} looks like a " +
                               "potential euro amount: {}").format(column_id,
                                                                   entry)
                        column_candidates['euro'].append(index)
                        continue
                except ValueError:
                    pass
        for column_type, candidates in column_candidates.iteritems():
            if column_map[column_type].index is not None:
                continue
            if len(candidates) > 1:
                print ("Could not reliably identify the '" + column_type +
                       "' column - more than one possible candiate!")
            elif len(candidates) < 1:
                print "No candidate found for column '" + column_type + "'!"
            else:
                index = candidates.pop()
                column_map[column_type].index = index
                if header:
                    column_id = header[index]
                    column_map[column_type].column_name = column_id
                else:
                    column_id = index
                print ("Assuming column '{}' to be the '{}' " +
                       "column.").format(column_id, column_type)
                column_map[column_type].index = index
        break

    # Wrap up: Check if there any mandatory column types left which have not
    # yet been identified - we cannot continue in that case (unless forced).
    unassigned = filter(lambda (k, v): v.mandatory and v.index is None,
                        column_map.iteritems())
    if unassigned:
        for item in unassigned:
            print "The {} column is still unidentified.".format(item[0])
        if header:
            print "The CSV header is:\n" + dialect.delimiter.join(header)
        if not args.force:
            print ("ERROR: We cannot continue because not all mandatory " +
                   "column types in the CSV file could be automatically " +
                   "identified. There are 2 ways to fix this:")
            if not header:
                print ("1) Add a header row to your file and identify the " +
                       "column(s) by assigning them an appropiate column name.")
            else:
                print ("1) Identify the missing column(s) by assigning them " +
                       "a different column name in the CSV header (You can " +
                       "use the column name(s) mentioned in the message above)")
            print ("2) Use command line parameters when calling this script " +
                   "to identify the missing columns (use -h for help) ")
            sys.exit()
        else:
            print ("WARNING: Not all mandatory column types in the CSV file " +
                   "could be automatically identified - forced to continue.")

    print "\n    *** CSV file analysis summary ***\n"

    index_dict = {csvc.index: csvc for csvc in column_map.values()}

    for index in range(num_columns):
        column_name = ""
        if header:
            column_name = header[index]
        if index in index_dict:
            column = index_dict[index]
            mandatory = "mandatory" if column.mandatory else "optional"
            msg = "column number {} ({}) is the {} column '{}'"
            print msg.format(index, column_name, mandatory, column.column_type)
        else:
            msg = ("column number {} ({}) is an unknown column, it will be " +
                   "appended to the generated CSV file")
            print msg.format(index, column_name)
            if not column_name:
                # Use a generic name
                column_name = "unknown"
            while column_name in csv_columns:
                # TODO: Replace by a numerical, increasing suffix
                column_name += "_"
            csv_columns[column_name] = "NA"
            additional_columns.append(CSVColumn(column_name, False, index))


    print ""
    for column in column_map.values():
        if column.index is None:
            # Should all be optional...
            mandatory = "mandatory" if column.mandatory else "optional"
            msg = "The {} column '{}' could not be identified."
            print msg.format(mandatory, column.column_type)


    # Check for unassigned optional column types. We can continue but should
    # issue a warning as all entries will need a valid DOI in this case.
    unassigned = filter(lambda (k, v): not v.mandatory and v.index is None,
                        column_map.iteritems())
    if unassigned:
        print ("\nWARNING: Not all optional column types could be " +
               "identified. Metadata aggregation is still possible, but " +
               "every entry in the CSV file will need a valid DOI.")

    start = raw_input("\nStart metadata aggregation? (y/n):")
    while start not in ["y", "n"]:
        start = raw_input("Please type 'y' or 'n':")
    if start == "n":
        sys.exit()



    print "\n    *** Starting metadata aggregation ***\n"

    enriched_content = []

    csv_file.seek(0)
    reader = oat.UnicodeReader(csv_file, dialect=dialect, encoding=enc)
    header_processed = False

    for row in reader:
        if not row:
            continue # skip empty lines
        if not header_processed:
            header_processed = True
            enriched_content.append(csv_columns.keys())
            if has_header:
                # If the CSV file has a header, we are currently there - skip it
                # to get to the first data row
                continue

        doi = row[column_map["doi"].index]

        current_row = copy(csv_columns)

        # Copy content of identified columns
        for csv_column in column_map.values():
            if csv_column.index is not None:
                if csv_column.column_type == "euro":
                    # special case for monetary values: Cast to float to ensure
                    # the decimal point is a dot (instead of a comma)
                    euro = locale.atof(row[csv_column.index])
                    if euro.is_integer():
                        euro = int(euro)
                    current_row[csv_column.column_type] = str(euro)
                else:
                    current_row[csv_column.column_type] = row[csv_column.index]
                    

        # add unidentified fields to the row
        for column in additional_columns:
            field = row[column.index]
            current_row[column.column_type] = field

        # include crossref metadata
        crossref_result = oat.get_metadata_from_crossref(doi)
        if crossref_result["success"]:
            print "Crossref: DOI resolved: " + doi
            current_row["indexed_in_crossref"] = "TRUE"
            data = crossref_result["data"]
            for key, value in data.iteritems():
                if value is not None:
                    current_row[key] = value
                else:
                    current_row[key] = "NA"
                    print (u"WARNING: Element '{}' not found in in response " +
                           "for doi {}.").format(key, doi)
        else:
            print ("Crossref: Error while trying to resolve DOI " + doi + ": " +
                   crossref_result["error_msg"])
            current_row["indexed_in_crossref"] = "FALSE"

        # include pubmed metadata
        pubmed_result = oat.get_metadata_from_pubmed(doi)
        if pubmed_result["success"]:
            print "Pubmed: DOI resolved: " + doi
            data = pubmed_result["data"]
            for key, value in data.iteritems():
                if value is not None:
                    current_row[key] = value
                else:
                    current_row[key] = "NA"
                    print (u"WARNING: Element '{}' not found in in response " +
                           "for doi {}.").format(key, doi)
        else:
            print ("Pubmed: Error while trying to resolve DOI " + doi + ": " +
                   pubmed_result["error_msg"])

        # lookup in DOAJ. try the EISSN first, then ISSN and finally print ISSN
        if current_row["doaj"] != "TRUE":
            issns = []
            if current_row["issn_electronic"] != "NA":
                issns.append(current_row["issn_electronic"])
            if current_row["issn"] != "NA":
                issns.append(current_row["issn"])
            if current_row["issn_print"] != "NA":
                issns.append(current_row["issn_print"])
            for issn in issns:
                doaj_res = oat.lookup_journal_in_doaj(issn)
                if doaj_res["data_received"]:
                    if doaj_res["data"]["in_doaj"]:
                        msg = "DOAJ: Journal ISSN ({}) found in DOAJ ('{}')."
                        print msg.format(issn, doaj_res["data"]["title"])
                        current_row["doaj"] = "TRUE"
                        break
                    else:
                        msg = "DOAJ: Journal ISSN ({}) not found in DOAJ."
                        current_row["doaj"] = "FALSE"
                        print msg.format(issn)
                else:
                    msg = "DOAJ: Error while trying to look up ISSN {}: {}"
                    print msg.format(issn, doaj_res["error_msg"])


        enriched_content.append(current_row.values())

    csv_file.close()

    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, quotemask, True, True)
        writer.write_rows(enriched_content)


if __name__ == '__main__':
    main()
