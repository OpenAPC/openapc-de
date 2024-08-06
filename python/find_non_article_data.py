#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import os
import re

from csv import writer, unix_dialect

from pathlib import Path

import openapc_toolkit as oat

WHITELIST_PATH = "find_non_article_data_directory_whitelist.txt"

CROSSREF_ARTICLE_TYPES = [
    "journal_article",
    "journal-article",
]

ARG_HELP_STRINGS = {
    "description": "This script is meant to discover non-article records in the OpenAPC data directory. It works as follows:\n\n" + 
                   " 1) Discover enriched files in all data directories (Some are blacklisted, see EXCEPTIONS). DEAL files are omitted.\n" +
                   " 2) Find corresponding non-enriched files\n" +
                   " 3) Compare the file pairs linewise: Search for empty lines in the enriched file and see if there's a DOI in the corresponding original line\n" +
                   " 4) Query the DOI in Crossref\n" +
                   " 5) If the DOI exists and has a non-article publication type (see below), write it to the results file (out.csv)\n\n" +
                   "Data directories which have been searched exhaustively without any findings are added to a whitelist (" + WHITELIST_PATH + ") to speed up consecutive runs.\n\n" +
                   "All publications which do NOT have one of the following Crossref types are considered non-article: \n" + ", ".join(CROSSREF_ARTICLE_TYPES)
}

ENRICHED_RE = re.compile(r"(?P<name>.*?)[_-]enriched\.csv", re.IGNORECASE)

DEAL_RE = re.compile(r".*?deal.*?\.csv", re.IGNORECASE)

UNSUPPORTED_ERROR = re.compile(r'Unsupported DOI type "(?P<doi_type>.*?)".*?')

# without subdirectories
EXCEPTIONS_DIRS = [
    "../data",
    "../data/couperin",
]

# includes subdirectories
EXCEPTIONS_SUBDIRS = [
    "../data/transformative_agreements",
    "../data/doaj",
    "../data/mpg",
    "../data/offsetting",
    "../data/journalsociology",
    "../data/template",
]



def _find_doi_in_line(line):
    for item in line:
        norm_doi = oat.get_normalised_DOI(item)
        if norm_doi is not None:
            return norm_doi
    return None
    
def _get_file_content(path):
    for encoding in ["utf-8", "latin-1"]:
        try:
            _, content = oat.get_csv_file_content(path, enc=encoding, force_header=True, print_results=False)
            return content
        except IOError:
            pass
    raise IOError("Could not open file " + path + " with any provided encoding!")

def discover_non_article_data(orig_file, enriched_file):
    try:
       orig_content =  _get_file_content(orig_file)
       enriched_content = _get_file_content(enriched_file)
    except IOError as ioe:
        raise ValueError(str(ioe))
    if len(orig_content) != len(enriched_content):
        msg = "orig file and enriched file differ in lines numbers! ('{}': {}, '{}': {})"
        msg = msg.format(orig_file, len(orig_content), enriched_file, len(enriched_content))
        raise ValueError(msg)
    results = []
    for i in range(len(enriched_content)):
        # check institution column
        line = enriched_content[i]
        if len(line) == 0 or line[0] in ["", "NA"]:
            orig_line = orig_content[i]
            doi = _find_doi_in_line(orig_line)
            if not doi:
                continue
            ret = oat.get_metadata_from_crossref(doi)
            if not ret["success"]:
                match = UNSUPPORTED_ERROR.match(ret["error_msg"])
                if match:
                    results.append((orig_file, doi, match["doi_type"]))
            elif ret["data"]["doi_type"] not in CROSSREF_ARTICLE_TYPES:
                results.append((orig_file, doi, ret["data"]["doi_type"]))
    return results

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=ARG_HELP_STRINGS["description"])
    args = parser.parse_args()
    # an auto-generated whitelist for directories which have:
    #   - all data files fully paired
    #   - no non-article types found in any orig file
    dir_whitelist = []
    all_results = []
    Path(WHITELIST_PATH).touch()
    with open(WHITELIST_PATH, "r") as f:
        for line in f:
            dir_whitelist.append(line[:-1])
        oat.print_c("Directory whitelist loaded, it contains " + str(len(dir_whitelist)) + " entries.")
    for tup in os.walk("../data"):
        path = tup[0]
        if path in dir_whitelist:
            oat.print_c("Directory '" + path + "' is whitelisted, skipping...")
            continue
        if path in EXCEPTIONS_DIRS:
            oat.print_c("Directory '" + path + "' is directly excluded, skipping...")
            continue
        excluded = False
        for exc in EXCEPTIONS_SUBDIRS:
            if Path(path).is_relative_to(Path(exc)):
                oat.print_c("Directory '" + path + "' is excluded (Rule: '" + exc + "'), skipping...")
                excluded = True
                break
        if excluded:
            continue
        files_left = list(tup[2])
        oat.print_b("Walking directory " + path)
        pairs_found = 0
        results_in_dir = []
        for filename in tup[2]:
            # exclude READMEs and DEAL files
            if filename in files_left and filename.lower() in ["readme.md", "readme.txt"]:
                files_left.remove(filename)
                oat.print_c(filename + " seems to be a README file, skipping...")
                continue
            if filename in files_left and DEAL_RE.match(filename):
                oat.print_c(filename + " seems to be a DEAL file, skipping...")
                files_left.remove(filename)
                continue
            match = ENRICHED_RE.match(filename)
            if match:
                # check preprocessed files first
                orig_filenames = [match["name"] + "_preprocessed.csv", match["name"] + ".csv"]
                match_found = False
                for orig_filename in orig_filenames:
                    if orig_filename in files_left:
                        orig_path = os.path.join(path, orig_filename)
                        if match_found:
                            # if a preprocessed version already matched, also delete the original file
                            files_left.remove(orig_filename)
                            continue
                        enriched_path = os.path.join(path, filename)
                        try:
                            msg = "Working on file pair '{}' <-> '{}' ..."
                            oat.print_b(msg.format(orig_path, enriched_path))
                            results = discover_non_article_data(orig_path, enriched_path)
                            results_in_dir += results
                            for r in results:
                                oat.print_g(", ".join(r))
                            files_left.remove(orig_filename)
                            files_left.remove(filename)
                            match_found = True
                        except ValueError as ve:
                            print(ve)
                        pairs_found += 1
                if not match_found:    
                    oat.print_r("ERROR: Could not find a corresponding original for enriched file '" + filename + "'")
                    oat.print_r("Candidates were: " + ", ".join(tup[2]))
        if pairs_found:
            oat.print_b(str(pairs_found) + " orig-enriched pair(s) found.")
        else:
            oat.print_r("No orig-enriched pair(s) found!")
        if files_left:
            oat.print_y("WARNING: Could not match all files in " + path + ", still remaining: " + ", ".join(files_left))
        # If all files have been paired and searched without results, we can add this dir to the wl
        # and ignore it in the future
        if not files_left and len(results_in_dir) == 0:
            with open(WHITELIST_PATH, "a") as f:
                f.write(path + "\n")
            oat.print_y("Directory '" + path + "' has been fully searched without results, adding it to the whitelist file.")
        all_results += results_in_dir

    with open("out.csv", "w") as out:
        csv_writer = writer(out, dialect=unix_dialect)
        csv_writer.writerow(["file", "doi", "type"])
        csv_writer.writerows(all_results)
            

if __name__ == '__main__':
    main()
