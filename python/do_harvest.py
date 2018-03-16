#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import datetime
import os

from collections import OrderedDict

import openapc_toolkit as oat



def integrate_changes(articles, file_path, enriched_file=False):
    '''
    Update existing entries in a previously created harvest file.
    
    Args:
        articles: A list of article dicts, as retured by openapc_toolkit.oai_harvest
        file_path: Path to the CSV file the new values should be integrated into.
        enriched_file: If true, columns which are overwritten during enrichment
                       will not be updated
    Returns:
        A tuple. The first element is a reduced list of article dicts, containing
        those which did not find a matching DOI in the file (Order preserved).
        The second element is the list of column headers encountered in the harvest 
        file.
    '''
    if not os.path.isfile("file_path"):
        return (articles, None)
    enriched_blacklist = ["publisher", "journal_full_title", "issn", "license_ref", "pmid"]
    article_dict = OrderedDict()
    for article in articles:
        doi = article["doi"]
        if oat.has_value(doi):
            article_dict[doi] = article
    updated_lines = []
    fieldnames = None
    with open(file_path, "r") as f:
        reader = oat.UnicodeReader(oat, encoding="utf-8")
        fieldnames = reader.reader.fieldnames
        updated_lines.append(fieldnames) #header
        for line in reader:
            doi = line["doi"]
            line_num = reader.reader.line_num
            if oat.has_value(doi):
                msg = "Line {}: Checking for changes ({})"
                oat.print_y(msg.format(line_num, doi))
            else:
                msg = "Line {}: No DOI found, change check not possible"
                oat.print_r(msg.format(line_num))
            if doi in article_dict:
                for key, value in article_dict[doi].iteritems():
                    if enriched_file and key in enriched_blacklist:
                        continue
                    if key in line and value != line[key]:
                        update_msg = 'Updating value in column {} ("{}" -> "{}")'
                        oat.print_g(update_msg.format(key, line[key], value))
                        line[key] = value
                del(article_dict[doi])
            updated_line = [line[key] for key in fieldnames]
            updated_lines.append(updated_line)
    with open(file_path, "w") as f:
        writer = OpenAPCUnicodeWriter(f, openapc_quote_rules=True, has_header=True)
        writer.write_rows(updated_articles)
    return (article_dict.values(), fieldnames)
    

def main():
    with open("harvest_list.csv", "r") as harvest_list:
        reader = oat.UnicodeDictReader(harvest_list, encoding="utf-8")
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
                if header is not None:
                    new_articles = [header]
                else:
                    # if no header was returned, an "all_harvested" file doesn't exist yet
                    new_articles = [oat.OAI_COLLECTION_CONTENT.values()]
                for artice_dict in new_article_dicts:
                    new_articles.append([article_dict[key] for key in header])
                now = datetime.datetime.now()
                date_string = now.strftime("%Y_%m_%d")
                file_name = "new_articles_" + date_string + ".csv"
                target = os.path.join(directory, file_name)
                with open(target, "w") as t:
                    writer = OpenAPCUnicodeWriter(t, openapc_quote_rules=True, has_header=True)
                    writer.write_rows(new_articles)
            else:
                oat.print_y("Skipping inactive source " + basic_url)
            
    
if __name__ == '__main__':
    main()
