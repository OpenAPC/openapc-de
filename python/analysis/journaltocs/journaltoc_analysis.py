#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from csv import DictReader, DictWriter
from os import path
import re
from time import sleep
import socket
import sys
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

JTOC_METADATA_RES = {
    "jtoc_id": re.compile("journaltocID\:\s*(?P<jtoc_id>\d+)"),
    "jtoc_title": re.compile("\<dc\:title\>(?P<jtoc_title>.*?)\<\/dc\:title\>"),
    "jtoc_publisher": re.compile("Publisher\:\s*(?P<jtoc_publisher>.*?)\<br\>")
}

JOURNAL_TYPE_RES = {
    "HYBRID": re.compile('title="Hybrid Journal. It can contain Open Access articles"'),
    "OA": re.compile('title="This is an Open Access Journal"'),
    "SUBSCRIPTION": re.compile('title="Subscription journal, but a few articles may be freely available"'),
    "PARTIALLY_FREE": re.compile('title="Partially Free or Hybrid journal."'),
    "FREE": re.compile('title="Free journal"'),
    "ERROR": re.compile("Article not found or there are no recent issues available for this journal")
}

DATA_FILES = ["../../../data/apc_de.csv", "../../../data/offsetting/offsetting.csv"]
JOURNALTOC_RESULTS_FILE = "journaltoc_comparison.csv"

RESULTS_FILE_FIELDNAMES = ["journal_full_title", "publisher", "issns", "is_hybrid", "in_jtoc", "jtoc_publisher", "jtoc_title", "jtoc_type"]
ISSN_TYPES = ["issn", "issn_print", "issn_electronic", "issn_l"]

BATCH_SIZE = 1000
JTOCS_USERNAME = "user@example.com"


def main():
    analysed_journals = {}
    if path.isfile(JOURNALTOC_RESULTS_FILE):
        with open(JOURNALTOC_RESULTS_FILE) as results:
            reader = DictReader(results)
            for line in reader:
                title = line["journal_full_title"]
                if title not in analysed_journals:
                    analysed_journals[title] = line
    remaining_journals = {}
    
    for data_file in DATA_FILES:
        with open(data_file) as f:
            reader = DictReader(f)
            for line in reader:
                title = line["journal_full_title"]
                if title in analysed_journals:
                    continue
                if title not in remaining_journals:
                    remaining_journals[title] = {"journal_full_title": line["journal_full_title"], "publisher": line["publisher"], "is_hybrid": line["is_hybrid"], "issns": []}
                for issn_type in ISSN_TYPES:
                    issn = line[issn_type]
                    if issn not in remaining_journals[title]["issns"] and oat.is_wellformed_ISSN(issn):
                        remaining_journals[title]["issns"].append(issn)
                is_hybrid = line["is_hybrid"]
                if is_hybrid in ["TRUE", "FALSE"] and is_hybrid != remaining_journals[title]["is_hybrid"]:
                    remaining_journals[title]["is_hybrid"] = "FLIPPED"
            
    msg = "{} unique journals found in OpenAPC and offsetting files, {} already analysed, {} remaining."
    oat.print_g(msg.format(len(remaining_journals) + len(analysed_journals), len(analysed_journals), len(remaining_journals)))

    count = 0
    for title, fields in remaining_journals.items():
        count += 1
        entry = {field: None for field in RESULTS_FILE_FIELDNAMES}
        entry["journal_full_title"] = title
        for key in ["publisher", "is_hybrid"]:
            entry[key] = fields[key]
        entry["issns"] = "|".join(fields["issns"])
        msg = 'Analysing journal "{}" ({}), OpenAPC hybrid status is {}...'
        msg = msg.format(entry["journal_full_title"], entry["issns"], entry["is_hybrid"])
        oat.print_b(msg)
        for issn in fields["issns"]:
            oat.print_y("Looking up ISSN " + issn + "...")
            jtoc_metadata = get_jtoc_metadata(issn)
            if jtoc_metadata["jtoc_id"] is not None:
                entry["in_jtoc"] = "TRUE"
                for key in ["jtoc_publisher", "jtoc_title"]:
                    entry[key] = jtoc_metadata[key]
                journal_type = get_jtoc_journal_type(jtoc_metadata["jtoc_id"])
                entry["jtoc_type"] = journal_type
                msg = 'Journal found ("{}"), JournalTOCs type is {}'
                oat.print_g(msg.format(entry["jtoc_title"], entry["jtoc_type"]))
                break
        else:
            oat.print_r("None of the associated ISSNS found in JTOCs!")
            entry["in_jtoc"] = "FALSE"
        analysed_journals[title] = entry
        if count < BATCH_SIZE:
            sleep(2)
        else:
            break
        
    with open(JOURNALTOC_RESULTS_FILE, "w") as res_file:
        writer = DictWriter(res_file, fieldnames=RESULTS_FILE_FIELDNAMES)
        writer.writeheader()
        for _, entry in analysed_journals.items():
            writer.writerow(entry)

def get_jtoc_metadata(issn, retries=0):
    api_url = "http://www.journaltocs.ac.uk/api/journals/"
    user_param = "?user=" + JTOCS_USERNAME
    
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
            print ("Socket timeout, retrying (" + str(retries) + ")")
            return get_jtoc_metadata(issn, retries + 1)
        return None
    except ConnectionResetError:
        if retries <= 3:
            print ("ConnectionResetError, retrying (" + str(retries) + ")")
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
        for journal_type, re in JOURNAL_TYPE_RES.items():
            match = re.search(content)
            if match:
                return journal_type
        raise Exception("Error: No RE matched for journal at " + url)
        return None
    except socket.timeout:
        if retries <= 3:
            print ("Socket timeout, retrying (" + str(retries) + ")")
            return get_jtoc_journal_type(jtoc_id, retries + 1)
        return None
    except ConnectionResetError:
        if retries <= 3:
            print ("ConnectionResetError, retrying (" + str(retries) + ")")
            return get_jtoc_journal_type(jtoc_id, retries + 1)
        return None
    except HTTPError as httpe:
        print("HTTPError: {} - {}".format(httpe.code, httpe.reason))
        return None
    except URLError as urle:
        print("URLError: {}".format(urle.reason))
        return None

    
if __name__ == '__main__':
    sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
    import openapc_toolkit as oat
    main()
