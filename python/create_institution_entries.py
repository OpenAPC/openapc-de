#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import time
import sys

from copy import deepcopy

import openapc_toolkit as oat
import mappings

ARG_HELP_STRINGS = {
    "source_file": "The source csv file. Default: ../data/apc_de.csv",
    "source_file_ins_column": "The numerical index of the institution column. Default: 0",
    "ins_table": "Check names against the OpenAPC institutions table first and " +
                 "only look up unknown institutions. Default: True",
    "encoding": "The encoding of the CSV file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "num_lookups": "Maximum number of lookups before quitting and writing " +
                   "results to out.csv. Default: 10"
}

INS_LINE_TMPL = {
    "institution": "NA",
    "institution_cubes_name": "NA",
    "institution_full_name": "NA",
    "continent": "NA",
    "country": "NA",
    "state": "NA",
    "openapc_data_dir": "NA",
    "ror_id": "NA",
    "institution_type": "NA",
    "institution_group": "NA",
    "info_url": "NA",
    "comment": "NA"
}

def _build_ins_line_dict(ins_name, ror_item):
    names = _get_ror_names(ror_item)
    line = deepcopy(INS_LINE_TMPL)
    line["institution"] = ins_name
    line["institution_cubes_name"] = _build_cubes_name(ins_name)
    line["institution_full_name"] = names["main"]
    geo_data = {
        "continent": ror_item["locations"][0]["geonames_details"]["continent_name"],
        "country": ror_item["locations"][0]["geonames_details"]["country_code"],
        "state": ror_item["locations"][0]["geonames_details"]["country_subdivision_code"],
    }
    for geo_level, geo_name in geo_data.items():
        if geo_name not in mappings.GEO_MAPPINGS:
            msg = 'WARNING: Geo name "{}" not found in mappings.GEO_MAPPINGS, using original value'
            oat.print_y(msg.format(geo_name))
            line[geo_level] = geo_name
        else:
            line[geo_level] = mappings.GEO_MAPPINGS[geo_name]
    line["ror_id"] = ror_item["id"]
    for link_dict in ror_item["links"]:
        if link_dict["type"] == "website":
            line["info_url"] = link_dict["value"]
            break
    return line

def _build_cubes_name(ins_name):
    cubes_name = ins_name.lower().replace(" ", "_").replace("'", "")
    if cubes_name.endswith("university"):
        cubes_name = cubes_name[:-9]
    elif cubes_name.startswith("university_of"):
        cubes_name = cubes_name[14:] + "_u"
    return cubes_name

def _load_ins_data():
    ins_map = {}
    ror_map = {}
    field_names = None
    with open(oat.INSTITUTIONS_FILE, "r") as ins_file:
        reader = csv.DictReader(ins_file)
        field_names = reader.fieldnames
        for line in reader:
            ins_map[line["institution"]] = line
            ror_map[line["ror_id"]] = line
    return {"ins_map": ins_map, "ror_map": ror_map, "field_names": field_names}

def _get_ror_names(ror_item):
    ret = {
        "main": "",
        "other_lang": [],
        "aliases": []
    }
    names = ror_item["names"]
    for name_dict in names:
        if "ror_display" in name_dict["types"]:
            ret["main"] = name_dict["value"]
        elif "label" in name_dict["types"]:
            ret["other_lang"].append(name_dict["value"])
        elif "alias" in name_dict["types"]:
            ret["aliases"].append(name_dict["value"])
    return ret

def _build_name_string(names_dict):
    name_str = 'Main variant: {}, {}{}'
    main = '"' + oat.colorize(names_dict["main"], "green") + '"'
    other = ""
    aliases = ""
    if names_dict["other_lang"]:
        other = "other languages: "
        for name in names_dict["other_lang"]:
            other += '"' + oat.colorize(name, "cyan") + '", '
    if names_dict["aliases"]:
        aliases = "aliases: "
        for name in names_dict["aliases"]:
            aliases += '"' + oat.colorize(name, "magenta") + '", '
    return name_str.format(main, other, aliases)[:-2]

