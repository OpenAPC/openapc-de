#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
import logging
import re
import sys
import time
import urllib2

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "csv_file": "An OpenAPC-conforming CSV file where oa status for elsevier " +
                "articles should be checked",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "start": "Do not process the whole file, but start from this line " +
             "number. May be used together with '-end' to select a specific " +
             "segment.",
    "end": "Do not process the whole file, but end at this line number. May " +
           "be used together with '-start' to select a specific segment."
}

# regex for landing pages with a single pdf file
pdflink_re = re.compile('<a id="pdfLink".*?pdfurl="(.*?)"')

# regex for pages with more than one pdf. Note that this snippet is located
# in a commented section (it is transformed via js dynamically), so the href
# link might not be initially valid (ampersand escaping etc)
pdflink_multi_re = re.compile('<a class="download-pdf-link".*?href="(.*?)"')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help=ARG_HELP_STRINGS["csv_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-start", type=int, default=1, help=ARG_HELP_STRINGS["start"])
    parser.add_argument("-end", type=int, help=ARG_HELP_STRINGS["start"])
    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(oat.ANSIColorFormatter())
    bufferedHandler = oat.BufferedErrorHandler(handler)
    bufferedHandler.setFormatter(oat.ANSIColorFormatter())
    logging.root.addHandler(handler)
    logging.root.addHandler(bufferedHandler)
    logging.root.setLevel(logging.INFO)

    enc = None
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

    head, content = oat.get_csv_file_content(args.csv_file, enc)
    content = head + content

    header = {"User-Agent": "Mozilla/5.0 Firefox/45.0"}

    line_num = 0
    for line in content:
        line_num += 1
        if args.start and args.start > line_num:
            continue
        if args.end and args.end < line_num:
            continue
        institution = line[0]
        period = line[1]
        doi = line[3]
        is_hybrid = line[4]
        publisher = line[5]
        journal = line[6]
        if publisher != "Elsevier BV" or is_hybrid != "TRUE":
            continue
        init_msg = (u"Line {}: Checking {} article from {}, published in " +
                    "{}...").format(line_num, institution, period, journal)
        oat.print_b(init_msg)
        url = 'http://doi.org/' + doi
        req = urllib2.Request(url, None, header)
        ret_value = {'success': True}
        try:
            response = urllib2.urlopen(req)
            target = response.geturl()
            resolve_msg = u"DOI {} resolved, led us to {}".format(doi, target)
            if "sciencedirect.com" not in target:
                oat.print_y(resolve_msg)
                oat.print_y("Journal not located at sciencedirect, skipping...")
                continue
            oat.print_b(resolve_msg)
            content_string = response.read()
            single_match = pdflink_re.search(content_string)
            if single_match:
                link_url = single_match.groups()[0]
                oat.print_g(u"PDF link found: " + link_url)
            else:
                multi_match = pdflink_multi_re.search(content_string)
                if multi_match:
                   link_url = multi_match.groups()[0]
                   link_url = link_url.replace("&amp;", "&")
                   oat.print_g(u"PDF link found (more than one document): " + link_url)
                else:
                    error_msg = (u"No PDF link found! (line {}, DOI: {}, " +
                                 "landing page: {})").format(line_num, doi, target)
                    logging.error(error_msg)
            time.sleep(1)
        except urllib2.HTTPError as httpe:
            code = str(httpe.getcode())
            oat.print_r("HTTPError: {} - {}".format(code, httpe.reason))
        except urllib2.URLError as urle:
            oat.print_r("URLError: {}".format(urle.reason))

    if not bufferedHandler.buffer:
        oat.print_g("\nLookup finished, all articles were accessible on sciencedirect")
    else:
        oat.print_r("\nLookup finished, not all articles could be accessed on sciencedirect:\n")
    # closing will implicitly flush the handler and print any buffered
    # messages to stderr
    bufferedHandler.close()

if __name__ == '__main__':
    main()
