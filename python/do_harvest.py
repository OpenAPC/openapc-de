#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import datetime
import os

from collections import OrderedDict
from csv import DictReader

import openapc_toolkit as oat



def integrate_changes(articles, file_path, enriched_file=False):
    '''
    Update existing entries in a previously created harvest file.
    
    Args:
        articles: A list of article dicts, as retured by openapc_toolkit.oai_harvest()
        file_path: Path to the CSV file the new values should be integrated into.
        enriched_file: If true, columns which are overwritten during enrichment
                       will not be updated
    Returns:
        A tuple. The first element is a reduced list of article dicts, containing
        those which did not find a matching DOI in the file (Order preserved).
        The second element is the list of column headers encountered in the harvest 
        file.
    '''
    if not os.path.isfile(file_path):
        return (articles, None)
    enriched_blacklist = ["institution", "publisher", "journal_full_title", "issn", "license_ref", "pmid"]
    article_dict = OrderedDict()
    for article in articles:
        # This is possible because currently all repos use a local ID/record url, but it's just
        # a workaround. We might have to change to OAI record IDs later. 
        url = article["url"]
        if oat.has_value(url):
            article_dict[url] = article
    updated_lines = []
    fieldnames = None
    with open(file_path, "r") as f:
        reader = DictReader(f)
        fieldnames = reader.fieldnames
        updated_lines.append(list(fieldnames)) #header
        start_msg = "Integrating changes in harvest data into existing file {}"
        oat.print_g(start_msg.format(file_path))
        for line in reader:
            url = line["url"]
            line_num = reader.reader.line_num
            msg = "Line {}: Checking for changes ({})"
            oat.print_b(msg.format(line_num, url))
            if url in article_dict:
                for key, value in article_dict[url].items():
                    if enriched_file and key in enriched_blacklist:
                        continue
                    if key in line and value != line[key]:
                        update_msg = 'Updating value in column {} ("{}" -> "{}")'
                        oat.print_g(update_msg.format(key, line[key], value))
                        line[key] = value
                del(article_dict[url])
                updated_line = [line[key] for key in fieldnames]
                updated_lines.append(updated_line)
            else:
                remove_msg = "URL {} no longer found in harvest data, removing article"
                oat.print_r(remove_msg.format(url))
    with open(file_path, "w") as f:
        mask = oat.OPENAPC_STANDARD_QUOTEMASK if enriched_file else None
        writer = oat.OpenAPCUnicodeWriter(f, quotemask=mask, openapc_quote_rules=True, has_header=True)
        writer.write_rows(updated_lines)
    return (article_dict.values(), fieldnames)
    

def main():
    with open("harvest_list.csv", "r") as harvest_list:
        reader = DictReader(harvest_list)
        for line in reader:
            basic_url = line["basic_url"]
            if line["active"] == "TRUE":
                oat.print_g("Starting harvest from source " + basic_url)
                oai_set = line["oai_set"] if len(line["oai_set"]) > 0 else None
                prefix = line["metadata_prefix"] if len(line["metadata_prefix"]) > 0 else None
                processing = line["processing"] if len(line["processing"]) > 0 else None
                directory = os.path.join("..", line["directory"])
                articles = oat.oai_harvest(basic_url, prefix, oai_set, processing)
                harvest_file_path = os.path.join(directory, "all_harvested_articles.csv")
                enriched_file_path = os.path.join(directory, "all_harvested_articles_enriched.csv")
                new_article_dicts, header = integrate_changes(articles, harvest_file_path, False)
                integrate_changes(articles, enriched_file_path, True)
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
