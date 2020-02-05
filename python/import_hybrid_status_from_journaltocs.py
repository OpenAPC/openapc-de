#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import re
from time import sleep
import socket
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

import openapc_toolkit as oat

JTOC_METADATA_RES = {
    "jtoc_id": re.compile("journaltocID\:\s*(?P<jtoc_id>\d+)"),
    "jtoc_title": re.compile("\<dc\:title\>(?P<jtoc_title>.*?)\<\/dc\:title\>"),
    "jtoc_publisher": re.compile("Publisher\:\s*(?P<jtoc_publisher>.*?)\<br\>")
}

JOURNAL_TYPE_RES = {
    "HYBRID": (re.compile('title="Hybrid Journal. It can contain Open Access articles"'), "TRUE"),
    "OA": (re.compile('title="This is an Open Access Journal"'), "FALSE"),
    "SUBSCRIPTION": (re.compile('title="Subscription journal, but a few articles may be freely available"'), "TRUE"),
    "PARTIALLY_FREE": (re.compile('title="Partially Free or Hybrid journal."'), "TRUE"),
    "FREE": (re.compile('title="Free journal"'), "FALSE"),
    "ERROR": (re.compile("Article not found or there are no recent issues available for this journal"), "NA")
}

ARG_HELP_STRINGS = {
    "source_file": "The source file, in OpenAPC enriched format",
    "journaltocs_user": "User name at journaltocs.ac.uk",
    "integrate": ("Integrate results directly into the source file's is_hybrid column. " +
                  "Otherwise, generate a result file with a journal_full_title -> is_hybrid " +
                  "mapping."),
    "max_lookups": "maximum number of lookups"
}

QUOTE_MASK = [True, False, False, True, True, True, True, True, True, True, True, True, True, True,
              True, True, True, True, True]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("journaltocs_user", help=ARG_HELP_STRINGS["journaltocs_user"])
    parser.add_argument("-i", "--integrate", action="store_true", help=ARG_HELP_STRINGS["integrate"])
    parser.add_argument("-m", "--max_lookups", type=int, default=100, help=ARG_HELP_STRINGS["max_lookups"])
    args = parser.parse_args()

    analysed_journals = {}

    modified_content = []

    lookups = 0
    header, content = oat.get_csv_file_content(args.source_file, enc="utf-8", force_header=True)
    header_line = header[0]
    modified_content = [list(header_line)]
    for line in content:
        if not oat.has_value(line[6]): #journal_full_title
            modified_content.append(line)
            continue
        if not oat.has_value(line[4]): #is_hybrid
            title = line[6]
            oat.print_y('Looking up journal {}'.format(title))
            if title not in analysed_journals:
                if lookups < args.max_lookups:
                    hybrid_status = get_hybrid_status(line, args.journaltocs_user)
                    if hybrid_status is not None:
                        analysed_journals[title] = hybrid_status
                    else:
                        analysed_journals[title] = "NA"
                    lookups += 1
                    line[4] = analysed_journals[title]
                else:
                    oat.print_r("Maximum number of lookups reached!")
            else:
                line[4] = analysed_journals[title]
        modified_content.append(line)

    with open("out.csv", "w") as out:
        if args.integrate:
            writer = oat.OpenAPCUnicodeWriter(out, QUOTE_MASK, True, True)
            writer.write_rows(modified_content)
        else:
            out.write("journal_full_title,is_hybrid\n")
            for key, value in analysed_journals.items():
                out.write(key + "," + value + "\n")


def get_hybrid_status(line, username):
    for issn in [7, 8, 9, 10]:
        if not oat.has_value(line[issn]):
            continue
        msg = 'Looking up ISSN {}...'
        oat.print_y(msg.format(line[issn]))
        jtoc_metadata = get_jtoc_metadata(line[issn], username)
        sleep(1)
        if jtoc_metadata["jtoc_id"] is not None:
            msg = ('Entry found (publisher: {}, title: {}, jtoc_ID: {}, ' +
                   'obtaining hybrid status...)')
            oat.print_g(msg.format(jtoc_metadata["jtoc_publisher"], jtoc_metadata["jtoc_title"],
                                   jtoc_metadata["jtoc_id"]))
            journal_type = get_jtoc_journal_type(jtoc_metadata["jtoc_id"])
            if not journal_type:
                oat.print_r("Error while obtaining hybrid status!")
                continue
            sleep(1)
            msg = "journaltocs type is '{}' , mapped to is_hybrid = {}"
            oat.print_g(msg.format(journal_type[0], journal_type[1]))
            return journal_type[1]
    oat.print_r("None of the ISSN values found in journaltocs!")
    return None


def get_jtoc_metadata(issn, user, retries=0):
    api_url = "http://www.journaltocs.ac.uk/api/journals/"
    user_param = "?user=" + user

    url = api_url + issn + user_param
    req = Request(url)
    try:
        response = urlopen(req, timeout=5)
        content = response.read().decode("utf8")
        results = {}
        for key, regex in JTOC_METADATA_RES.items():
            match = regex.search(content)
            if match:
                results[key] = match.groupdict()[key]
            else:
                results[key] = None
        return results
    except socket.timeout:
        if retries <= 3:
            print("Socket timeout, retrying (" + str(retries) + ")")
            return get_jtoc_metadata(issn, retries + 1)
        return None
    except ConnectionResetError:
        if retries <= 3:
            print("ConnectionResetError, retrying (" + str(retries) + ")")
            return get_jtoc_metadata(issn, retries + 1)
        return None
    except HTTPError as httpe:
        print("HTTPError: {} - {}".format(httpe.code, httpe.reason))
        return None
    except URLError as urle:
        print("URLError: {}".format(urle.reason))
        return None

def get_jtoc_journal_type(jtoc_id, retries=0):
    api_url = "http://www.journaltocs.ac.uk/index.php?journalID="

    url = api_url + jtoc_id
    req = Request(url)
    try:
        response = urlopen(req, timeout=5)
        content = response.read().decode("utf8")
        for journal_type, tup in JOURNAL_TYPE_RES.items():
            match = tup[0].search(content)
            if match:
                return (journal_type, tup[1])
        raise Exception("Error: No RE matched for journal at " + url)
    except socket.timeout:
        if retries <= 3:
            print("Socket timeout, retrying (" + str(retries) + ")")
            return get_jtoc_journal_type(jtoc_id, retries + 1)
        return None
    except ConnectionResetError:
        if retries <= 3:
            print("ConnectionResetError, retrying (" + str(retries) + ")")
            return get_jtoc_journal_type(jtoc_id, retries + 1)
        return None
    except HTTPError as httpe:
        print("HTTPError: {} - {}".format(httpe.code, httpe.reason))
        return None
    except URLError as urle:
        print("URLError: {}".format(urle.reason))
        return None


if __name__ == '__main__':
    main()
