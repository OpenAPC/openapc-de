#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
import codecs
import datetime
import json
from os import path
import re
import sys
import urllib2

ARG_HELP_STRINGS = {
    "source_file": "The jisc csv file",
    "fixer_cache_file": "An optional cache file for fixer.io results",
    "no_decorations": "Do not use ANSI coded colors in console output"
}

FIELDNAMES = [
    u"APC paid (actual currency) including VAT if charged",
    u"APC paid (£) including VAT (calculated)",
    u"APC paid (£) including VAT if charged",
    u"Currency of APC",
    u"DOI",
    u"Date of APC payment",
    u"Date of initial application by author",
    u"ISSN0",
    u"Institution",
    u"Journal",
    u"Licence",
    u"PubMed Central (PMC) ID",
    u"PubMed ID",
    u"Publisher",
    u"TCO year",
    u"Type of publication",
    u"Drop?",
    u"Year of publication",
    u"period",
    u"is_hybrid",
    u"euro"
]

PUBLICATION_TYPES_BL = [
    u"Book",
    u"Book chapter",
    u"Book edited",
    u"Conference Paper/Proceeding/Abstract",
    u"Letter",
    u"Monograph"
]

DATE_DAY_RE = re.compile("(?P<year>[0-9]{4})-?(?P<month>[0-9]{2})?-?(?P<day>[0-9]{2})?")

PERIOD_FIELD_SOURCE = [
    u"Date of APC payment",
    u"Year of publication",
    u"Date of initial application by author",
    u"TCO year"
]

AVG_YEARLY_CONVERSION_RATES = {
    "AUD": {"2015": 1.4777},
    "GBP": {"2005": 0.68380, "2009": 0.89094, "2012": 0.81087, "2013": 0.84926,
            "2014": 0.80612, "2015": 0.72584, "2016": 0.81948},
    "USD": {"2005": 1.2441, "2013": 1.3281, "2014": 1.3285, "2015": 1.1095,
            "2016": 1.1069},
    "CHF": {"2013": 1.2311, "2014": 1.2146, "2015": 1.0679, "2016": 1.0902}
}

FIXER_CACHE = {}
FIXER_CACHE_FILE = None

DELETE_REASONS = {}

NO_DECORATIONS = False

def delete_line(line_dict, reason):
    _print("r", "   - " + reason + ", line deleted")
    if reason not in DELETE_REASONS:
        DELETE_REASONS[reason] = 1
    else:
        DELETE_REASONS[reason] += 1
    for key in line_dict:
        line_dict[key] = u""

def line_as_list(line_dict):
    return [line_dict[field] for field in FIELDNAMES]

def is_money_value(string):
    try:
        number = float(string)
        return number > 0
    except ValueError:
        return False

def is_valid_date(date_match_obj):
    gd = date_match_obj.groupdict()
    if gd["year"] is None or gd["month"] is None or gd["day"] is None:
        return False
    try:
        datetime.date(int(gd["year"]), int(gd["month"]), int(gd["day"]))
        return True
    except ValueError:
        return False

def shutdown():
    _print("r", "Updating fixer cache...")
    with open(FIXER_CACHE_FILE, "w") as f:
        f.write(json.dumps(FIXER_CACHE, sort_keys=True, indent=4, separators=(',', ': ')))
        f.flush()
    _print("r", "Done.")
    sys.exit()
    
def _print(color, s):
    if color in ["r", "y", "g", "b"] and not NO_DECORATIONS:
        getattr(oat, "print_" + color)(s)
    else:
        print s
        

