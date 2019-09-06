#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import os
import sys


from Levenshtein import ratio

import openapc_toolkit as oat

MATCH_TYPES = [
    {
        "min_ratio": 0.9,
        "print_func": oat.print_y,
        "name": "Possible"
    },
    {
        "min_ratio": 0.95,
        "print_func": oat.print_g,
        "name": "Good"
    },
    {
        "min_ratio": 1.0,
        "print_func": oat.print_b,
        "name": "Perfect"
    }
]

def get_match_type(ratio):
    best_type = None
    for match_type in MATCH_TYPES:
        if ratio >= match_type["min_ratio"]:
            best_type = match_type
        else:
            break # requires ordering
    return best_type

def get_best_match(grid_names, institutions_name):
    highest_ratio = 0.0
    grid_name = None
    for name in grid_names:
        current_ratio = ratio(name, institutions_name)
        if current_ratio > highest_ratio:
            highest_ratio = current_ratio
            grid_name = name
    return grid_name, highest_ratio
    
def write_out_file(ins_header, ins_content):
    with open("out.csv", "w") as out_file:
        quote_mask = [False for x in range(7)]
        writer = oat.OpenAPCUnicodeWriter(out_file, quote_mask, False, False)
        print(ins_content)
        writer.write_rows(ins_header + ins_content)


ins_header, ins_content = oat.get_csv_file_content("../data/institutions.csv", "utf-8", True, False)

with open("grid.json") as grid_file:
    content = grid_file.read()
    json_dict = json.loads(content)
    grid_list = json_dict["institutes"]


for index, ins in enumerate(grid_list):
    deciles = {round((len(grid_list)/10) * i): str(i * 10) + "%" for i in range(1, 10)}
    if index in deciles:
        oat.print(deciles[index])
    if ins["status"] != "active":
        continue
    grid_names = [ins["name"]]
    if "aliases" in ins:
        grid_names += ins["aliases"]
    for institutions_row in ins_content:
        if oat.has_value(institutions_row[7]):
            continue
        institutions_name = institutions_row[2]
        grid_name, highest_ratio = get_best_match(grid_names, institutions_name)
        match_type = get_match_type(highest_ratio)
        if match_type != None:
            grid_id = ins["id"]
            msg = '{} match: "{}" might be Grid institution "{}" ({}).'
            question = 'Assign Grid ID {} ({})  (y/n/q)?'
            msg = msg.format(match_type["name"], institutions_name, grid_name, highest_ratio)
            question = question.format(grid_id, ins["name"])
            match_type["print_func"](msg)
            start = input(question)
            while start not in ["y", "n", "q"]:
                start = input("Please type 'y', 'n' or 'q':")
            if start == "y":
                institutions_row[7] = grid_id
            elif start == "q":
                write_out_file(ins_header, ins_content)
                sys.exit()
write_out_file(ins_header, ins_content)
