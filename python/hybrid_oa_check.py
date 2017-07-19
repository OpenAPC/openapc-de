#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
import logging
import re
from socket import error as socket_error
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

class LandingPageLookup(object):
    """
    Encapsulates information on how to perform a landing page lookup for a
    given publisher.

    Attributes:
        publisher_name: The publisher name as it occurs in the "publisher"
                        column of the given OpenAPC file
        landingpage_domain: The domain where the publisher's landing
                            pages reside (like "sciencedirect.com").
                            A simple match against this value is performed
                            for all DOI targets, so it should not be too specific.
        regex_groups: A list of RegexGroup objects. At least one of these groups
                      must produce a match for all of its expressions to
                      confirm OA status.
        publisher_aliases: An optional list of aliases, if the same publisher
                           has different designations in the input file
    """
    def __init__(self, publisher_name, landingpage_domain, regex_groups, publisher_aliases=None):
        self.publisher_name = publisher_name
        self.landingpage_domain = landingpage_domain
        self.regex_groups = regex_groups
        if publisher_aliases is None:
            self.publisher_aliases = []
        else:
            self.publisher_aliases = publisher_aliases

    def publisher_matches(self, publisher):
        return publisher == self.publisher_name or publisher in self.publisher_aliases

    def search_for_oa(self, page_content):
        for group in self.regex_groups:
            link = group.search(page_content)
            if link is None:
                continue
            return link
        return None

class RegexGroup(object):
    """
    A simple container class for grouping regular expressions objects.

    Instances of this class are created with an arbitrary number of
    pre-compiled regular expressions objects. Its purpose is to bundle
    a set of expressions which must all match to confirm the OA status
    of a landing page. Exactly one of the regexes should
    contain a group which matches the link target of the article PDF.
    """
    def __init__(self, *args):
        self.regexes = []
        for regex in args:
            self.regexes.append(regex)

    def search(self, text):
        link = ""
        for regex in self.regexes:
            match = regex.search(text)
            if not match:
                return None
            groups = match.groups()
            if len(groups) > 0:
                link = groups[0]
        return link


elsevier_regex_groups = [
    # landing pages with a single pdf file
    RegexGroup(re.compile('<a id="pdfLink".*?pdfurl="(.*?)"')),
    # pages with more than one pdf. Note that this snippet is located
    # in a commented section (it is transformed via js dynamically), so the href
    # link might not be initially valid (ampersand escaping etc)
    RegexGroup(re.compile('<a class="download-pdf-link".*?href="(.*?)"'))
]

springer_regex_groups = [
    RegexGroup(re.compile('<a href="(.*?)".*?title="Download this article in PDF format"'),
               re.compile('<span.*?class="open-access"'))
]

wiley_regex_groups = [
    RegexGroup(re.compile('<li class="box-actions"><a href="(.*?)" class="js-article-section__pdf-container-link article-section__pdf-container-link"')),
    RegexGroup(re.compile('<span class="article-type article-type--open-access">.*?Open Access.*?</span>'))
]

elsevier = LandingPageLookup("Elsevier BV", "sciencedirect.com", elsevier_regex_groups)
springer = LandingPageLookup("Springer Nature", "link.springer.com", springer_regex_groups, ["Springer Science + Business Media"])
wiley = LandingPageLookup("Wiley-Blackwell", "onlinelibrary.wiley.com", wiley_regex_groups)

lpl_list = [elsevier, springer, wiley]

def get_landingpage_content(doi, lpl):
    url = 'http://doi.org/' + doi
    header = {"User-Agent": "Mozilla/5.0 Firefox/45.0"}
    req = urllib2.Request(url, None, header)
    try:
        response = urllib2.urlopen(req)
        target = response.geturl()
        resolve_msg = u"DOI {} resolved, led us to {}".format(doi, target)
        if lpl.landingpage_domain not in target:
            oat.print_y(resolve_msg)
            landingpage_msg = (u"Journal not located at {}, " +
                               "skipping...").format(lpl.landingpage_domain)
            oat.print_y(landingpage_msg)
            return None
        oat.print_b(resolve_msg)
        content_string = response.read()
        return content_string
    except urllib2.HTTPError as httpe:
        code = str(httpe.getcode())
        oat.print_r("HTTPError: {} - {}".format(code, httpe.reason))
        return None
    except urllib2.URLError as urle:
        oat.print_r("URLError: {}".format(urle.reason))
        return None
    except socket_error as se:
        oat.print_r("Socket Error: {}".format(se.message))
        return None

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

    line_num = 0
    for line in content:
        line_num += 1
        if args.start and args.start > line_num:
            continue
        if args.end and args.end < line_num:
            continue
        # Check hybrid status
        if line[4] != "TRUE":
            continue
        institution = line[0]
        period = line[1]
        doi = line[3]
        publisher = line[5]
        journal = line[6]
        for lpl in lpl_list:
            if lpl.publisher_matches(publisher):
                init_msg = (u"Line {}: Checking {} article from {}, published in '" +
                            "{}'...").format(line_num, institution, period, journal)
                oat.print_b(init_msg)
                page_content = get_landingpage_content(doi, lpl)
                if page_content is None:
                    continue
                pdf_link = lpl.search_for_oa(page_content)
                if pdf_link is None:
                    error_msg = (u"No PDF link found! (line {}, DOI: " +
                                 "http://doi.org/{}").format(line_num, doi)
                    logging.error(error_msg)
                elif pdf_link == "":
                    warning_msg = (u"A RegexGroup matched, but no PDF " +
                                   "link was found! (line {}, DOI: " +
                                   "http://doi.org/{}").format(line_num, doi)
                    logging.warning(warning_msg)
                else:
                    oat.print_g(u"PDF link found: " + pdf_link)
        time.sleep(1)

    if not bufferedHandler.buffer:
        oat.print_g("\nLookup finished, all articles were accessible on sciencedirect")
    else:
        oat.print_r("\nLookup finished, not all articles could be accessed on sciencedirect:\n")
    # closing will implicitly flush the handler and print any buffered
    # messages to stderr
    bufferedHandler.close()

if __name__ == '__main__':
    main()
