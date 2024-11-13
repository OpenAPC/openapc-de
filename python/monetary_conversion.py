#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import datetime
import locale
from os import path
import re
import sys

import openapc_toolkit as oat

EXCHANGE_RATES = {
    "D": {},
    "M": {},
    "A": {} 
}

ARG_HELP_STRINGS = {
    "encoding": "The encoding of the source file.",
    "quotemask": "A quotemask to apply to the result file after the conversion " +
                 "has been performed. A quotemask is a string consisting " +
                 "only of the letters 't' and 'f' (true/false) and has " +
                 "the same length as there are columns in the (resulting) " +
                 "csv file. Only the columns where the index is 't' will be " +
                 "quoted.",
    "openapc_quote_rules": "Determines if the special openapc quote rules " +
                           "should be applied, meaning that the keywords " +
                           "NA, TRUE and FALSE will never be quoted. If in " +
                           "conflict with a quotemask, openapc_quote_rules " +
                           "will take precedence.",
    "locale": "Set the locale context used by the script. You might want to " +
              "set this if your system locale differs from the locale the " +
              "CSV file was created in (Example: Using en_US as your system " +
              "locale might become a problem if the file contains monetary " +
              "values with ',' as decimal mark character)",
}

YEARLY_RE = re.compile(r"^\d\d\d\d$")
MONTHLY_RE = re.compile(r"^\d{4}-[0-1]{1}\d$")
DAILY_RE = re.compile(r"^\d{4}-[0-1]{1}\d-[0-3]{1}\d$")

def get_frequency(date_string):
    date_string = date_string.strip()
    if YEARLY_RE.match(date_string):
        return "A"
    elif MONTHLY_RE.match(date_string):
        return "M"
    elif DAILY_RE.match(date_string):
        return "D"
    else:
        return None

# calculate a preliminary average for the current year
def _calulate_preliminary_annual_average(year, currency):
    if currency not in EXCHANGE_RATES["D"]:
        msg = 'No daily exchange rates found for currency "{}", querying ECB data warehouse...'
        oat.print_b(msg.format(currency))
        rates = oat.get_euro_exchange_rates(currency, "D")
        EXCHANGE_RATES["D"][currency] = rates
    rates = []
    for day, rate in EXCHANGE_RATES["D"][currency].items():
        if day.startswith(year):
            rates.append(float(rate))
    if rates:
        result = sum(rates)/len(rates)
        msg = "Calculated a preliminary average for year {} ({}) using {} daily values"
        oat.print_b(msg.format(year, result, len(rates)))
        return result
    else:
        msg = "Could not calculate a preliminary average for year {}"
        oat.print_r(msg.format(year))
        return None

