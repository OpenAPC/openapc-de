#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import datetime
import os
import re
import xml.etree.ElementTree as ET

from collections import OrderedDict
from csv import DictReader
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

import openapc_toolkit as oat
import opencost_toolkit_v2 as octk

ARG_HELP_STRINGS = {
    "output": 'Write raw harvested data to disk',
    "links": "Print OAI GetRecord links for all harvested articles, useful " +
             "for inspecting and debugging the original data",
    "validate": "Do not process any data and validate all records against the " +
                "openCost XSD schema instead. Only works for sources with type " +
                "'opencost'",
    "force_update": "Download a fresh copy of the openCost XSD from GitHub. Only "+
                    "works in connection with the -v option"
}

def oai_harvest(basic_url, metadata_prefix=None, oai_set=None, processing=None, out_file_suffix=None, data_type="intact", validate_only=False, force_update=False, record_url=None):
    """
    Harvest records via OAI-PMH
    """
    namespaces = {
        "opencost": "https://opencost.de",
        "oai_2_0": "http://www.openarchives.org/OAI/2.0/",
        "intact": "http://intact-project.org"
    }
    processing_regex = re.compile(r"'(?P<target>\w*?)':'(?P<generator>.*?)'")
    variable_regex = re.compile(r"%(\w*?)%")
    token_xpath = ".//oai_2_0:resumptionToken"
    url = basic_url + "?verb=ListRecords"
    if metadata_prefix:
        url += "&metadataPrefix=" + metadata_prefix
    if oai_set:
        url += "&set=" + oai_set
    processing_instructions = None
    if processing:
        match = processing_regex.match(processing)
        if match:
            groupdict = match.groupdict()
            target = groupdict["target"]
            generator = groupdict["generator"]
            variables = variable_regex.search(generator).groups()
            processing_instructions = {
                "generator": generator,
                "variables": variables,
                "target": target
            }
        else:
            print_r("Error: Unable to parse processing instruction!")
    record_url = basic_url + "?verb=GetRecord"
    if metadata_prefix:
        record_url += "&metadataPrefix=" + metadata_prefix
    oat.print_b("Harvesting from " + url)
    file_output = ""
    xml_content_strings = []
    while url is not None:
        try:
            request = Request(url)
            url = None
            response = urlopen(request)
            content_string = response.read()
            xml_content_strings.append(content_string)
            root = ET.fromstring(content_string)
            if out_file_suffix:
                file_output += content_string.decode()
            token = root.find(token_xpath, namespaces)
            if token is not None and token.text is not None:
                url = basic_url + "?verb=ListRecords&resumptionToken=" + token.text
        except HTTPError as httpe:
            code = str(httpe.getcode())
            print("HTTPError: {} - {}".format(code, httpe.reason))
        except URLError as urle:
            print("URLError: {}".format(urle.reason))
    if out_file_suffix:
        with open("raw_harvest_data_" + out_file_suffix, "w") as out:
            out.write(file_output)
    if data_type == "intact":
        return oat.process_intact_xml(processing_instructions, *xml_content_strings)
    elif data_type == "opencost":
        return octk.process_opencost_oai_records(processing_instructions, validate_only, force_update, record_url, *xml_content_strings)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help=ARG_HELP_STRINGS["output"], action="store_true")
    parser.add_argument("-l", "--print_record_links", help=ARG_HELP_STRINGS["links"], action="store_true")
    parser.add_argument("-v", "--validate_only", help=ARG_HELP_STRINGS["validate"], action="store_true")
    parser.add_argument("-u", "--force_update", help=ARG_HELP_STRINGS["force_update"], action="store_true")
    args = parser.parse_args()

    with open("harvest_list.csv", "r") as harvest_list:
        reader = DictReader(harvest_list)
        for line in reader:
            basic_url = line["basic_url"]
            if line["active"] == "TRUE":
                oai_set = line["oai_set"] if len(line["oai_set"]) > 0 else None
                prefix = line["metadata_prefix"] if len(line["metadata_prefix"]) > 0 else None
                processing = line["processing"] if len(line["processing"]) > 0 else None
                repo_type = line["type"]
                directory = os.path.join("..", line["directory"])
                out_file_suffix = os.path.basename(line["directory"]) if args.output else None
                if args.validate_only:
                    if repo_type != "opencost":
                        oat.print_y("Skipping source " + basic_url + " - Validation is not possible since it is not an openCost repository")
                        continue
                    oat.print_g("Starting validation run for source " + basic_url)
                    oai_harvest(basic_url, prefix, oai_set, processing, out_file_suffix, repo_type, args.validate_only, args.force_update)
                    continue
                oat.print_g("Starting harvest for source " + basic_url)
                publication_dicts = oai_harvest(basic_url, prefix, oai_set, processing, out_file_suffix, repo_type, args.validate_only, args.force_update)
                if repo_type == 'intact':
                    header = list(oat.OAI_COLLECTION_CONTENT.keys())
                elif repo_type == 'opencost':
                    header = list(octk.OPENCOST_EXTRACTION_FIELDS.keys())
                new_publications = {
                    "journal article": [list(header)],
                    "book": [list(header)],
                }
                for publication_dict in publication_dicts:
                    pub_type = publication_dict.get("type", "journal article") # opencost only, intact will be accepted as article per default
                    if pub_type not in new_publications:
                        msg = 'Skipping publication ({}), invalid type "{}"'
                        oat.print_y(msg.format(publication_dict["doi"], publication_dict["type"]))
                        continue
                    new_publications[pub_type].append([publication_dict[key] for key in header])
                now = datetime.datetime.now()
                date_string = now.strftime("%Y_%m_%d")
                for pub_type, content in new_publications.items():
                    if len(content) < 2:
                        continue
                    type_string = pub_type.replace(" ", "_")
                    file_name = "harvest_" + type_string + "_" + date_string + ".csv"
                    target = os.path.join(directory, file_name)
                    with open(target, "w") as t:
                        writer = oat.OpenAPCUnicodeWriter(t, openapc_quote_rules=True, has_header=True)
                        writer.write_rows(content)
            else:
                oat.print_y("Skipping inactive source " + basic_url)

if __name__ == '__main__':
    main()
