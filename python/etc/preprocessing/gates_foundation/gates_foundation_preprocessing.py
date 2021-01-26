#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import csv
import datetime
import json
from os import path
import sys
from urllib.error import HTTPError, URLError

ARG_HELP_STRINGS = {
    "source_file": "The csv input file",
    "doi_file": "The additional report containing a PublicationID -> DOI mapping",
    "exchange_rates_cache_file": "An optional cache file for ECB exchange rates",
    "no_decorations": "Do not use ANSI coded colors in console output"
}

EXCHANGE_RATES_CACHE = {}
EXCHANGE_RATES_CACHE_FILE = None

DELETE_REASONS = {}

OUTPUT_FIELDS = ["Publisher", "Journal title", "Currency", "APC", "Date Payment Completed",
                 "institution", "period", "euro", "doi", "is_hybrid"]

NO_DECORATIONS = False


def delete_line(line_dict, reason):
    _print("r", "   - " + reason + ", line deleted")
    if reason not in DELETE_REASONS:
        DELETE_REASONS[reason] = 1
    else:
        DELETE_REASONS[reason] += 1
    for key in line_dict:
        line_dict[key] = ""

def line_as_list(line_dict):
    return [line_dict[field] for field in FIELDNAMES[FORMAT]]

def is_zero_value(string):
    number = float(string)
    return number == 0.0

def is_valid_date(date_match_obj):
    gd = date_match_obj.groupdict()
    if gd["year"] is None or gd["month"] is None or gd["day"] is None:
        return False
    try:
        date = datetime.datetime(int(gd["year"]), int(gd["month"]), int(gd["day"]))
        if date > datetime.datetime.now():
            return False
        return True
    except ValueError:
        return False

def shutdown():
    _print("r", "Updating exchange rates cache...")
    with open(EXCHANGE_RATES_CACHE_FILE, "w") as f:
        f.write(json.dumps(EXCHANGE_RATES_CACHE, sort_keys=True, indent=4, separators=(',', ': ')))
        f.flush()
    _print("r", "Done.")
    sys.exit()

def _print(color, s):
    if color in ["r", "y", "g", "b"] and not NO_DECORATIONS:
        getattr(oat, "print_" + color)(s)
    else:
        print(s)


def get_exchange_rate(currency, date):
    if currency not in EXCHANGE_RATES_CACHE:
        EXCHANGE_RATES_CACHE[currency] = {}
    if not len(EXCHANGE_RATES_CACHE[currency]):
        try:
            rates = oat.get_euro_exchange_rates(currency)
            EXCHANGE_RATES_CACHE[currency] = rates
        except HTTPError as httpe:
            _print("r", "HTTPError while querying the ECB data warehouse: " + httpe.reason)
            shutdown()
        except URLError as urle:
            _print("r", "URLError while querying the ECB data warehouse: " + urle.reason)
            shutdown()
        except ValueError as ve:
            _print("r", "ValueError while querying the ECB data warehouse: " + ve.reason)
            shutdown()
    # The ECB does not report exchange rate for all dates due to weekends/holidays. We have
    # consider some days in advance to find the next possible data in some cases.
    for i in range(6):
        future_day = date + datetime.timedelta(days=i)
        search_day = future_day.strftime("%Y-%m-%d")
        if search_day in EXCHANGE_RATES_CACHE[currency]:
            _print("y", "     [Exchange rates: Cached value used]")
            if i > 0:
                msg = "     [Exchange rates: No rate found for date {}, used value for {} instead]"
                _print("y", msg.format(date, search_day))
            return EXCHANGE_RATES_CACHE[currency][search_day]
    _print("r", "Error during Exchange rates lookup: No rate for " + date.strftime("%Y-%m-%d") + " or any following day!")
    shutdown()
        
def calculate_euro_value(line):
    date_string = line["Date Payment Completed"]
    date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    apc_value = line["APC"]
    if not is_zero_value(apc_value):
        currency = line["Currency"].strip()
        if currency == "EUR":
            line["euro"] = apc_value
            msg = "   - Created euro field ('{}') by using the value in 'APC' directly since the currency is EUR"
            _print("g", msg.format(apc_value))
        else:
            rate = get_exchange_rate(currency, date)
            euro_value = round(float(apc_value) / float(rate), 2)
            line["euro"] = str(euro_value)
            msg = "   - Created euro field ('{}') by dividing the value in 'APC' ({}) by {} (EUR -> {} conversion rate on {}) [ECB]"
            msg = msg.format(euro_value, apc_value, rate, currency, date.strftime("%Y-%m-%d"))
            _print("g", msg)
    else:
        delete_line(line, "APC value is zero")
       
def main():
    global EXCHANGE_RATES_CACHE, EXCHANGE_RATES_CACHE_FILE, NO_DECORATIONS
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("doi_file", help=ARG_HELP_STRINGS["doi_file"])
    parser.add_argument("-c", "--exchange_rates_cache_file", help=ARG_HELP_STRINGS["exchange_rates_cache_file"], default="_exchange_rates_cache.json")
    parser.add_argument("-n", "--no-decorations", help=ARG_HELP_STRINGS["no_decorations"], action="store_true")
    
    args = parser.parse_args()
    NO_DECORATIONS = args.no_decorations
    EXCHANGE_RATES_CACHE_FILE = args.exchange_rates_cache_file

    if path.isfile(args.exchange_rates_cache_file):
        with open(EXCHANGE_RATES_CACHE_FILE, "r") as f:
            try:
                EXCHANGE_RATES_CACHE = json.loads(f.read())
            except ValueError:
                _print("r", "Could not decode a cache structure from " + EXCHANGE_RATES_CACHE_FILE + ", starting with an empty cache.")
    
    doi_mappings = {}
    with open(args.doi_file, "r") as doi_file:
        reader = csv.DictReader(doi_file)
        for line in reader:
            pub_id = line["PublicationID"]
            doi_mappings[pub_id] = line["DOI"]
    
    f = open(args.source_file, "r", encoding="utf-8")
    reader = csv.DictReader(f)
    
    modified_content = [list(OUTPUT_FIELDS)]
    line_num = 1
    for line in reader:
        line_num += 1
        line["institution"] = "Bill & Melinda Gates Foundation"
        line["period"] = ""
        line["is_hybrid"] = ""
        line["euro"] = ""
        line["doi"] = doi_mappings.get(line["PublicationID"], "")
        _print("b", "--- Analysing line " + str(line_num) + " ---")
        # DOI check
        if len(line["doi"].strip()) == 0:
            delete_line(line, "Empty DOI")
            modified_content.append([line[field] for field in OUTPUT_FIELDS])
            continue
        # period field generation
        date_string = line["Date Payment Completed"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
        line["period"] = str(date.year)
        # euro field generation
        calculate_euro_value(line)
        modified_content.append([line[field] for field in OUTPUT_FIELDS])

    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, None, False, True)
        writer.write_rows(modified_content)

    print("\n\nPreprocessing finished, deleted articles overview:")

    sorted_reasons = sorted(DELETE_REASONS.items(), key=lambda x: x[1])
    sorted_reasons.reverse()
    for item in sorted_reasons:
        _print("r", item[0].ljust(72) + str(item[1]))
    _print("r,", "-------------------------------------------------")
    _print("r", "Total".ljust(72) + str(sum(DELETE_REASONS.values())))

    shutdown()

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))))
    import openapc_toolkit as oat
    main()
