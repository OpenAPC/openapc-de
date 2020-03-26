#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from csv import DictReader, unix_dialect, writer

from test import whitelists as wl

mappings = {
    "journal_full_title": {},
    "publisher": {}
}

def _get_publisher_identity(publisher):
    for entry in wl.PUBLISHER_IDENTITY:
        if publisher in entry[1]:
            publisher = entry[0][0]
    return publisher

for data_file in ["../data/apc_de.csv", "../data/transformative_agreements/transformative_agreements.csv"]:
    with open(data_file, "r") as handle:
        reader = DictReader(handle)
        for line in reader:
            for field in ["issn", "issn_print", "issn_electronic", "issn_l"]:
                issn = line[field]
                if issn == "NA":
                    continue
                for map_type in mappings.keys():
                    if map_type == "publisher":
                        if issn in wl.JOURNAL_OWNER_CHANGED:
                            continue
                        value = _get_publisher_identity(line[map_type])
                    else:
                        value = line[map_type]
                    if issn not in mappings[map_type]:
                        mappings[map_type][issn] = value
                    else:
                        if mappings[map_type][issn] != value:
                            msg = 'Inconsistency: ISSN {} maps to different {}s: "{}" and "{}"'
                            print(msg.format(issn, map_type, mappings[map_type][issn], value))

for map_type in mappings.keys():
    result = list(mappings[map_type].items())
    result.sort(key=lambda x: x[1])
    with open("issn_to_" +  map_type + ".csv", "w") as out_file:
        csv_writer = writer(out_file, dialect=unix_dialect)
        csv_writer.writerow(["issn", map_type])
        csv_writer.writerows(result)
        