def get_next_day(date_string):
    day = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    next_day = day + datetime.timedelta(days=1)
    return next_day.strftime("%Y-%m-%d")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    parser.add_argument("source_column", type=int)
    parser.add_argument("currency_column", type=int)
    parser.add_argument("period_column", type=int)
    parser.add_argument("target_column", type=int)
    parser.add_argument("-f", "--force_overwrite", action="store_true")
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-q", "--quotemask", help=ARG_HELP_STRINGS["quotemask"])
    parser.add_argument("-o", "--openapc_quote_rules", 
                        help=ARG_HELP_STRINGS["openapc_quote_rules"],
                        action="store_true", default=False)
    args = parser.parse_args()
    
    quote_rules = args.openapc_quote_rules

    mask = None
    if args.quotemask:
        reduced = args.quotemask.replace("f", "").replace("t", "")
        if len(reduced) > 0:
            print ("Error: A quotemask may only contain the letters 't' and"  +
                   "'f'!")
            sys.exit()
        mask = [True if x == "t" else False for x in args.quotemask]
    
    enc = None
    
    if args.encoding:
        try:
            codec = codecs.lookup(args.encoding)
            msg = "Encoding '{}' found in Python's codec collection as '{}'"
            oat.print_g(msg.format(args.encoding, codec.name))
            enc = args.encoding
        except LookupError:
            print ("Error: '" + args.encoding + "' not found Python's " +
                   "codec collection. Either look for a valid name here " +
                   "(https://docs.python.org/2/library/codecs.html#standard-" +
                   "encodings) or omit this argument to enable automated " +
                   "guessing.")
            sys.exit()
    
    if args.locale:
        norm = locale.normalize(args.locale)
        if norm != args.locale:
            msg = "locale '{}' not found, normalised to '{}'".format(
                  args.locale, norm)
            oat.print_y(msg)
        try:
            loc = locale.setlocale(locale.LC_ALL, norm)
            oat.print_g("Using locale " + loc)
        except locale.Error as loce:
            msg = "Setting locale to {} failed: {}".format(norm, loce.message)
            oat.print_r(msg)
            sys.exit()
        
    header, content = oat.get_csv_file_content(args.source_file, enc, True)
    fieldnames = header.pop()
    
    modified_content = []
    line_num = 0
    
    for column_type in ["source_column", "currency_column", "period_column", "target_column"]:
        index = getattr(args, column_type)
        msg = "Column {} ('{}') is the {}."
        oat.print_g(msg.format(index, fieldnames[index], column_type))
    
    start = input("\nStart conversion? (y/n):")
    while start not in ["y", "n"]:
        start = input("Please type 'y' or 'n':")
    if start == "n":
        sys.exit()
    
    for line in content:
        line_num += 1
        if not oat.has_value(line[args.source_column]):
            oat.print_y("WARNING: No source value found in line " + str(line_num) + ", skipping...")
            modified_content.append(line)
            continue
        monetary_value = None
        try: 
            monetary_value = locale.atof(line[args.source_column])
        except ValueError:
            msg = "WARNING: Could not extract a valid monetary value from source column in line {} ('{}'), skipping..."
            oat.print_y(msg.format(line_num, line[args.source_column]))
            modified_content.append(line)
            continue
        currency = line[args.currency_column]
        if currency == "EUR":
            msg = "WARNING: Currency in line {} is already EUR, skipping..."
            oat.print_y(msg.format(line_num))
            line[args.target_column] = line[args.source_column]
            modified_content.append(line)
            continue
        if not oat.has_value(currency):
            msg = "WARNING: Could not extract a valid currency indicator from currency column in line {} ('{}'), skipping..."
            oat.print_y(msg.format(line_num, currency))
            modified_content.append(line)
            continue
        period = line[args.period_column]
        frequency = get_frequency(period)
        if frequency is None:
            msg = "WARNING: Could not extract a valid date string (YYYY, YYYY-MM or YYYY-MM-DD) from period column in line {} ('{}'), skipping..."
            oat.print_y(msg.format(line_num, period))
            modified_content.append(line)
            continue
        if currency not in EXCHANGE_RATES[frequency]:
            msg = 'No exchange rates ({}) found for currency "{}", querying ECB data warehouse...'
            oat.print_b(msg.format(frequency, currency))
            rates = oat.get_euro_exchange_rates(currency, frequency)
            EXCHANGE_RATES[frequency][currency] = rates
        rate = EXCHANGE_RATES[frequency][currency].get(period)
        if rate is None and frequency == "A":
            rate = _calulate_preliminary_annual_average(period, currency)
            if rate:
                EXCHANGE_RATES[frequency][currency][period] = rate
        if rate is None:
            if frequency != "D":
                msg = "Error: No conversion rate found for currency {} for period {} (line {}), aborting..."
                oat.print_r(msg.format(currency, period, line_num))
                sys.exit()
            day_retries = 0
            while rate is None:
                msg = "Warning: No conversion rate found for currency {} for period {} (line {}), trying next day..."
                oat.print_y(msg.format(currency, period, line_num))
                period = get_next_day(period)
                rate = EXCHANGE_RATES[frequency][currency].get(period)
                day_retries += 1
                if day_retries > 5:
                    msg = "Error: Look-ahead limit for days exceeded, aborting..."
                    oat.print_r(msg)
                    sys.exit()

        euro_value = round(monetary_value/float(rate), 2)
        line[args.target_column] = str(euro_value)
        
        msg = "Line {}: {} exchange rate ({}) for date {} is {} -> {} / {} = {} EUR"
        msg = msg.format(line_num, currency, frequency, period, rate, monetary_value, rate, euro_value)
        oat.print_g(msg)
        
        modified_content.append(line)
    
    with open('out.csv', 'w') as out:
        writer = oat.OpenAPCUnicodeWriter(out, mask, quote_rules, True)
        writer.write_rows([fieldnames] + modified_content)

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))))
    import openapc_toolkit as oat
    main()
