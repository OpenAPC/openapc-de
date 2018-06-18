#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from csv import DictReader, DictWriter
import os
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
    "HYBRID": re.compile('title="Hybrid Journal. It can contain Open Access articles"'),
    "OA": re.compile('title="This is an Open Access Journal"'),
    "SUBSCRIPTION": re.compile('title="Subscription journal, but a few articles may be freely available"'),
    "PARTIALLY_FREE": re.compile('title="Partially Free or Hybrid journal."'),
    "FREE": re.compile('title="Free journal"'),
    "ERROR": re.compile("Article not found or there are no recent issues available for this journal")
}

APC_DE_FILE = "../data/apc_de.csv"
JOURNALTOC_RESULTS_FILE = "journaltoc_comparison.csv"

RESULTS_FILE_FIELDNAMES = ["issn", "publisher", "journal_full_title", "is_hybrid", "in_jtoc", "jtoc_publisher", "jtoc_title", "jtoc_type"]
BATCH_SIZE = 100

def main():
    analysed_journals = {}
    if os.path.isfile(JOURNALTOC_RESULTS_FILE):
        with open(JOURNALTOC_RESULTS_FILE) as results:
            reader = DictReader(results)
            for line in reader:
                issn = line["issn"]
                if issn not in analysed_journals:
                    analysed_journals[issn] = line
    openapc_journals = {}
    with open(APC_DE_FILE) as apc_de:
        reader = DictReader(apc_de)
        for line in reader:
            issn = line["issn"]
            if issn not in openapc_journals and issn not in analysed_journals:
                openapc_journals[issn] = {"journal_full_title": line["journal_full_title"], "publisher": line["publisher"], "is_hybrid": line["is_hybrid"]}
    msg = "{} unique journals found in OpenAPC core data file, {} already analysed, {} remaining."
    oat.print_g(msg.format(len(openapc_journals) + len(analysed_journals), len(analysed_journals), len(openapc_journals)))

    count = 0
    for issn, fields in openapc_journals.items():
        count += 1
        entry = {field: None for field in RESULTS_FILE_FIELDNAMES}
        entry["issn"] = issn
        for key in ["journal_full_title", "publisher", "is_hybrid"]:
            entry[key] = fields[key]
        msg = 'Analysing journal "{}" ({}), OpenAPC hybrid status is {}...'
        msg = msg.format(fields["journal_full_title"], issn, fields["is_hybrid"])
        oat.print_b(msg)
        jtoc_metadata = get_jtoc_metadata(issn)
        if jtoc_metadata["jtoc_id"] is None:
            entry["in_jtoc"] = "FALSE"
            oat.print_y("Journal not found in journalTOCs!")
        else:
            entry["in_jtoc"] = "TRUE"
            for key in ["jtoc_publisher", "jtoc_title"]:
                entry[key] = jtoc_metadata[key]
            journal_type = get_jtoc_journal_type(jtoc_metadata["jtoc_id"])
            entry["jtoc_type"] = journal_type
            msg = 'Journal found ("{}"), JournalTOCs type is {}'
            oat.print_g(msg.format(entry["jtoc_title"], entry["jtoc_type"]))
        analysed_journals[issn] = entry
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
    user_param = "?user=openapc@uni-bielefeld.de"
    
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
    main()