def query_fixer(currency, date):
    try:
        rate = FIXER_CACHE[currency][date]
        _print("y", "     [fixer.io: Cached value used]")
        return rate
    except KeyError:
        pass
    url = 'https://api.fixer.io/' + date
    req = urllib2.Request(url, None)
    try:
        response = urllib2.urlopen(req)
        content = json.loads(response.read())
        sent_date = datetime.datetime.strptime(date, "%Y-%m-%d")
        content_date = datetime.datetime.strptime(content[u"date"], "%Y-%m-%d")
        delta = sent_date - content_date
        if delta.days > 4 or content[u"base"] != "EUR":
            _print("r", "ERROR in fixer response: date (> 4 day) or base currency mismatch: " + url + " -> " + str(content))
            shutdown()
        if currency not in content["rates"]:
            _print("r", "ERROR in fixer response: requested currency '" + currency + "'not in rates: " + url + " -> " + str(content))
            shutdown()
        rate = content["rates"][currency]
        if currency not in FIXER_CACHE:
            FIXER_CACHE[currency] = {}
        FIXER_CACHE[currency][date] = rate
        return rate
    except urllib2.HTTPError as httpe:
        _print("r", "HTTPError while querying fixer.io: " + httpe.reason)
        shutdown()
    except urllib2.URLError as urle:
        _print("r", "URLError while querying fixer.io: " + urle.reason)
        shutdown()

