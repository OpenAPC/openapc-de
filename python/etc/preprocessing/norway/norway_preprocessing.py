#!/usr/bin/python
# -*- coding: UTF-8 -*-

import argparse
from os import path
import sys

AVG_YEARLY_CONVERSION_RATES = {
    "2015": 0.1119,
    "2016": 0.1077
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file")
    args = parser.parse_args()

    result = oat.analyze_csv_file(args.source_file, 500)
    if result["success"]:
        csv_analysis = result["data"]
        print csv_analysis
    else:
        print result["error_msg"]
        sys.exit()

    dialect = csv_analysis.dialect
    csv_file = open(args.source_file, "r")
    reader = oat.UnicodeDictReader(csv_file, dialect=dialect)
    
    fieldnames = reader.reader.fieldnames
    modified_content = [fieldnames]
    
    for line in reader:
        rate = AVG_YEARLY_CONVERSION_RATES[line["Year"]]
        euro_value = float(line["APC in NOK"]) * rate
        line["APC in NOK"] = str(round(euro_value, 2))
        
        line_as_list = [line[field] for field in fieldnames]
        modified_content.append(line_as_list)
    csv_file.close()
    
    with open('out.csv', 'w') as out:
        quotemask = [False, True, True, True, True, True, False, True, False]
        writer = oat.OpenAPCUnicodeWriter(out, quotemask, False, True)
        writer.write_rows(modified_content)

if __name__ == '__main__' and __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__))))))
    import openapc_toolkit as oat
    main()
