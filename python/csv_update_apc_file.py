#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import codecs
import csv
import locale
import sys

import json

import openapc_toolkit as oat

ARG_HELP_STRINGS = {
    "original_file": "The csv file to update",
    "update_file": "The csv file to update the original file with",
    "encoding": "The encoding of the original file. Setting this argument will " +
                "disable automatic guessing of encoding.",
    "update_encoding": "The encoding of the update file.",
    "locale": "The locale to parse the original file with (important for monetary values)",
    "update_locale": "The locale to parse the update file with",
    "autocreate_mappings": "Create mappings for all matched column pairs without asking for confirmation",
    "grouping": "Use grouping (thousands separator) when updating euro field values"
}

class Change(object):
    
    def __init__(self, field_name, old_value, new_value, monetary=False):
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value
        self.monetary = monetary
        
    def __str__(self):
        return ' Column "{}", {} -> {}'.format(self.field_name, self.old_value, self.new_value)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("original_file", help=ARG_HELP_STRINGS["original_file"])
    parser.add_argument("update_file", help=ARG_HELP_STRINGS["update_file"])
    parser.add_argument("-e", "--encoding", help=ARG_HELP_STRINGS["encoding"])
    parser.add_argument("-eu", "--update_encoding", help=ARG_HELP_STRINGS["update_encoding"])
    parser.add_argument("-l", "--locale", help=ARG_HELP_STRINGS["locale"])
    parser.add_argument("-lu", "--update_locale", help=ARG_HELP_STRINGS["update_locale"])
    parser.add_argument("-a", "--autocreate_mappings", action="store_true", help=ARG_HELP_STRINGS["autocreate_mappings"])
    parser.add_argument("-g", "--grouping", action="store_true", help=ARG_HELP_STRINGS["grouping"])
    
    args = parser.parse_args()
    
    params = {
        "original": {
            "file": args.original_file,
            "encoding": args.encoding,
            "locale": args.locale,
            "csv_analysis": None,
            "fieldnames": None,
            "doi_field": None,
            "euro_field": None,
            "mappings": []
        },
        "update": {
            "file": args.update_file,
            "encoding": args.update_encoding,
            "locale": args.update_locale,
            "csv_analysis": None,
            "fieldnames": None,
            "doi_field": None,
            "euro_field": None,
            "mappings": []
        }
    }
    
    def field_mapped(file_type, field_name):
        if field_name == params[file_type]["euro_field"]:
            return True
        if field_name == params[file_type]["doi_field"]:
            return True
        if field_name in params[file_type]["mappings"]:
            return True
        return False
    
    for file_type in params.keys():
        msg = "*** Performing analysis for {} file ***"
        oat.print_b(msg.format(file_type))
        encoding = params[file_type]["encoding"]
        if encoding is not None:
            try:
                codec = codecs.lookup(encoding)
                msg = "Encoding '{}' found in Python's codec collection as '{}'"
                print(msg.format(encoding, codec.name))
                params[file_type]["encoding"] = encoding
            except LookupError:
                print ("Error: '" + encoding + "' not found Python's " +
                       "codec collection. Either look for a valid name here " +
                       "(https://docs.python.org/2/library/codecs.html#standard-" +
                       "encodings) or omit this argument to enable automated " +
                       "guessing.")
                sys.exit()

        loc = params[file_type]["locale"]
        if loc is not None:
            norm = locale.normalize(loc)
            if norm != loc:
                msg = "locale '{}' not found, normalised to '{}'".format(loc, norm)
                oat.print_y(msg)
                params[file_type]["locale"] = norm

        csv_analysis = oat.analyze_csv_file(params[file_type]["file"], enc=params[file_type]["encoding"])
        if not csv_analysis["success"]:
            oat.print_r(csv_analysis["error_msg"])
            sys.exit()
        params[file_type]["csv_analysis"] = csv_analysis["data"]
        print(params[file_type]["csv_analysis"])
        
        if params[file_type]["encoding"] is None:
            guessed_enc = params[file_type]["csv_analysis"].enc
            params[file_type]["encoding"] = guessed_enc

        locale_name = "default locale"
        if params[file_type]["locale"] is not None:
            locale_name = "locale " + params[file_type]["locale"]
        msg = "{} file will be opened with encoding {} and {}"
        oat.print_g(msg.format(file_type, params[file_type]["encoding"], locale_name))
        
        with open(params[file_type]["file"], "r", encoding=params[file_type]["encoding"]) as f:
            reader = csv.DictReader(f, dialect=params[file_type]["csv_analysis"].dialect)
            params[file_type]["fieldnames"] = list(reader.fieldnames)
            for index, name in enumerate(params[file_type]["fieldnames"]):
                field_type = oat.get_column_type_from_whitelist(name)
                found = False
                if field_type == "doi":
                    params[file_type]["doi_field"] = name
                    found = True
                elif field_type == "euro":
                    params[file_type]["euro_field"] = name
                    found = True
                if found:
                    msg = '{} file: Found {} column at index {} ("{}")'
                    msg = msg.format(file_type, field_type, index, name)
                    oat.print_b(msg)
            for field_type in ["doi_field", "euro_field"]:
                if params[file_type][field_type] is None:
                    msg = "Error: No {} found in {} file"
                    oat.print_r(msg.format(field_type, file_type))
                    sys.exit()
    
    for orig_index, orig_field in enumerate(params["original"]["fieldnames"]):
        if field_mapped("original", orig_field):
            continue
        norm_orig_field = orig_field.lower().strip()
        for update_index, update_field in enumerate(params["update"]["fieldnames"]):
            if field_mapped("update", update_field):
                continue
            norm_update_field = update_field.lower().strip()
            if norm_orig_field == norm_update_field:
                if args.autocreate_mappings:
                    params["original"]["mappings"].append(orig_field)
                    params["update"]["mappings"].append(update_field)
                    msg = 'Auto-created mapping "{}" (update file, index {}) -> "{}" (original file, index {})'
                    oat.print_b(msg.format(update_field, update_index, orig_field, orig_index))
                else:
                    msg = 'Possible mapping found: "{}" (update file, index {}) -> "{}" (original file, index {}). Create mapping (y/n)?'
                    msg = msg.format(update_field, update_index, orig_field, orig_index)
                    create = input(msg)
                    while create not in ["y", "n"]:
                        create = input("Please type 'y' or 'n':")
                    if create == "y":
                        params["original"]["mappings"].append(orig_field)
                        params["update"]["mappings"].append(update_field)
                    
    update_mappings = {}
    with open(params["update"]["file"], "r", encoding=params["update"]["encoding"]) as f:
        doi_field = params["update"]["doi_field"]
        euro_field = params["update"]["euro_field"]
        reader = csv.DictReader(f, dialect=params["update"]["csv_analysis"].dialect)
        locale.setlocale(locale.LC_ALL, params["update"]["locale"])
        for line in reader:
            doi = oat.get_normalised_DOI(line[doi_field])
            if doi is None:
                msg = 'Warning: Empty or invalid DOI in update file (line {}): "{}"'
                oat.print_y(msg.format(reader.line_num, line[doi_field]))
                continue
            if doi in update_mappings:
                msg = "Error: Duplicate doi in update file ({})".format(line[doi_field])
                oat.print_r(msg)
                sys.exit()
            update_mappings[doi] = {}
            euro_value = locale.atof(line[euro_field])
            orig_euro_field = params["original"]["euro_field"]
            update_mappings[doi][orig_euro_field] = euro_value
            for index, update_field_name in enumerate(params["update"]["mappings"]):
                orig_field_name = params["original"]["mappings"][index]
                update_mappings[doi][orig_field_name] = line[update_field_name]
            
    #print(json.dumps(update_mappings, sort_keys=False, indent=4))
    
    modified_content = []
    fieldnames = None
    with open(params["original"]["file"], "r", encoding=params["original"]["encoding"]) as f:
        doi_field = params["original"]["doi_field"]
        euro_field = params["original"]["euro_field"]
        reader = csv.DictReader(f, dialect=params["original"]["csv_analysis"].dialect)
        fieldnames = list(reader.fieldnames)
        locale.setlocale(locale.LC_ALL, params["original"]["locale"])
        for line in reader:
            doi = oat.get_normalised_DOI(line[doi_field])
            if doi not in update_mappings:
                msg = "line {}: DOI {} not found in update file!"
                oat.print_r(msg.format(reader.line_num, doi))
                continue
            changes = []
            old_euro_value = locale.atof(line[euro_field])
            new_euro_value = update_mappings[doi][euro_field]
            if old_euro_value != new_euro_value:
                changes.append(Change(euro_field, old_euro_value, new_euro_value, monetary=True))
            for field in update_mappings[doi].keys():
                if field == euro_field:
                    continue
                if line[field] != update_mappings[doi][field]:
                    changes.append(Change(field, line[field], update_mappings[doi][field]))
            if not changes:
                msg = "line {}: DOI {} found in update file, but nothing changed."
                oat.print_g(msg.format(reader.line_num, doi))
            else:
                msg = "line {}: DOI {} found in update file with the following updates:"
                oat.print_y(msg.format(reader.line_num, doi))
                for change in changes:
                    oat.print_y(str(change))
                    if change.monetary:
                        line[change.field_name] = locale.currency(change.new_value,symbol=False, grouping=args.grouping)
                    else:
                        line[change.field_name] = change.new_value
            del(update_mappings[doi])
            modified_content.append(line)
        if update_mappings:
            oat.print_y("{} entries in update file not contained in original file:".format(len(update_mappings)))
        for doi, changes in update_mappings.items():
            oat.print_y(doi)
            new_line = changes
            new_line[params["original"]["doi_field"]] = doi
            formatted_euro = locale.currency(new_line[params["original"]["euro_field"]], symbol=False, grouping=args.grouping)
            new_line[params["original"]["euro_field"]] = formatted_euro
            modified_content.append(new_line)
    
    with open("out.csv", "w", encoding=params["original"]["encoding"]) as out:
        writer = csv.DictWriter(out, fieldnames, dialect=params["original"]["csv_analysis"].dialect)
        writer.writeheader()
        for line in modified_content:
            writer.writerow(line)

if __name__ == '__main__':
    main()
