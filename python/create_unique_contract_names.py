#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv
import datetime

import openapc_toolkit as oat

consortium_map = {}

esac = oat.ESACHandling()
ESAC_TIME_STAMP = "%Y-%m-%d %H:%M:%S"

mapped_esac_ids = {}
unmapped_esac_ids = []

ask_msg = ('Assign contract_name "{}" to ESAC Id "{}"? Current name is "{}"\n' +
       '1) Yes and continue\n'
       '2) No and continue\n'
       '3) No and quit (save results to out.csv)')

# 2021-01-01 00:00:00

with open("consortium_map.csv", "r") as handle:
    reader = csv.DictReader(handle)
    for line in reader:
        target = line["normalized_name"]
        if not oat.has_value(target):
            target = line["name"]
        consortium_map[line["name"]] = target

source_header, source_content = oat.get_csv_file_content("../data/transformative_agreements/contracts.csv", enc='utf-8')
modified_content = []

do_quit = False

for line in source_content:
    if do_quit:
        modified_content.append(line)
        continue
    consortium = line[1]
    contract_name = line[2]
    esac_id = line[3]
    if esac_id in mapped_esac_ids:
        print(esac_id + " already mapped to " + mapped_esac_ids[esac_id])
        line[2] = mapped_esac_ids[esac_id]
        modified_content.append(line)
        continue
    if esac_id in unmapped_esac_ids:
        print(esac_id + " already marked for keeping")
        modified_content.append(line)
        continue
    mapped_consortium = consortium_map.get(consortium, "")
    esac_entry = esac.get_esac_entry(esac_id)
    if esac_entry is None:
        modified_content.append(line)
        continue
    start = esac_entry["Start date"]
    end = esac_entry["End date"]
    start_time = datetime.datetime.strptime(start, ESAC_TIME_STAMP)
    end_time = datetime.datetime.strptime(end, ESAC_TIME_STAMP)
    publisher = esac_entry["Publisher"]
    if contract_name.startswith("Springer Compact"):
        publisher = "Springer Compact" # SC special rule
    name_candidate = "{} ({}) {}-{}".format(publisher, mapped_consortium, start_time.year, end_time.year)
    if name_candidate == contract_name:
        print("name " + contract_name + " is already correct for esac_id " + esac_id)
        modified_content.append(line)
        continue
    ret = input(ask_msg.format(name_candidate, esac_id, contract_name))
    if ret not in ["1", "2", "3"]:
        repeat_msg = "Please select an option from 1,2,3 > "
        ret = input(repeat_msg)
    if ret == "1":
        mapped_esac_ids[esac_id] = name_candidate
        line[2] = mapped_esac_ids[esac_id]
        modified_content.append(line)
    elif ret == "2":
        unmapped_esac_ids.append(esac_id)
        modified_content.append(line)
    elif ret == "3":
        do_quit = True
    
with open("out.csv", "w") as out:
    mask = oat.QUOTEMASKS["contracts"]
    writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
    writer.write_rows(source_header + source_content)
    
