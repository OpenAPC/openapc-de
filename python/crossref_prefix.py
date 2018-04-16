#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import os
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
import xml.etree.ElementTree as ET

import openapc_toolkit as oat

def get_prefix(doi):
    url = 'http://data.crossref.org/' + doi
    req = Request(url)
    req.add_header("Accept", "application/vnd.crossref.unixsd+xml")
    try:
        response = urlopen(req)
        content_string = response.read()
        root = ET.fromstring(content_string)
        result = root.findall(".//cr_qr:crm-item[@name='prefix-name']", {"cr_qr": "http://www.crossref.org/qrschema/3.0"})
        return result[0].text
    except HTTPError as httpe:
        code = str(httpe.getcode())
        return "HTTPError: {} - {}".format(code, httpe.reason)
    except URLError as urle:
        return "URLError: {}".format(urle.reason)
    except ET.ParseError as etpe:
        return "ElementTree ParseError: {}".format(str(etpe))

parser = argparse.ArgumentParser()
parser.add_argument("doi_or_file", help="An OpenAPC-compatible CSV file or a single DOI to look up in crossref.")
args = parser.parse_args()

arg = args.doi_or_file
if os.path.isfile(arg):
    csv_file = open(arg, "r", encoding="utf8")
    reader = csv.reader(csv_file)
    line_number = 0
    for line in reader:
        if not line:
            prefix = ""
        else:
            prefix = get_prefix(line[3])
        result = str(line_number) + ": " + prefix
        if prefix == "Springer (Biomed Central Ltd.)":
            oat.print_g(result)
        elif prefix == "Nature Publishing Group":
            oat.print_r(result)
        else:
            print(result)
        line_number += 1
else:
    print(get_prefix(arg))
