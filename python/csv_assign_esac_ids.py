#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import sys

import openapc_toolkit as oat
from mappings import AGREEMENT_PUBLISHER_MAP

ARG_HELP_STRINGS = {
    "ta_file": "The ta file, must have an additional column 'esac_id' at index 19",
    "esac_file": "The esac registry file, with two additional OAPC-normalized columns: " +
                 "Publisher_OAPC and Country_OAPC",
    "ins_file": "The OpenAPC institutions file"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ta_file", help=ARG_HELP_STRINGS["ta_file"])
    parser.add_argument("esac_file", help=ARG_HELP_STRINGS["esac_file"])
    parser.add_argument("ins_file", help=ARG_HELP_STRINGS["ins_file"], default="../data/institutions.csv")
    
    args = parser.parse_args()
    
    esac_content = {}
    print("Processing ESAC file...")
    with open(args.esac_file, encoding="utf-8") as esac_file:
        reader = csv.DictReader(esac_file)
        for line in reader:
            country_oapc = line["Country_OAPC"]
            if country_oapc == "NA":
                continue
            if country_oapc not in esac_content:
                esac_content[country_oapc] = []
            esac_content[country_oapc].append(line)
    print("...Done")
    
    ins_lookup = {}
    print("Processing institutions file...")
    with open(args.ins_file, encoding="utf-8") as ins_file:
        reader = csv.DictReader(ins_file)
        for line in reader:
            ins_lookup[line["institution"]] = line["country"]
    print("...Done")
    
    print("Processing TA file...")
    source_header, source_content = oat.get_csv_file_content(args.ta_file, enc='utf-8')
    if not source_header[0][20] == "esac_id":
        oat.print_r("TA file is missing an additional column 'esac_id' at index 20!")
        sys.exit()
        
    assigned_ids = {}
    for line in source_content:
        ins = line[0]
        period = line[1]
        publisher = line[6]
        publisher = AGREEMENT_PUBLISHER_MAP.get(publisher, publisher)
        agreement = line[19]
        esac_id = line[20]
        if ins not in assigned_ids:
            assigned_ids[ins] = {}
        if period not in assigned_ids[ins]:
            assigned_ids[ins][period] = {}
        if publisher not in assigned_ids[ins][period]:
            assigned_ids[ins][period][publisher] = {}
        if agreement not in assigned_ids[ins][period][publisher]:
            assigned_ids[ins][period][publisher][agreement] = esac_id
        
    sug_head = "Line {}: Trying to assign an ESAC ID for:\nInstitution: {}, Period: {}, Publisher: {}, Agreement: {}\n\nThe following candidate TAs have been found in the ESAC Registry:\n\n"
    sug_tmpl = "{}) Org: {}, Start: {}, End: {}, ID: {}\n"
    sug_foot = "x) None of the above, assign value NA and continue\nq) None of the above, quit and save results to out.csv\n> "
    
    for line_num, line in enumerate(source_content):
        if line[20] != "unchecked":
            continue
        ins = line[0]
        period = line[1]
        publisher_orig = line[6]
        publisher = AGREEMENT_PUBLISHER_MAP.get(publisher_orig, publisher_orig)
        agreement = line[19]
        if publisher == publisher_orig:
            publisher_str = publisher
        else:
            publisher_str = publisher + ' [mapped from "{}"]'.format(publisher_orig)
        country = ins_lookup[ins]
        assigned_id = assigned_ids[ins][period][publisher][agreement]
        if assigned_id != "unchecked":
            line[20] = assigned_id
            msg = "Line {}: ID for combination already assigned ({}, {}, {}, {}) => {}"
            print(msg.format(line_num, ins, period, publisher, agreement, assigned_id))
            continue
        if country == 'LIE':
            country = 'CHE' # Liechtenstein participates in Swiss agreements
        if country not in esac_content:
            oat.print_y("Line {}: Country '{}' not found in ESAC file!".format(line_num, country))
            continue
        if agreement == "DEAL Springer Nature Germany" and int(period) >= 2020 and int(period) <= 2023:
            print("Line {}: ESAC ID for Springer DEAL assigned automatically".format(line_num))
            line[20] = "sn2020deal"
            continue
        if agreement == "DEAL Wiley Germany" and int(period) >= 2019 and int(period) <= 2023:
            print("Line {}: ESAC ID for Wiley DEAL assigned automatically".format(line_num))
            line[20] = "wiley2019deal"
            continue
        candidates = []
        country_tas = esac_content[country]
        candidates = [ta for ta in country_tas if ta["Publisher_OAPC"] == publisher]
        if candidates:
            msg = sug_head.format(line_num, ins, period, publisher_str, agreement)
            for num, can in enumerate(candidates):
                msg += sug_tmpl.format(num, can["Organization"], can["Start date"], can["End date"], can["ID"])
            msg += sug_foot
            ret = input(msg)
            opts = [str(x) for x in list(range(len(candidates)))] + ["x", "q"]
            while ret not in opts:
                repeat_msg = "Please select an option from {} >"
                ret = input(repeat_msg.format(opts))
            if ret == "q":
                break
            if ret == "x":
                line[20] = "NA"
            else:
                line[20] = candidates[int(ret)]["ID"]
            assigned_ids[ins][period][publisher][agreement] = line[20]
    
    with open('out.csv', 'w') as out:
        mask = [True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        writer = oat.OpenAPCUnicodeWriter(out, mask, True, True)
        writer.write_rows(source_header + source_content)

if __name__ == '__main__':
    main()