def main():
    global FIXER_CACHE, FIXER_CACHE_FILE, NO_DECORATIONS
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file", help=ARG_HELP_STRINGS["source_file"])
    parser.add_argument("-c", "--fixer_cache_file", help=ARG_HELP_STRINGS["fixer_cache_file"], default="_fixer_cache.json")
    parser.add_argument("-n", "--no-decorations", help=ARG_HELP_STRINGS["no_decorations"], action="store_true")

    args = parser.parse_args()

    NO_DECORATIONS = args.no_decorations
    FIXER_CACHE_FILE = args.fixer_cache_file

    if path.isfile(args.fixer_cache_file):
        with open(FIXER_CACHE_FILE, "r") as f:
            try:
                FIXER_CACHE = json.loads(f.read())
            except ValueError:
                _print("r", "Could not decode a cache structure from " + FIXER_CACHE_FILE + ", starting with an empty cache.")

    result = oat.analyze_csv_file(args.source_file, 500)
    if result["success"]:
        csv_analysis = result["data"]
        print csv_analysis
    else:
        print result["error_msg"]
        shutdown()

    dialect = csv_analysis.dialect
    csv_file = open(args.source_file, "r")
    reader = oat.UnicodeDictReader(csv_file, dialect=dialect)

    modified_content = [FIELDNAMES]
    for line in reader:
        line[u"period"] = ""
        line[u"is_hybrid"] = ""
        line[u"euro"] = ""
        _print("b", "--- Analysing line " + str(reader.reader.line_num) + " ---")
        # DOI checking
        if len(line[u"DOI"].strip()) == 0:
            delete_line(line, u"Empty DOI")
            modified_content.append(line_as_list(line))
            continue
        # Drop checking
        if line[u"Drop?"] == u"1":
            delete_line(line, u"Drop mark found")
            modified_content.append(line_as_list(line))
            continue
        # Publication blacklist checking
        pub_type = line[u"Type of publication"]
        if pub_type in PUBLICATION_TYPES_BL:
            delete_line(line, "Blacklisted pub type ('" + pub_type + "')")
            modified_content.append(line_as_list(line))
            continue
        # period field generation
        for source_field in PERIOD_FIELD_SOURCE:
            content = line[source_field].strip()
            match = DATE_DAY_RE.match(content)
            if match:
                year = match.groupdict()["year"]
                line[u"period"] = year
                msg = "   - Created period field ('{}') by parsing value '{}' in column '{}'".format(year, content, source_field)
                _print("g", msg)
                break
        else:
            _print("r", "ERROR: period column could not be created for line:\n" + str(line))
            shutdown()
        # euro field generation
        apc_orig = line[u"APC paid (actual currency) including VAT if charged"]
        apc_pound = ""
        field_used_for_pound_value = ""
        for field in [u"APC paid (£) including VAT (calculated)", u"APC paid (£) including VAT if charged"]:
            if is_money_value(line[field]):
                apc_pound = line[field]
                field_used_for_pound_value = field
                break
        payment_date = line[u"Date of APC payment"]
        date_match = DATE_DAY_RE.match(payment_date)
        if is_money_value(apc_orig):
            currency = line[u"Currency of APC"].strip()
            if currency == u"EUR":
                line[u"euro"] = apc_orig
                msg = "   - Created euro field ('{}') by using the value in 'APC paid (actual currency) including VAT if charged' directly since the currency is EUR"
                _print("g", msg.format(apc_orig))
            elif len(currency) == 3:
                if date_match and is_valid_date(date_match):
                    rate = query_fixer(currency, payment_date)
                    euro_value = round(float(apc_orig) / rate, 2)
                    line[u"euro"] = str(euro_value)
                    msg = "   - Created euro field ('{}') by dividing the value in 'APC paid (actual currency) including VAT if charged' ({}) by {} (EUR -> {} conversion rate on {}) [fixer.io]"
                    msg = msg.format(euro_value, apc_orig, rate, currency, payment_date)
                    _print("g", msg)
                else:
                    year = line[u"period"]
                    if int(year) >= datetime.datetime.now().year:
                        del_msg = "period ({}) too recent to determine average yearly conversion rate".format(year)
                        delete_line(line, del_msg)
                        modified_content.append(line_as_list(line))
                        continue
                    try:
                        rate = AVG_YEARLY_CONVERSION_RATES[currency][year]
                    except KeyError:
                        _print("r", "KeyError: An average yearly conversion rate is missing (" + currency + ", " + year + ")")
                        shutdown()
                    euro_value = round(float(apc_orig) / rate, 2)
                    line[u"euro"] = str(euro_value)
                    msg = "   - Created euro field ('{}') by dividing the value in 'APC paid (actual currency) including VAT if charged' ({}) by {} (avg EUR -> {} conversion rate in {}) [ECB]"
                    msg = msg.format(euro_value, apc_orig, rate, currency, year)
                    _print("g", msg)
        if line[u"euro"] == "" and is_money_value(apc_pound):
            if date_match and is_valid_date(date_match):
                rate = query_fixer("GBP", payment_date)
                euro_value = round(float(apc_pound) / rate, 2)
                line[u"euro"] = str(euro_value)
                msg = u"   - Created euro field ('{}') by dividing the value in '{}' ({}) by {} (EUR -> GBP conversion rate on {}) [fixer.io]"
                msg = msg.format(euro_value, field_used_for_pound_value, apc_pound, rate, payment_date)
                _print("g", msg)
            else:
                year = line[u"period"]
                if int(year) >= datetime.datetime.now().year:
                    del_msg = "period ({}) too recent to determine average yearly conversion rate".format(year)
                    delete_line(line, del_msg)
                    modified_content.append(line_as_list(line))
                    continue
                try:
                    rate = AVG_YEARLY_CONVERSION_RATES["GBP"][year]
                except KeyError:
                    _print("r", "KeyError: An average yearly conversion rate is missing (GBP, " + year + ")")
                    shutdown()
                euro_value = round(float(apc_pound) / rate, 2)
                line[u"euro"] = str(euro_value)
                msg = u"   - Created euro field ('{}') by dividing the value in '{}' ({}) by {} (avg EUR -> GBP conversion rate in {}) [ECB]"
                msg = msg.format(euro_value, field_used_for_pound_value, apc_pound, rate, year)
                _print("g", msg)
        if line[u"euro"] == "":
            delete_line(line, "Unable to properly calculate a converted euro value")
            modified_content.append(line_as_list(line))
            continue
        modified_content.append(line_as_list(line))
    csv_file.close()

    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, None, False, True)
        writer.write_rows(modified_content)

    print "\n\nPreprocessing finished, deleted articles overview:"

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
    utf8_writer = codecs.getwriter('utf8')
    sys.stdout = utf8_writer(sys.stdout)
    main()
