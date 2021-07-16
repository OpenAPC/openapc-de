#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import json
from math import inf
import random
import sys
from time import sleep
from urllib.error import HTTPError
from urllib.parse import quote_plus, urlencode
from urllib.request import urlopen, Request

from Levenshtein import ratio, matching_blocks, editops

import openapc_toolkit as oat

MATCH_DEFAULT = 0.9
ASK_DEFAULT = 0.8
COLORS_DEFAULT = True

TITLE_HEADER_WL = ["article title", "title"]

ARG_HELP_STRINGS = {
    "input_file": "CSV input file, which should have a column containing book/journal article titles.",
    "title_index": "Numerical index of the column containing titles, with the leftmost column being 0.",
    "doi_index": "Numerical index of an existing DOI column, with the leftmost column being 0. If given, obtained DOIs will be integrated into this column (user will be prompted before overwrite). If left out, all obtained DOIs will be written to a new column 'crossref_doi' which is added to the resulting CSV file",
    "overwrite": "If doi_index is given, overwrite existing DOIs without asking for confirmation.",
    "encoding": "The encoding of the CSV file. Setting this argument will disable automatic guessing of encoding.",
    "match_threshold": "a float value determining the minimum Levenshtein ratio to accept a title match (default: " + str(MATCH_DEFAULT) + ")",
    "ask_threshold": "a float value determining the minimum Levenshtein ratio to accept a title match (default: " + str(ASK_DEFAULT) + ")",
    "ansi_colors": "Use colorised text for easier visual match recognition (default: " + str(COLORS_DEFAULT) + ")",
    "start": "Start from this line number",
    "end": "End at this line number"
}

