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
    "integrate": ('Integrate changes in harvested data into existing ' +
                  'collected files ("all_harvested_articles.csv" and '+
                  '"all_harvested_articles_enriched.csv")'),
    "output": 'Write raw harvested data to disk',
    "links": "Print OAI GetRecord links for all harvested articles, useful " +
             "for inspecting and debugging the original data"
}

def integrate_changes(articles, file_path, enriched_file=False, dry_run=False):
    '''
    Update existing entries in a previously created harvest file.
    
    Args:
        articles: A list of article dicts, as retured by openapc_toolkit.oai_harvest()
        file_path: Path to the CSV file the new values should be integrated into.
        enriched_file: If true, columns which are overwritten during enrichment
                       will not be updated
        dry_run: Do not make any changes to the file (but still report changes and
                 return the list of unencountered articles)
    Returns:
        A tuple. The first element is a reduced list of article dicts, containing
        those which did not find a matching DOI in the file (Order preserved).
        The second element is the list of column headers encountered in the harvest 
        file.
    '''

    messages = {
        'wet': {
            'start': 'Integrating changes in harvest data into existing file {}',
            'line_change': 'Line {} ({}): Updating value in column {} ("{}" -> "{}")',
            'remove': 'PID {} no longer found in harvest data, removing article',
        },
        'dry': {
            'start': 'Dry Run: Comparing harvest data to existing file {}',
            'line_change': 'Line {} ({}): Change in column {} ("{}" -> "{}")',
            'remove': 'PID {} no longer found in harvest data, article would be removed',
        }
    }

    messages = messages['dry'] if dry_run else messages['wet']

    if not os.path.isfile(file_path):
        return (articles, None)
    enriched_blacklist = ["institution", "publisher", "journal_full_title", "issn", "license_ref", "pmid"]
    article_dict = OrderedDict()
    for article in articles:
        # Harvested articles use OAI record IDs in the url field as PID.
        url = article["url"]
        if oat.has_value(url):
            article_dict[url] = article
    updated_lines = []
    fieldnames = None
    with open(file_path, "r") as f:
        reader = DictReader(f)
        fieldnames = reader.fieldnames
        updated_lines.append(list(fieldnames)) #header
        oat.print_y(messages["start"].format(file_path))
        for line in reader:
            url = line["url"]
            if not oat.has_value(line["institution"]):
                # Do not change empty lines
                updated_lines.append([line[key] for key in fieldnames])
                continue
            line_num = reader.reader.line_num
            if url in article_dict:
                for key, value in article_dict[url].items():
                    if enriched_file and key in enriched_blacklist:
                        continue
                    if key in line and value != line[key]:
                        oat.print_g(messages["line_change"].format(line_num, line["url"], key, line[key], value))
                        line[key] = value
                del(article_dict[url])
                updated_line = [line[key] for key in fieldnames]
                updated_lines.append(updated_line)
            else:
                oat.print_r(messages["remove"].format(url))
    if not dry_run:
        with open(file_path, "w") as f:
            mask = oat.OPENAPC_STANDARD_QUOTEMASK if enriched_file else None
            writer = oat.OpenAPCUnicodeWriter(f, quotemask=mask, openapc_quote_rules=True, has_header=True)
            writer.write_rows(updated_lines)
    return (article_dict.values(), fieldnames)

def oai_harvest(basic_url, metadata_prefix=None, oai_set=None, processing=None, out_file_suffix=None, data_type="intact"):
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
    if processing:
        match = processing_regex.match(processing)
        if match:
            groupdict = match.groupdict()
            target = groupdict["target"]
            generator = groupdict["generator"]
            variables = variable_regex.search(generator).groups()
        else:
            print_r("Error: Unable to parse processing instruction!")
            processing = None
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
        return oat.process_intact_xml(*xml_content_strings)
    elif data_type == "opencost":
        return octk.process_opencost_xml(*xml_content_strings)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--integrate", help=ARG_HELP_STRINGS["integrate"], action="store_true")
    parser.add_argument("-o", "--output", help=ARG_HELP_STRINGS["output"], action="store_true")
    parser.add_argument("-l", "--print_record_links", help=ARG_HELP_STRINGS["links"], action="store_true")
    args = parser.parse_args()

    with open("harvest_list.csv", "r") as harvest_list:
        reader = DictReader(harvest_list)
        for line in reader:
            basic_url = line["basic_url"]
            if line["active"] == "TRUE":
                oat.print_g("Starting harvest from source " + basic_url)
                oai_set = line["oai_set"] if len(line["oai_set"]) > 0 else None
                prefix = line["metadata_prefix"] if len(line["metadata_prefix"]) > 0 else None
                processing = line["processing"] if len(line["processing"]) > 0 else None
                repo_type = line["type"]
                directory = os.path.join("..", line["directory"])
                out_file_suffix = os.path.basename(line["directory"]) if args.output else None
                articles = oai_harvest(basic_url, prefix, oai_set, processing, out_file_suffix, repo_type)
                harvest_file_path = os.path.join(directory, "all_harvested_articles.csv")
                enriched_file_path = os.path.join(directory, "all_harvested_articles_enriched.csv")
                new_article_dicts, header = integrate_changes(articles, harvest_file_path, False, not args.integrate)
                integrate_changes(articles, enriched_file_path, True, not args.integrate)
                if header is None:
                    # if no header was returned, an "all_harvested" file doesn't exist yet
                    header = list(oat.OAI_COLLECTION_CONTENT.keys())
                new_articles = [header]
                for article_dict in new_article_dicts:
                    new_articles.append([article_dict[key] for key in header])
                now = datetime.datetime.now()
                date_string = now.strftime("%Y_%m_%d")
                file_name = "new_articles_" + date_string + ".csv"
                target = os.path.join(directory, file_name)
                with open(target, "w") as t:
                    writer = oat.OpenAPCUnicodeWriter(t, openapc_quote_rules=True, has_header=True)
                    writer.write_rows(new_articles)
            else:
                oat.print_y("Skipping inactive source " + basic_url)

if __name__ == '__main__':
    main()