def _ror_lookup(institution_name):
    ret = oat.search_institution_in_ror(institution_name)
    if ret["success"] == False:
        msg = "An Error occured while querying the ROR API: {}"
        oat.print_r(msg.format(ret["error_msg"]))
        return {}
    data = ret["data"]
    if data["number_of_results"] == 0:
        msg = 'No ROR entry found for institution "{}"'
        oat.print_y(msg.format(institution_name))
        return {}
    selected_item = data["items"][0]
    if data["number_of_results"] > 1:
        ask_msg = 'Found more than one possible candidate in ROR for institution name "{}", please select one:\n'
        ask_msg = ask_msg.format(institution_name)
        options = []
        current_option = 1
        for ror_item in data["items"][:9]:
            names =  _get_ror_names(ror_item)
            name_str = _build_name_string(names)
            ask_msg += str(current_option) + ") " + name_str + "\n"
            options.append(str(current_option))
            current_option += 1
        ask_msg += 'x) None of the above, skip entry\n'
        select = input(ask_msg)
        while select not in options + ["x"]:
            select = input("Please select one of " + ", ".join(options + ["x"]))
        if select in options:
            selected_item = data["items"][int(select) - 1]
        else:
            return {}
    else:
        names =  _get_ror_names(selected_item)
        name_str = _build_name_string(names)
        print('Found a candidate in ROR for institution "{}":\n'.format(institution_name) + name_str)
    return selected_item

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--source_file", default="../data/apc_de.csv", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("-c", "--source_file_key_column", type=int, default=0, help=ARG_HELP_STRINGS["source_file_ins_column"])
    parser.add_argument("-i", "--ins_table", action="store_true", default=True, help=ARG_HELP_STRINGS["ins_table"])
    parser.add_argument("-e", "--encoding", default="utf-8", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-n", "--num_lookups", type=int, default=10, help=ARG_HELP_STRINGS["num_lookups"])
    
    args = parser.parse_args()

    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            print(msg.format(args.encoding, codec.name))
            args.encoding = codec.name
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()

    ins_data = _load_ins_data()
    field_names = ins_data["field_names"]
    ins_map = ins_data["ins_map"] if args.ins_table else None
    ror_map = ins_data["ror_map"] if args.ins_table else None

    source_header, source_content = oat.get_csv_file_content(args.source_file, enc=args.encoding, force_header=True)

    oat.print_g('Extracting institution names from column "{}"'.format(source_header[0][args.source_file_key_column]))

    processed_names = []
    generated_ins_lines = []
    lookups = 0
    for line in source_content:
        if lookups >= args.num_lookups:
            break
        institution_name = line[args.source_file_key_column]
        if institution_name in processed_names:
            continue
        print("----------------")
        if ins_map is not None and institution_name in ins_map:
            msg = 'Institution "{}" already present in institutions.csv, skipping...'
            processed_names.append(institution_name)
            oat.print_c(msg.format(institution_name))
            continue
        ror_item = _ror_lookup(institution_name)
        if not ror_item:
            continue
        lookups += 1
        ror_id = ror_item["id"]
        if ror_map is not None and ror_id in ror_map:
            msg = 'WARNING: ROR ID ({}) for institution "{}" already present in institutions.csv - OpenAPC internal name is "{}". Skipping entry...'
            oat.print_y(msg.format(ror_id, institution_name, ror_map[ror_id]["institution"]))
            continue
        line = _build_ins_line_dict(institution_name, ror_item)
        generated_ins_lines.append(line)
        processed_names.append(institution_name)
        time.sleep(1)

    with open("out.csv", "w") as out:
        writer = csv.DictWriter(out, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(generated_ins_lines)

if __name__ == '__main__':
    main()
