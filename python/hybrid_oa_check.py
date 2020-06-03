#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import logging
import re
from socket import error as socket_error
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import unquote
from urllib.request import build_opener, Request, HTTPCookieProcessor

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
                           has different designations in the input file.
        nonstandard_redirects: An optional list of NonstandardRedirect objects.
    """
    def __init__(self, publisher_name, landingpage_domain, regex_groups, 
                 publisher_aliases=None, nonstandard_redirects=None):
        self.publisher_name = publisher_name
        self.landingpage_domain = landingpage_domain
        self.regex_groups = regex_groups
        if publisher_aliases is None:
            self.publisher_aliases = []
        else:
            self.publisher_aliases = publisher_aliases
        if nonstandard_redirects is None:
            self.nonstandard_redirects = []
        else:
            self.nonstandard_redirects = nonstandard_redirects

    def publisher_matches(self, publisher):
        return publisher == self.publisher_name or publisher in self.publisher_aliases

    def search_for_oa(self, page_content):
        for group in self.regex_groups:
            link = group.search(page_content)
            if link is None:
                continue
            return link
        return None
    
    def get_next_redirect(self, response):
        url = response.geturl()
        for nsd in self.nonstandard_redirects:
            if nsd.redirect_domain in url:
                content = response.read().decode("utf-8")
                return nsd.extract_target(content)
        return None
        
class NonstandardRedirect(object):
    """
    Handles non-HTTP redirects.
    
    Some DOI resolve paths involve redirects which are
    dependent on web browsers, like java script code or usage of a 
    http-equiv="refresh" meta tag with additional url content (as seen on
    linkinghub.elsevier.com). This class is meant to handle those cases.
    
    Attributes:
        redirect_domain: Domain of the redirection service. URLs are matched
                         against this pattern to determine if this
                         NonstandardRedirect should be applied.
        regex_group: A RegexGroup to extract the next redirection target from
                     the page content.
    """
    
    def __init__(self, redirect_domain, regex_group):
        self.redirect_domain = redirect_domain
        self.regex_group = regex_group
        
    def extract_target(self, content):
        link = self.regex_group.search(content)
        if link is not None:
            return unquote(link)
        return None
    
        

class RegexGroup(object):
    """
    A container class for grouping regular expressions objects.

    Instances of this class are created with an arbitrary number of
    pre-compiled regular expressions objects. Its purpose is to bundle
    a set of expressions which must all match to confirm the validity
    of a landing page. Exactly one of the regexes should
    contain a group which matches a link target.
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
    RegexGroup(re.compile('<meta\s+name="citation_pdf_url"\s+content="(.*?)"\s*/>'),
               re.compile('<div class="OpenAccessLabel">open access</div>'))
]

elsevier_nsd = NonstandardRedirect("linkinghub.elsevier.com", RegexGroup(re.compile('<input\s+type="hidden"\s+name="redirectURL"\s+value="(.*?)"')))

springer_regex_groups = [
    RegexGroup(re.compile('<a href="(.*?)".*?title="Download this article in PDF format"'),
               re.compile('<span.*?class="open-access'))
]

wiley_regex_groups = [
    RegexGroup(re.compile('<meta\s+name="citation_pdf_url"\s+content="(.*?)"')),
    RegexGroup(re.compile('<div\s+class="doi-access.*?>Open Access</div>'))
]

elsevier = LandingPageLookup("Elsevier BV", "sciencedirect.com", elsevier_regex_groups, nonstandard_redirects=[elsevier_nsd])
springer = LandingPageLookup("Springer Nature", "link.springer.com", springer_regex_groups, publisher_aliases=["Springer Science + Business Media"])
wiley = LandingPageLookup("Wiley-Blackwell", "onlinelibrary.wiley.com", wiley_regex_groups)

lpl_list = [elsevier, springer, wiley]

def get_landingpage_content(doi, lpl):
    url = 'https://doi.org/' + doi
    # Some publisher LPs require us to put on our magic hood
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0"}
    req = Request(url, headers=headers)
    opener = build_opener(HTTPCookieProcessor())
    try:
        response = opener.open(req)
        target = response.geturl()
        resolve_msg = "DOI {} resolved, led us to {}".format(doi, target)
        oat.print_y(resolve_msg)
        while lpl.landingpage_domain not in target:
            target = lpl.get_next_redirect(response)
            if target is None:
                msg = "Journal not located at {}, skipping..."
                oat.print_r(msg.format(lpl.landingpage_domain))
                return None
            req = Request(target, headers=headers)
            response = opener.open(req)
            target = response.geturl()
            redir_msg = "Non-standard redirect found, led us to {}"
            oat.print_y(redir_msg.format(target))
        content_string = response.read().decode("utf-8")
        return content_string
    except HTTPError as httpe:
        code = str(httpe.getcode())
        oat.print_r("HTTPError: {} - {}".format(code, httpe.reason))
        return None
    except URLError as urle:
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
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            oat.print_g(msg.format(args.encoding, codec.name))
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
        oat.print_g("\nLookup finished, all articles were accessible")
    else:
        oat.print_r("\nLookup finished, not all articles could be accessed:\n")
    # closing will implicitly flush the handler and print any buffered
    # messages to stderr
    bufferedHandler.close()

if __name__ == '__main__':
    main()