L_JUST = 40
BREAK = "".join(["-" for i in range(80)])
CMP_COLORS = ["blue", "green", "yellow", "red"]
EMPTY_RESULT = {
    "crossref_title": "",
    "similarity": 0,
    "doi": ""
}
MAX_RETRIES_ON_ERROR = 3

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help=ARG_HELP_STRINGS["input_file"])
    parser.add_argument("title_index", type=int, help=ARG_HELP_STRINGS["title_index"])
    parser.add_argument("-d", "--doi_index", type=int, help=ARG_HELP_STRINGS["doi_index"])
    parser.add_argument("-o", "--overwrite", action="store_true", help=ARG_HELP_STRINGS["overwrite"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-m", "--match_threshold", type=float, default=0.9, help=ARG_HELP_STRINGS["match_threshold"])
    parser.add_argument("-a", "--ask_threshold", type=float, default=0.8, help=ARG_HELP_STRINGS["ask_threshold"])
    parser.add_argument("-c", "--colors", type=bool, default=COLORS_DEFAULT, help=ARG_HELP_STRINGS["ansi_colors"])
    parser.add_argument("--start", type=int, default=0, help=ARG_HELP_STRINGS["start"])
    parser.add_argument("--end", type=int, default=inf, help=ARG_HELP_STRINGS["end"])
    args = parser.parse_args()
    
    enc = None
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            print (msg.format(args.encoding, codec.name))
            enc = args.encoding
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/3.7/library/codecs.html" +
                   "#standard-encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()

    header, content = oat.get_csv_file_content(args.input_file, enc)
    header = header.pop()
    index_error_msg = "Error: Invalid {} column index {} (CSV header consists of {} elements, must be between 0 and {})."
    if args.title_index < 0 or args.title_index >= len(header):
        oat.print_r(index_error_msg.format("title", args.title_index, len(header), len(header) - 1))
        sys.exit()
    oat.print_g("Using column '" + header[args.title_index] + "' as title column")
    if args.doi_index:
        if args.doi_index < 0 or args.doi_index >= len(header):
            oat.print_r(index_error_msg.format("DOI", args.doi_index, len(header), len(header) - 1))
            sys.exit()
        doi_index = args.doi_index
        oat.print_g("Using column '" + header[doi_index] + "' as target DOI column")
    else:
        header += ["crossref_doi"]
        doi_index = len(header) - 1
        for line in content:
            line += ["NA"]
        if args.overwrite:
            oat.print_y("Warning: Overwrite parameter has no effect if used without doi_index (-d)")

    ask_for_similarity_lines = {}
    ask_for_overwrite_lines = {}
    for line_num, line in enumerate(content):
        if line_num < args.start or line_num > args.end:
            continue
        print(BREAK)
        title = line[args.title_index]
        head = "line " + str(line_num) + ", query title:"
        oat.print_b(head.ljust(L_JUST) + "'" + title + "'")
        ret = crossref_query_title(title)
        retries = 0
        while not ret['success'] and retries < MAX_RETRIES_ON_ERROR:
            retries += 1
            msg = "Error while querying CrossRef API ({}), retrying ({})..."
            oat.print_r(msg.format(ret["exception"], retries))
            ret = crossref_query_title(title)
        result = ret["result"]
        msg_tail = "'{}' [{}]"
        msg_tail = msg_tail.format(result["crossref_title"], result["doi"])
        if result["similarity"] == 1.0:
            msg_head = "Perfect match found ({}):"
            msg_head = msg_head.format(round(result["similarity"], 2)).ljust(L_JUST)
            oat.print_c(msg_head + msg_tail)
            if not integrate_doi(line, doi_index, result["doi"], args.overwrite):
                ask_for_overwrite_lines[line_num] = result
        elif result["similarity"] >= args.match_threshold:
            msg_head = "Good match found ({}):"
            msg_head = msg_head.format(round(result["similarity"], 2)).ljust(L_JUST)
            oat.print_g(msg_head + msg_tail)
            if not integrate_doi(line, doi_index, result["doi"], args.overwrite):
                ask_for_overwrite_lines[line_num] = result
        elif result["similarity"] >= args.ask_threshold:
            msg_head = "Possible match found ({}):"
            msg_head = msg_head.format(round(result["similarity"], 2)).ljust(L_JUST)
            oat.print_y(msg_head + msg_tail)
            ask_for_similarity_lines[line_num] = result
        else:
            msg_head = "No match found, most similar was ({}):"
            msg_head = msg_head.format(round(result["similarity"], 2)).ljust(L_JUST)
            oat.print_r(msg_head + msg_tail)
    if len(ask_for_similarity_lines) > 0:
        print(BREAK)
        ask_msg = "{} matches found with a similarity between {} and {} will need manual confirmation."
        oat.print_y(ask_msg.format(len(ask_for_similarity_lines), args.ask_threshold, args.match_threshold))
    for line_num, line in enumerate(content):
        if line_num in ask_for_similarity_lines:
            result = ask_for_similarity_lines[line_num]
            print(BREAK)
            query_t = line[args.title_index]
            xref_t = result["crossref_title"]
            # display matching segments in identical colors for easier recognition
            diff = matching_blocks(editops(query_t.lower(), xref_t.lower()), query_t, xref_t)
            query_print = query_t
            xref_print = xref_t
            # ANSI codes increase string length, so we need an offset to compensate
            offset = 0
            for i in range(len(diff)):
                a, b, c = diff[i]
                a += offset
                b += offset
                offset += 9
                color = CMP_COLORS[i % len(CMP_COLORS)]
                query_print = colorise_text_segment(query_print, a, a + c , color)
                xref_print = colorise_text_segment(xref_print, b, b + c , color)
            query_head = colorise("line {}, query title:".format(line_num), "blue")
            xref_head = colorise("Possible match ({}):".format(round(result["similarity"], 2)), "yellow")
            existing_doi = oat.get_normalised_DOI(line[args.doi_index])
            if existing_doi is None:
                query_hint = "[" + line[args.doi_index] + "]"
            else:
                query_hint = "[https://doi.org/" + existing_doi + "]"
            xref_hint = "[https://doi.org/" + result["doi"] + "]"
            print(query_head.ljust(L_JUST) + query_print + "   " + query_hint)
            print(xref_head.ljust(L_JUST) + xref_print + "   " + xref_hint)
            answer = input("Do you want to accept the DOI for the match title? (y/n):")
            while answer not in ["y", "n"]:
                answer = input("Please type 'y' or 'n':")
            if answer == "y":
                if not integrate_doi(line, doi_index, result["doi"], args.overwrite):
                    ask_for_overwrite_lines[line_num] = result
    if len(ask_for_overwrite_lines) > 0:
        print(BREAK)
        ask_msg = "{} new DOIs differ from existing values and will need manual confirmation."
        oat.print_y(ask_msg.format(len(ask_for_overwrite_lines)))
    for line_num, line in enumerate(content):
        if line_num in ask_for_overwrite_lines:
            new_doi = ask_for_overwrite_lines[line_num]["doi"]
            msg = 'Existing value in DOI column "{}" is to replaced by Crossref DOI "{}"'
            oat.print_y(msg.format(line[doi_index], new_doi))
            answer = input("Confirm Replacement? (y/n):")
            while answer not in ["y", "n"]:
                answer = input("Please type 'y' or 'n':")
            if answer == "y":
                line[doi_index] = new_doi
    with open("out.csv", "w") as out:
        csv_writer = csv.writer(out)
        csv_writer.writerow(header)
        csv_writer.writerows(content)

def integrate_doi(line, doi_index, new_doi, overwrite):
    old_doi = line[doi_index]
    if not oat.has_value(old_doi):
        line[doi_index] = new_doi
        msg = 'Replacing NA value with new DOI "{}"'
        oat.print_c(msg.format(new_doi))
        return True
    if oat.get_normalised_DOI(old_doi) == oat.get_normalised_DOI(new_doi):
        msg = 'Integration not necessary, new DOI is eqivalent to old one ("{}" <-> "{}")'
        oat.print_c(msg.format(new_doi, old_doi))
        return True
    if overwrite:
        line[doi_index] = new_doi
        msg = 'Overwriting existing value "{}" with new DOI "{}"'
        oat.print_c(msg.format(old_doi, new_doi))
        return True
    msg = 'Existing DOI differs from new value ("{}" <-> "{}")'
    oat.print_y(msg.format(old_doi, new_doi))
    return False

def crossref_query_title(title):
    api_url = "https://api.crossref.org/works?"
    params = {"rows": "10", "select": "DOI,title,type", "query.bibliographic": title}
    url = api_url + urlencode(params, quote_via=quote_plus)
    request = Request(url)
    request.add_header("User-Agent", "OpenAPC title preprocessor (https://github.com/OpenAPC/openapc-de/blob/master/python/title_preprocessing.py; mailto:openapc@uni-bielefeld.de)")
    try:
        ret = urlopen(request)
        content = ret.read()
        data = json.loads(content)
        items = data["message"]["items"]
        most_similar = EMPTY_RESULT
        for item in items:
            if "title" not in item:
                continue
            title = item["title"].pop()
            result = {
                "crossref_title": title,
                "similarity": ratio(title.lower(), params["query.bibliographic"].lower()),
                "doi": item["DOI"]
            }
            if most_similar["similarity"] < result["similarity"]:
                most_similar = result
        return {"success": True, "result": most_similar}
    except HTTPError as httpe:
        return {"success": False, "result": EMPTY_RESULT, "exception": httpe}
    time.sleep(1)
    
def colorise(text, color):
    return colorise_text_segment(text, 0, len(text), color)
    
def colorise_text_segment(text, start, end, color):
    ANSI_COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m"
    }
    if color not in ANSI_COLORS.keys():
        raise ValueError("Argument 'color' must be one of [" + ", ".join(ANSI_COLORS.keys()) + "]")
    s = ANSI_COLORS[color]
    e = "\033[0m"
    return text[:start] + s + text[start:end] + e + text[end:]
    
if __name__ == '__main__':
    main()
