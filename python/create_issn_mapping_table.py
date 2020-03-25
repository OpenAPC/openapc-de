#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from csv import DictReader, unix_dialect, writer

issn_map = {}

for data_file in ["../data/apc_de.csv", "../data/transformative_agreements/transformative_agreements.csv"]:
    with open(data_file, "r") as handle:
        reader = DictReader(handle)
        for line in reader:
            for field in ["issn", "issn_print", "issn_electronic", "issn_l"]:
                issn = line[field]
                if issn == "NA":
                    continue
                if issn not in issn_map:
                    issn_map[issn] = line["journal_full_title"]
                else:
                    if issn_map[issn] != line["journal_full_title"]:
                        msg = 'Inconsistency: ISSN {} maps to different journals: "{}" and "{}"'
                        print(msg.format(issn, issn_map[issn], line["journal_full_title"]))

result = list(issn_map.items())
result.sort(key=lambda x: x[1])
with open("out.csv", "w") as out_file:
    csv_writer = writer(out_file, dialect=unix_dialect)
    csv_writer.writerow(["issn", "journal_full_title"])
    csv_writer.writerows(result)
        
