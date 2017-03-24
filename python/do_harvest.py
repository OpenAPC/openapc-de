#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import datetime
import os

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "selective_harvesting": ("While harvesting, check the core data " +
                             "file for existing DOI, pmid and URL " +
                             "duplicates and do not ingest the " +
                             "according articles.")
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--selective_harvesting", action="store_true",
                        help=ARG_HELP_STRINGS["selective_harvesting"])
    args = parser.parse_args()
    with open("harvest_list.csv", "r") as harvest_list:
        reader = oat.UnicodeDictReader(harvest_list, encoding="utf-8")
        for line in reader:
            basic_url = line["basic_url"]
            if line["active"] == "TRUE":
                oat.print_g("Starting harvest from source " + basic_url)
                processing = None
                if len(line["processing"]) > 0:
                    processing = line["processing"]
                oat.oai_harvest(basic_url,
                                line["metadata_prefix"],
                                line["oai_set"],
                                processing,
                                args.selective_harvesting)
                now = datetime.datetime.now()
                date_string = now.strftime("%Y_%m_%d")
                file_name = "oai_harvest_" + date_string + ".csv"
                target = os.path.join("..", line["directory"], file_name)
                os.rename("out.csv", target)
            else:
                oat.print_y("Skipping inactive source " + basic_url)
            
    
if __name__ == '__main__':
    main()
