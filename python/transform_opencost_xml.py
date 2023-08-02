#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
from csv import DictWriter

import openapc_toolkit as oat

parser = argparse.ArgumentParser()
parser.add_argument("xml_file", help="An openCost XML file which should validate against the official openCost XSD schema")
args = parser.parse_args()

articles = None

with open(args.xml_file) as f:
    content = f.read()
    articles = oat.process_opencost_xml(content)
    
fieldnames = list(oat.OPENCOST_EXTRACTION_FIELDS.keys())
with open("out.csv", "w") as out:
    writer = DictWriter(out, fieldnames)
    writer.writeheader()
    for article in articles:
        writer.writerow(article)
