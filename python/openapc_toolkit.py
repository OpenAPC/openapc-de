#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import csv
from collections import OrderedDict
import datetime
from html import unescape
from http.client import RemoteDisconnected
import json
import locale
import logging
from logging.handlers import MemoryHandler
import openpyxl
import os
import re
from shutil import copyfileobj, copy2
import sys
from urllib.parse import quote_plus, urlencode
from urllib.request import build_opener, urlopen, urlretrieve, HTTPErrorProcessor, Request
from urllib.error import HTTPError, URLError
from time import sleep
import requests
import xml.etree.ElementTree as ET
import zipfile

import mappings

try:
    import chardet
except ImportError:
    chardet = None
    print("WARNING: 3rd party module 'chardet' not found - character " +
          "encoding guessing will not work")
try:
    import Levenshtein
except ImportError:
    chardet = None
    print("WARNING: 3rd party module 'Levenshtein' not found - title " +
          "search in Crossref will not work")

# Identifying User Agent header for metadata API requests
USER_AGENT = ("OpenAPC Toolkit (https://github.com/OpenAPC/openapc-de/blob/master/python/openapc_toolkit.py;"+
              " mailto:openapc@uni-bielefeld.de)")

# Optional token for Crossref Metadata Plus Service (loaded lazily)
CROSSREF_PLUS_TOKEN = 'unset'

# regex for detecing DOIs
DOI_RE = re.compile(r"^(((https?://)?(dx.)?doi.org/)|(doi:))?(?P<doi>10\.[0-9]+(\.[0-9]+)*\/\S+)", re.IGNORECASE)
# regex for detecting shortDOIs
SHORTDOI_RE = re.compile(r"^(https?://)?(dx.)?doi.org/(?P<shortdoi>[a-z0-9]+)$", re.IGNORECASE)

ISSN_RE = re.compile(r"^(?P<first_part>\d{4})\-(?P<second_part>\d{3})(?P<check_digit>[\dxX])$")

# regex for ROR IDs, see also https://ror.readme.io/docs/ror-identifier-pattern
ROR_RE = re.compile(r"^((https?://)?ror.org/)?0[a-z0-9]{6}[0-9]{2}$")


OAI_COLLECTION_CONTENT = OrderedDict([
    ("institution", "intact:institution"),
    ("period", "intact:period"),
    ("euro", "intact:euro"),
    ("doi", "intact:id_number[@type='doi']"),
    ("is_hybrid", "intact:is_hybrid"),
    ("publisher", "intact:publisher"),
    ("journal_full_title", "intact:journal_full_title"),
    ("issn", "intact:issn"),
    ("license_ref", "intact:licence"),
    ("pmid", "intact:id_number[@type='pubmed']"),
    ("url", None),
    ("local_id", "intact:id_number[@type='local']")
])

MESSAGES = {
    "num_columns": "Syntax: The number of values in this row (%s) " +
                   "differs from the number of columns (%s). Line left " +
                   "unchanged, the resulting CSV file will not be valid.",
    "locale": "Error: Could not process the monetary value '%s' in " +
              "column %s. Usually this happens due to one of two reasons:\n1) " +
              "The value does not represent a number.\n2) The value " +
              "represents a number, but its format differs from your " +
              "current system locale - the most common source of error " +
              "is the decimal mark (1234.56 vs 1234,56). Try using " +
              "another locale with the -l option.",
    "unify": "Normalisation: Crossref-based {} changed from '{}' to '{}' " +
             "to maintain consistency.",
    "digits_error": "Monetary value %s has more than 2 digits after " +
                    "the decimal point. If this is just a formatting issue (from automated " +
                    "conversion for example) you may call the enrichment script with the -r " +
                    "option to round such values to 2 digits automatically.",
    "digits_norm": "Normalisation: Monetary value %s rounded to 2 digits after " +
                   "decimal mark (%s -> %s)",
    "doi_norm": "Normalisation: DOI '{}' normalised to pure form ({}).",
    "issn_hyphen_fix": "Normalisation: Added hyphen to %s value (%s -> %s)",
    "period_format": "Normalisation: Date format in period column changed to year only (%s -> %s)",
    "unknown_hybrid_identifier": "Unknown identifier in 'is_hybrid' column ('%s').",
    "hybrid_normalisation": "Normalisation: is_hybrid status changed from '%s' to '%s'.",
    "no_hybrid_identifier": "Empty value in 'is_hybrid' column.",
    "empty_row": "Row is empty."
}

QUOTEMASKS = {
    "journal-article": [
        True,
        False,
        False,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True
    ],
    "contracts": [
        True,
        True,
        True,
        True,
        False,
        False,
        True,
        False,
        True,
    ],
    "additional_costs": [
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ],
    "journal-article_transagree": [
        True,
        False,
        False,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True
    ],
    "oapk_output": [
        True,
        True,
        False,
        False,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        True
    ]
}

COLUMN_SCHEMAS = {
    "journal-article": [
        "institution",
        "period",
        "euro",
        "doi",
        "is_hybrid",
        "publisher",
        "journal_full_title",
        "issn",
        "issn_print",
        "issn_electronic",
        "issn_l",
        "license_ref",
        "indexed_in_crossref",
        "pmid",
        "pmcid",
        "ut",
        "url",
        "doaj"
    ],
    "journal-article_transagree": [
        "institution",
        "period",
        "euro",
        "doi",
        "is_hybrid",
        "opt_out",
        "publisher",
        "journal_full_title",
        "issn",
        "issn_print",
        "issn_electronic",
        "issn_l",
        "license_ref",
        "indexed_in_crossref",
        "pmid",
        "pmcid",
        "ut",
        "url",
        "doaj",
        "agreement",
        "group_id"
    ],
    "book": [
        "institution",
        "period",
        "euro",
        "doi",
        "backlist_oa",
        "publisher",
        "book_title",
        "isbn",
        "isbn_print",
        "isbn_electronic",
        "license_ref",
        "indexed_in_crossref",
        "doab"
    ],
    "additional_costs": [
        "doi",
        "colour charge",
        "cover charge",
        "page charge",
        "permission",
        "reprint",
        "submission fee",
        "payment fee",
        "other"
    ],
    "contracts": [
        "institution",
        "consortium",
        "contract_name",
        "identifier",
        "period_from",
        "period_to",
        "cost_type",
        "euro",
        "group_id"
    ]
}

# short-term cache for annual exchange rates
EXCHANGE_RATES = {}

INSTITUTIONS_FILE = "../data/institutions.csv"
INSTITUTIONS_PATH_MAP = None
INSTITUTIONS_NAME_MAP = None

CONTRACTS_LOOKUP = None
ESAC_HANDLING = None

class OpenAPCUnicodeWriter(object):
    """
    A customized CSV Writer.

    A custom CSV writer. Encodes output in Unicode and can be configured to
    follow the open APC CSV quotation standards. A quote mask can also be
    provided to enable or disable value quotation in distinct CSV columns.

    Attributes:
        quotemask: A quotemask is a list of boolean values which should have
                   the same length as the number of columns in the csv file.
                   On writing, the truth values in the codemask will determine
                   if the values in the according column will be quoted. If no
                   quotemask is provided, every field will be quoted.
        openapc_quote_rules: Determines if the special openapc quote rules
                             should be applied, meaning that the keywords
                             NA, TRUE and FALSE will never be quoted. This
                             always takes precedence over a quotemask.
        has_header: Determines if the csv file has a header. If that's the case,
                    The values in the first row will all be quoted regardless
                    of any quotemask.
        minimal_quotes: Quote values containing a comma even if a quotemask
                        is False for that column (Might produce a malformed
                        csv file otherwise).
    """

    def __init__(self, f, quotemask=None, openapc_quote_rules=True,
                 has_header=True, minimal_quotes=True):
        self.outfile = f
        self.quotemask = quotemask
        self.openapc_quote_rules = openapc_quote_rules
        self.has_header = has_header
        self.minimal_quotes = minimal_quotes

    def _prepare_row(self, row, use_quotemask):
        for index in range(len(row)):
            if self.openapc_quote_rules and row[index] in ["TRUE", "FALSE", "NA"]:
                # Never quote these keywords
                continue
            if not use_quotemask or not self.quotemask:
                # Always quote without a quotemask
                row[index] = row[index].replace('"', '""')
                row[index] = '"' + row[index] + '"'
                continue
            if index < len(self.quotemask):
                if self.quotemask[index] or "," in row[index] and self.minimal_quotes:
                    row[index] = row[index].replace('"', '""')
                    row[index] = '"' + row[index] + '"'
        return row

    def _write_row(self, row):
        line = ",".join(row) + "\n"
        self.outfile.write(line)

    def write_rows(self, rows):
        if self.has_header:
            self._write_row(self._prepare_row(rows.pop(0), False))
        for row in rows:
            self._write_row(self._prepare_row(row, True))

class CSVColumn(object):

    MANDATORY = {"text": "mandatory", "color": "green"}
    BACKUP = {"text": "backup", "color": "blue"}
    RECOMMENDED = {"text": "recommended", "color": "cyan"}
    ADDITIONAL_COSTS = {"text": "additional_costs", "color": "magenta"}
    DEFAULT_FALSE = {"text": "defaulting to FALSE", "color": "green"}
    DEFAULT_NA = {"text": "defaulting to NA", "color": "green"}
    NONE = {"text": "not required", "color": "yellow"}

    OW_ALWAYS = 0
    OW_ASK = 1
    OW_NEVER = 2

    _OW_MSG = (u"\033[91mConflict\033[0m: Existing non-NA value " +
               u"\033[93m{ov}\033[0m in column \033[93m{name}\033[0m is to be " +
               u"replaced by new value \033[93m{nv}\033[0m.\nAllow overwrite?\n" +
               u"1) Yes\n2) Yes, and always replace \033[93m{ov}\033[0m by "+
               "\033[93m{nv}\033[0m in this column\n3) Yes, and always " +
               "overwrite in this column\n4) No\n5) No, and never replace " +
               "\033[93m{ov}\033[0m by \033[93m{nv}\033[0m in this " +
               "column\n6) No, and never overwrite in this column\n>")

    def __init__(self, column_type, requirement=None, index=None, column_name="", overwrite=OW_ASK):
        self.column_type = column_type
        if requirement is None:
            self.requirement = {
                "articles": CSVColumn.NONE,
                "books": CSVColumn.NONE
            }
        else:
            self.requirement = requirement
        self.index = index
        self.column_name = column_name
        self.overwrite = overwrite
        self.overwrite_whitelist = {}
        self.overwrite_blacklist = {}

    def get_req_description(self, colored=True):
        requirements = []
        for pub_type, required in self.requirement.items():
            if colored:
                requirement = colorize(required["text"] + " for " + pub_type, required["color"])
            else:
                requirement = required["text"] + " for " + pub_type
            requirements.append(requirement)
        return ", ".join(requirements)

    def check_overwrite(self, old_value, new_value):
        if old_value == new_value:
            return old_value
        # Priority: Empty or NA values will always be overwritten.
        if old_value == "NA":
            return new_value
        if old_value.strip() == "":
            return new_value
        # Do not replace an existing old value with NA
        if new_value == "NA":
            return old_value
        if self.overwrite == CSVColumn.OW_ALWAYS:
            return new_value
        if self.overwrite == CSVColumn.OW_NEVER:
            return old_value
        if old_value in self.overwrite_blacklist:
            if self.overwrite_blacklist[old_value] == new_value:
                return old_value
        if old_value in self.overwrite_whitelist:
            return new_value
        msg = CSVColumn._OW_MSG.format(ov=old_value, name=self.column_name,
                                       nv=new_value)
        ret = input(msg)
        while ret not in ["1", "2", "3", "4", "5", "6"]:
            ret = input("Please select a number between 1 and 5:")
        if ret == "1":
            return new_value
        if ret == "2":
            self.overwrite_whitelist[old_value] = new_value
            return new_value
        if ret == "3":
            self.overwrite = CSVColumn.OW_ALWAYS
            return new_value
        if ret == "4":
            return old_value
        if ret == "5":
            self.overwrite_blacklist[old_value] = new_value
            return old_value
        if ret == "6":
            self.overwrite = CSVColumn.OW_NEVER
            return old_value

class TempFileHandling(object):
    """
    Handle temporary files which need to be updated in regular intervals
    """

    MSGS = {
        "not_found": '{} offline copy not found at "{}", downloading ' +
                      'a fresh copy...',
        "forced": 'Forced download of a fresh {} offline copy to "{}"...',
        "max_mdays": 'Your {} offline copy at "{}" is {} days old. ' +
                     'The limit is {} days, downloading a fresh copy...',
        "backup": 'The previous offline copy was backed up as "{}".',
        "no_url": "Either a url or a path to a local file containing " +
                  "an url must be provided",
        "local_file": "Could not access local path '{}'. This " +
                      "file must exist and contain the URL to " +
                      "the download file '{}{}'"
    }

    def _unzip(self, **kwargs):
        with zipfile.ZipFile(self.file_path, "r") as zip_file:
            zip_file.extractall(self.temp_file_dir)

    def _excel_to_csv(self, **kwargs):
        excel = openpyxl.load_workbook(self.file_path)
        sheet = excel.active # only works for excel files with one sheet
        target_name = os.path.join(self.temp_file_dir, self.file_name + ".csv")
        skip_lines = kwargs.get("skip_lines", 0)
        row_num = -1
        with open(target_name, "w") as out:
            writer = csv.writer(out)
            for row in sheet.rows:
                row_num += 1
                if row_num < skip_lines:
                    continue
                writer.writerow([cell.value for cell in row])

    DECOMPRESSION_OPTIONS = {
        "zip": "_unzip",
        "excel_to_csv": "_excel_to_csv"
    }

    def __init__(self, file_name, file_ext, url=None, url_local_file=None, temp_file_dir="tempfiles", max_mdays=7):
        if url is None and url_local_file is None:
            raise Exception(self.MSGS["no_url"])
        self.file_name = file_name
        self.file_ext = file_ext
        self.temp_file_dir = temp_file_dir
        self.max_mdays = max_mdays
        self.file_suffix = "." + file_ext if file_ext != "" else ""
        self.file_path = os.path.join(temp_file_dir, file_name + self.file_suffix)
        if url is not None:
            self.url = url
        else:
            self.set_url_from_local_file(url_local_file)
        if not os.path.isdir(temp_file_dir):
            os.mkdir(temp_file_dir)

    def set_url_from_local_file(self, url_local_file):
        if not os.path.isfile(url_local_file):
            msg = self.MSGS["local_file"].format(url_local_file,
                                                 self.file_name,
                                                 self.file_suffix)
            raise Exception(msg)
        with open(url_local_file, "r") as handle:
            self.url = handle.read()

    def get_file_mdate_days(self):
        if not os.path.isfile(self.file_path):
            return None
        now = datetime.datetime.now()
        then = datetime.datetime.fromtimestamp(os.path.getmtime(self.file_path))
        timediff = now - then
        return timediff.days

    def prepare_file(self, force_update=False, make_backup=False, verbose=False, decompress=None, decompress_kwargs={}):
        """
        Return a path to the temporary file, downloading a fresh copy
        and creating a backup if necessary. 
        """
        if decompress is not None and decompress not in self.DECOMPRESSION_OPTIONS:
            error_msg = "{} is no valid decompression option. Available choices: {}"
            raise Exception(error_msg.format(decompress, ", ".join(self.DECOMPRESSION_OPTIONS.keys())))
        file_mdays = self.get_file_mdate_days()
        if file_mdays is not None:
            if not force_update:
                if file_mdays <= self.max_mdays:
                    return self.file_path
                elif verbose:
                    msg = self.MSGS["max_mdays"]
                    print_c(msg.format(self.file_name, self.file_path, file_mdays, self.max_mdays))
            elif verbose:
                msg = self.MSGS["forced"]
                print_c(msg.format(self.file_name, self.file_path))
        elif verbose:
            msg = self.MSGS["not_found"]
            print_c(msg.format(self.file_name, self.file_path))
        backup_msg = None
        if make_backup and file_mdays is not None:
            then = datetime.datetime.fromtimestamp(os.path.getmtime(self.file_path))
            mdate = then.strftime("%Y_%m_%d_%H_%M_%S")
            backup_target = os.path.join(self.temp_file_dir, self.file_name + "_" + mdate + self.file_suffix)
            if verbose:
                backup_msg = self.MSGS['backup'].format(backup_target)
            copy2(self.file_path, backup_target)
        request = Request(self.url)
        request.add_header("User-Agent", USER_AGENT)
        with urlopen(request) as source:
            with open(self.file_path, "wb") as dest:
                copyfileobj(source, dest)
        if decompress is not None:
            if verbose:
                print_c("Extracting/transforming file ({})...".format(decompress))
            decompression_func = getattr(self, self.DECOMPRESSION_OPTIONS[decompress])
            decompression_func(**decompress_kwargs)
        if verbose:
            print_c("...Done!")
            if backup_msg:
                print_c(backup_msg)
        return self.file_path

class DOAJAnalysis(TempFileHandling):

    def __init__(self, temp_file_dir="tempfiles", force_update=False, make_backup=True, verbose=False, max_mdays=7):
        super().__init__("DOAJ", "csv", url="https://doaj.org/csv", temp_file_dir=temp_file_dir, max_mdays=max_mdays)
        self.doaj_issn_map = {}
        self.doaj_eissn_map = {}
        
        doaj_csv_file = self.prepare_file(force_update, make_backup, verbose)

        handle = open(doaj_csv_file, "r")
        reader = csv.DictReader(handle)
        for line in reader:
            journal_title = line["Journal title"]
            issn = line["Journal ISSN (print version)"]
            eissn = line["Journal EISSN (online version)"]
            if issn:
                self.doaj_issn_map[issn] = journal_title
            if eissn:
                self.doaj_eissn_map[eissn] = journal_title

    def lookup(self, any_issn):
        if any_issn in self.doaj_issn_map:
            return self.doaj_issn_map[any_issn]
        elif any_issn in self.doaj_eissn_map:
            return self.doaj_eissn_map[any_issn]
        return None

    def download_doaj_csv(self, filename, make_backup=False, verbose=False):
        backup_msg = None
        if make_backup and os.path.isfile(filename):
            then = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
            mdate = then.strftime("%Y_%m_%d_%H_%M_%S")
            backup_target = "tempfiles/DOAJ_" + mdate + ".csv"
            if verbose:
                backup_msg = self.MSGS['backup'].format(backup_target)
            copy2(filename, backup_target)
        request = Request("https://doaj.org/csv")
        request.add_header("User-Agent", USER_AGENT)
        with urlopen(request) as source:
            with open(filename, "wb") as dest:
                copyfileobj(source, dest)
        if verbose:
            print_c("...Done!")
            if backup_msg:
                print_c(backup_msg)
        return filename

class DOABAnalysis(object):

    # Priority mappings from DOAB fields to OpenAPC values. Unfortuately, the current DOAB CSV file is a real mess...
    MAPPINGS = {
        "book_title": ["dc.title", "dc.subject.other"],
        "publisher": ["oapen.relation.isPublishedBy_publisher.name", "oapen.relation.isPublishedBy", "oapen.relation.isPartOfBook_dc.title", "oapen.imprint"],
        "license_ref": ["BITSTREAM License"]
    }
    ISBN_FIELDS = ["oapen.relation.isPublishedBy_publisher.name",
                   "oapen.relation.isPublisherOf",
                   "oapen.relation.isbn"]

    DOAB_ISBN_RE = re.compile(r"97[89]\d{10}")

    def __init__(self, isbn_handling, doab_csv_file, update=False, verbose=False):
        self.isbn_map = {}
        self.isbn_handling = isbn_handling

        if not os.path.isfile(doab_csv_file) or update:
            self.download_doab_csv(doab_csv_file)

        lines = []
        # The file might contain NUL bytes, we need to get rid of them before
        # handing the lines to a DictReader
        with open(doab_csv_file, "r") as handle:
            for line in handle:
                if "\x00" in line:
                    continue
                lines.append(line)
        duplicate_isbns = []
        reader = csv.DictReader(lines)
        for line in reader:
            # ATM we focus on books only
            if line["dc.type"] != "book" and line["dc.title.alternative"] != "book":
                continue
            isbn_string = " ".join([line[field] for field in self.ISBN_FIELDS])
            # may contain multi-values split by a whitespace, semicolon or double vbar...
            isbn_string = isbn_string.replace(";", " ")
            isbn_string = isbn_string.replace("||", " ")
            isbn_string = isbn_string.strip()
            if len(isbn_string) == 0:
                continue
            while "  " in isbn_string:
               isbn_string = isbn_string.replace("  ", " ")
            isbns = isbn_string.split(" ")
            # ...which may also contain duplicates
            for isbn in list(set(isbns)):
                result = self.isbn_handling.test_and_normalize_isbn(isbn)
                if not result["valid"]:
                    if verbose:
                        msg = "Line {}: ISBN normalization failure ({}): {}"
                        msg = msg.format(reader.line_num, result["input_value"],
                                         ISBNHandling.ISBN_ERRORS[result["error_type"]])
                        print_r(msg)
                    continue
                else:
                    isbn = result["normalised"]
                if isbn not in self.isbn_map:
                    new_line = self._extract_line_data(line)
                    if verbose:
                        for field in ["publisher", "book_title"]:
                            if not has_value(new_line[field]):
                                msg = "Line {}: No '{}' value found for ISBN {}" 
                                print_r(msg.format(reader.line_num, field, isbn))
                    self.isbn_map[isbn] = new_line
                else:
                    if isbn not in duplicate_isbns:
                        duplicate_isbns.append(isbn)
                        if verbose:
                            print_y("ISBN duplicate found in DOAB: " + isbn)
        for duplicate in duplicate_isbns:
            # drop duplicates alltogether
            del(self.isbn_map[duplicate])
        if verbose:
            print_b("ISBN map created, contains " + str(len(self.isbn_map)) + " entries")

    def _extract_line_data(self, line):
        new_line = {key: "" for key in self.MAPPINGS.keys()}
        for key, prio_list in self.MAPPINGS.items():
            for field in prio_list:
                if has_value(line[field]) and not self.DOAB_ISBN_RE.search(line[field]):
                    new_line[key] = line[field]
                    break
        return new_line

    def lookup(self, isbn):
        result = self.isbn_handling.test_and_normalize_isbn(isbn)
        if result["valid"]:
            norm_isbn = result["normalised"]
            return self.isbn_map.get(norm_isbn)
        return None

    def download_doab_csv(self, target):
        urlretrieve("https://directory.doabooks.org/download-export?format=csv", target)

class ESACHandling(TempFileHandling):

    def __init__(self, temp_file_dir="tempfiles", force_update=False, make_backup=True, verbose=True, max_mdays=7):
        super().__init__("ESAC_Transformative_Agreement_Registry", "xlsx", url="https://keeper.mpdl.mpg.de/f/7fbb5edd24ab4c5ca157/?dl=1", temp_file_dir=temp_file_dir, max_mdays=max_mdays)
        self.prepare_file(force_update, make_backup, verbose, decompress="excel_to_csv", decompress_kwargs={"skip_lines": 2})
        self.mapping_table = self._prepare_mapping_table()

    def _prepare_mapping_table(self):
        csv_file_path = os.path.join(self.temp_file_dir, self.file_name + ".csv")
        table = {}
        with open(csv_file_path, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                esac_id = line["ID"]
                table[esac_id] = line
        return table

    def get_esac_entry(self, esac_id, show_warnings=True):
        if esac_id not in self.mapping_table:
            return None
        entry = self.mapping_table[esac_id]
        publisher_oapc = mappings.ESAC_PUBLISHER_MAPPINGS.get(entry["Publisher"], "")
        entry["Publisher_OAPC"] = publisher_oapc
        if not publisher_oapc and show_warnings:
            msg = 'ESAC publisher "{}" not found in ESAC_PUBLISHER_MAPPINGS'
            print_y("WARNING: " + msg.format(entry["Publisher"]))
        country_oapc = mappings.ESAC_COUNTRY_MAPPINGS.get(entry["Country"], "")
        entry["Country_OAPC"] = country_oapc
        if not country_oapc and show_warnings:
            msg = 'ESAC Country Name "{}" not found in ESAC_COUNTRY_MAPPINGS'
            print_y("WARNING: " + msg.format(entry["Country"]))
        return entry

class ISSNLHandling(TempFileHandling):

    ISSNL_FILE_PATTERN = "%Y%m%d.ISSN-to-ISSN-L.txt"
    ISSN_L_RE = re.compile(r"^(?P<issn>\d{4}-\d{3}[\dxX])\t(?P<issn_l>\d{4}-\d{3}[\dxX])")

    def __init__(self, temp_file_dir="tempfiles/issnltables", force_update=False, make_backup=True, verbose=True, max_mdays=7):
        super().__init__("issnltables", "zip", url="http://www.issn.org/wp-content/uploads/2014/03/issnltables.zip", temp_file_dir=temp_file_dir, max_mdays=max_mdays)
        self.temp_file_dir = temp_file_dir
        self.verbose = verbose
        self.prepare_file(force_update, make_backup, verbose, decompress="zip")
        file_name =  self._find_latest_issnl_file()
        self.mapping_table = self._prepare_mapping_table(file_name)

    def get_issnl(self, issn):
        if "-" not in issn:
            issn = issn[:4] + "-"  + issn[4:]
        issnl = self.mapping_table.get(issn)
        if issnl is not None:
            issnl = get_corrected_issn_l(issnl)
        return issnl

    def _find_latest_issnl_file(self):
        latest_file_name = None
        latest_file_date = None
        for file_name in os.listdir(self.temp_file_dir):
            try:
                date = datetime.datetime.strptime(file_name, self.ISSNL_FILE_PATTERN)
                if latest_file_date is None or date > latest_file_date:
                    latest_file_date = date
                    latest_file_name = file_name
            except ValueError:
                continue
        if latest_file_name is None:
            msg = "Could not find a file in {} matching the pattern {}"
            raise Exception(msg.format(self.temp_file_dir, self.ISSNL_FILE_PATTERN))
        if self.verbose:
            msg = "Latest ISSN-L mapping file according to file name: {}"
            print_c(msg.format(latest_file_name))
        return latest_file_name

    def _prepare_mapping_table(self, file_name):
        table = {}
        if self.verbose:
            print_c("Preparing mapping table...")
        itself = other = 0
        file_path = os.path.join(self.temp_file_dir, file_name)
        with open(file_path, "r") as handle:
            for line in handle:
                match = self.ISSN_L_RE.match(line)
                if match:
                    match_dict = match.groupdict()
                    table[match_dict['issn']] = match_dict['issn_l']
                    if match_dict['issn'] == match_dict['issn_l']:
                        itself += 1
                    else:
                        other += 1
        if self.verbose:
            msg = "Done. ({} ISSNs are pointing to themselves as ISSN-L, {} to another value)"
            print_c(msg.format(itself, other))
        return table

class ISBNHandling(TempFileHandling):

    # regex for 13-digit, unsplit ISBNs
    ISBN_RE = re.compile(r"^97[89]\d{10}$")

    # regex for 13-digit ISBNs split with hyphens
    ISBN_SPLIT_RE = re.compile(r"^97[89]\-\d{1,5}\-\d{1,7}\-\d{1,6}\-\d{1}$")

    ISBN_ERRORS = {
        0: "Input is neither a valid split nor a valid unsplit 13-digit ISBN",
        1: "Too short (Must be 17 chars long including hyphens)",
        2: "Too long (Must be 17 chars long including hyphens)",
        3: "Input ISBN was split, but the segmentation is invalid"
    }

    def __init__(self, temp_file_dir="tempfiles", force_update=False, make_backup=True, verbose=True, max_mdays=7):
        super().__init__("ISBNRangeFile", "xml", url="http://www.isbn-international.org/export_rangemessage.xml", temp_file_dir=temp_file_dir, max_mdays=max_mdays)
        range_file_path = self.prepare_file(force_update, make_backup, verbose)
        with open(range_file_path, "r") as range_file:
            range_file_content = range_file.read()
            range_file_root = ET.fromstring(range_file_content)
            self.ean_elements = range_file_root.findall("./EAN.UCCPrefixes/EAN.UCC")
            self.registration_groups = range_file_root.findall("./RegistrationGroups/Group")

    def download_range_file(self, target):
        urlretrieve("http://www.isbn-international.org/export_rangemessage.xml", target)

    def test_and_normalize_isbn(self, isbn):
        """
        Take a string input and try to normalize it to a 13-digit, split ISBN.

        This method takes a string which is meant to represent a split or unsplit 13-digit ISBN. It
        applies a range of tests to verify its validity and then returns a normalized, split variant.

        The following tests will be applied:
            - Syntax (Regex)
            - Re-split and segmentation comparison (if input was split already)

        Args:
            isbn: A string potentially representing a 13-digit ISBN (split or unsplit).
        Returns:
            A dict with 3 keys:
                'valid': A boolean indicating if the input passed all tests.
                'input_value': The original input value
                'normalised': The normalised, split result. Will be present if 'valid' is True.
                'error_type': An int indicating why a test failed. Will be present if 'valid'
                              is False. Corresponds to a key in the ISBN_ERRORS dict.
        """
        ret = {"valid": False, "input_value": str(isbn)}
        stripped_isbn = isbn.strip()
        unsplit_isbn = stripped_isbn.replace("-", "")
        split_on_input = False
        if self.ISBN_SPLIT_RE.match(stripped_isbn):
            if len(stripped_isbn) < 17:
                ret["error_type"] = 1
                return ret
            elif len(stripped_isbn) > 17:
                ret["error_type"] = 2
                return ret
            else:
                split_on_input = True
        if self.ISBN_RE.match(unsplit_isbn):
            split_isbn = self.split_isbn(unsplit_isbn)["value"]
            if split_on_input and split_isbn != stripped_isbn:
                ret["error_type"] = 3
                return ret
            ret["normalised"] = split_isbn
            ret["valid"] = True
            return ret
        ret["error_type"] = 0
        return ret

    def isbn_has_valid_check_digit(self, isbn):
        """
        Take a string representing a 13-digit ISBN (without hyphens) and test if its check digit is
        correct.
        """
        if not self.ISBN_RE.match(isbn):
            raise ValueError(str(isbn) + " is no valid 13-digit ISBN!")
        checksum = 0
        for index, digit in enumerate(isbn):
            if index % 2 == 0:
                checksum += int(digit)
            else:
                checksum += 3 * int(digit)
        return checksum % 10 == 0

    def _get_range_length_from_rules(self, isbn_fragment, rules_element):
        value = int(isbn_fragment[:7])
        range_re = re.compile(r"(?P<min>\d{7})-(?P<max>\d{7})")
        for rule in rules_element.findall("Rule"):
            range_text = rule.find("Range").text
            range_match = range_re.match(range_text)
            if int(range_match["min"]) <= value <= int(range_match["max"]):
                length = rule.find("Length").text
                return int(length)
        # Shouldn't happen as the range file is meant to be comprehensive. Undefined ranges are marked
        # with a length of 0 instead.
        msg = ('Could not find a length definition for fragment "' + isbn_fragment + '" in the ISBN ' +
               'range file.')
        raise ValueError(msg)

    def split_isbn(self, isbn):
        """
        Take an unsplit, 13-digit ISBN and insert hyphens to correctly separate its parts.

        This method takes a 13-digit ISBN and returns a hyphenated variant (Example: 9782753518278 ->
        978-2-7535-1827-8). Since the segments of an ISBN may vary in length (except for the EAN prefix
        and the check digit), the official "RangeMessage" XML file provided by the ISBN organization is
        needed for reference.

        Args:
            isbn: A string representing a 13-digit ISBN.
        Returns:
            A dict with two keys: 'success' and 'result'. If the process was successful, 'success'
            will be True and 'result' will contain the hyphenated result string. Otherwise, 'success'
            will be False and 'result' will contain an error message stating the reason.
        """
        ret_value = {
            'success': False,
            'value': None
        }
        split_isbn = ""
        remaining_isbn = isbn

        if not self.ISBN_RE.match(isbn):
            ret_value['value'] = '"' + str(isbn) + '" is no valid 13-digit ISBN!'
            return ret_value
        for ean in self.ean_elements:
            prefix = ean.find("Prefix").text
            if remaining_isbn.startswith(prefix):
                split_isbn += prefix
                remaining_isbn = remaining_isbn[len(prefix):]
                rules = ean.find("Rules")
                length = self._get_range_length_from_rules(remaining_isbn, rules)
                if length == 0:
                    msg = ('Invalid ISBN: Remaining fragment "{}" for EAN prefix "{}" is inside a ' +
                           'range which is not marked for use yet')
                    ret_value['value'] = msg.format(remaining_isbn, prefix)
                    return ret_value
                group = remaining_isbn[:length]
                split_isbn += "-" + group
                remaining_isbn = remaining_isbn[length:]
                break
        else:
            msg = 'ISBN "{}" does not seem to have a valid prefix.'
            ret_value['value'] = msg.format(isbn)
            return ret_value
        for group in self.registration_groups:
            prefix = group.find("Prefix").text
            if split_isbn == prefix:
                rules = group.find("Rules")
                length = self._get_range_length_from_rules(remaining_isbn, rules)
                if length == 0:
                    msg = ('Invalid ISBN: Remaining fragment "{}" for registration group "{}" is ' +
                           'inside a range which is not marked for use yet')
                    ret_value['value'] = msg.format(remaining_isbn, split_isbn)
                    return ret_value
                registrant = remaining_isbn[:length]
                split_isbn += "-" + registrant
                remaining_isbn = remaining_isbn[length:]
                check_digit = remaining_isbn[-1:]
                publication_number = remaining_isbn[:-1]
                split_isbn += "-" + publication_number + "-" + check_digit
                ret_value['success'] = True
                ret_value['value'] = split_isbn
                return ret_value
        else:
            msg = 'ISBN "{}" does not seem to have a valid registration group element.'
            ret_value['value'] = msg.format(isbn)
            return ret_value

class ContractsLookup(object):

    CONTRACTS_FILE = "../data/transformative_agreements/contracts.csv"

    def __init__(self):
        lookup_fields = ["identifier", "contract_name", "group_id"]
        data_fields = ["identifier", "contract_name", "group_id", "consortium"]
        self.lookup_dicts = {
            field: {} for field in lookup_fields
        }
        with open(self.CONTRACTS_FILE, "r") as handle:
            reader = csv.DictReader(handle)
            for line in reader:
                data = {field: line[field] for field in data_fields}
                for field in lookup_fields:
                    field_value = line[field]
                    if not has_value(field_value):
                        continue
                    if field_value not in self.lookup_dicts[field]:
                        self.lookup_dicts[field][field_value] = {
                            field: [] for field in data_fields
                        }
                    for line_field, line_data in data.items():
                        if has_value(line_data) and line_data not in self.lookup_dicts[field][field_value][line_field]:
                            self.lookup_dicts[field][field_value][line_field].append(line_data)

    def get_by_identifier(self, identifier):
        return self.lookup_dicts["identifier"].get(identifier, None)

    def get_by_contract_name(self, identifier):
        return self.lookup_dicts["contract_name"].get(identifier, None)

    def get_by_group_id(self, identifier):
        return self.lookup_dicts["group_id"].get(identifier, None)

class CSVAnalysisResult(object):

    def __init__(self, blanks, dialect, has_header, enc, enc_conf):
        self.blanks = blanks
        self.dialect = dialect
        self.has_header = has_header
        self.enc = enc
        self.enc_conf = enc_conf

    def __str__(self):
        ret = "*****CSV file analysis*****\n"
        if self.dialect is not None:
            quote_consts = ["QUOTE_ALL", "QUOTE_MINIMAL", "QUOTE_NONE",
                            "QUOTE_NONNUMERIC"]
            quoting = self.dialect.quoting
            for const in quote_consts:
            # Seems hacky. Is there a more pythonic way to determine a
            # member const by its value?
                if hasattr(csv, const) and getattr(csv, const) == self.dialect.quoting:
                    quoting = const
            ret += ("CSV dialect sniffing:\ndelimiter => {dlm}\ndoublequote " +
                    "=> {dbq}\nescapechar => {esc}\nquotechar => {quc}\nquoting " +
                    "=> {quo}\nskip initial space => {sis}\n\n").format(
                        dlm=self.dialect.delimiter,
                        dbq=self.dialect.doublequote,
                        esc=self.dialect.escapechar,
                        quc=self.dialect.quotechar,
                        quo=quoting,
                        sis=self.dialect.skipinitialspace)

        if self.has_header:
            ret += "CSV file seems to have a header.\n\n"
        else:
            ret += "CSV file doesn't seem to have a header.\n\n"


        if self.blanks:
            ret += "Found " + str(self.blanks) + " empty lines in CSV file.\n\n"
        if self.enc:
            ret += ("Educated guessing of file character encoding: {} with " +
                    "a confidence of {}%\n").format(
                        self.enc,
                        int(self.enc_conf * 100))
        ret += "***************************"
        return ret

class ANSIColorFormatter(logging.Formatter):
    """
    A simple logging formatter using ANSI codes to colorize messages
    """

    def __init__(self):
        super().__init__(fmt="%(levelname)s: %(message)s", datefmt=None, style="%")

    FORMATS = {
        logging.ERROR: "\033[91m%(levelname)s: %(message)s\033[0m",
        logging.WARNING: "\033[93m%(levelname)s: %(message)s\033[0m",
        logging.INFO: "\033[94m%(levelname)s: %(message)s\033[0m",
        "DEFAULT": "%(levelname)s: %(message)s"
    }

    def format(self, record):
        self._style._fmt = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
        return logging.Formatter.format(self, record)

class BufferedErrorHandler(MemoryHandler):
    """
    A modified MemoryHandler without automatic flushing.

    This handler serves the simple purpose of buffering error and critical
    log messages so that they can be shown to the user in collected form when
    the enrichment process has finished.
    """
    def __init__(self, target):
        MemoryHandler.__init__(self, 100000, target=target)
        self.setLevel(logging.ERROR)

    def shouldFlush(self, record):
        return False

class NoRedirection(HTTPErrorProcessor):
    """
    A dummy processor to suppress HTTP redirection.

    This handler serves the simple purpose of stopping redirection for
    easy extraction of shortDOI redirect targets.
    """
    def http_response(self, request, response):
        return response

    https_response = http_response

class UnsupportedDoiTypeError(ValueError):
    """
    An exception indicating an unsupported DOI type while looking up Crossref metadata

    Its main purpose is to store already obtained Crossref data (type + title)
    for later error handling, avoiding double lookups
    """
    def __init__(self, doi_type, doi_types, crossref_title):
        self.doi_type = doi_type
        self.crossref_title = crossref_title
        supported_types = []
        for valid_doi_type, content in doi_types.items():
            doi_type_str = valid_doi_type
            if content['aliases']:
                doi_type_str += ' (alias: ' + ", ".join(content['aliases']) + ')'
            supported_types.append(doi_type_str)
        msg = ('Unsupported DOI type "{}" (OpenAPC only supports the following types: {})')
        msg = msg.format(doi_type, ", ".join(supported_types))
        super().__init__(msg)

def get_normalised_DOI(doi_string):
    doi_string = doi_string.strip()
    doi_match = DOI_RE.match(doi_string)
    if doi_match:
        doi = doi_match.groupdict()["doi"]
        return doi.lower()
    shortdoi_match = SHORTDOI_RE.match(doi_string)
    if shortdoi_match:
        # Extract redirect URL to obtain original DOI
        shortdoi = shortdoi_match.groupdict()["shortdoi"]
        url = "https://doi.org/" + shortdoi
        opener = build_opener(NoRedirection)
        try:
            res = opener.open(url)
            if res.code == 301:
                doi_match = DOI_RE.match(res.headers["Location"])
                if doi_match:
                    doi = doi_match.groupdict()["doi"]
                    return doi.lower()
            return None
        except (HTTPError, URLError):
            return None
    return None

def is_wellformed_ISSN(issn_string):
    issn_match = ISSN_RE.match(issn_string)
    if issn_match is not None:
        return True
    return False

def is_valid_ISSN(issn_string):
    issn_match = ISSN_RE.match(issn_string)
    match_dict = issn_match.groupdict()
    check_digit = match_dict["check_digit"]
    if check_digit in ["X", "x"]:
        check_digit = 10
    else:
        check_digit = int(check_digit)
    digits = match_dict["first_part"] + match_dict["second_part"]
    factor = 8
    total = 0
    for digit in digits:
        total += int(digit) * factor
        factor -= 1
    mod = total % 11
    if mod == 0 and check_digit == 0:
        return True
    else:
        if 11 - mod == check_digit:
            return True
    return False

def analyze_csv_file(file_path, test_lines=1000, enc=None):
    try:
        csv_file = open(file_path, "rb")
    except IOError as ioe:
        error_msg = "Error: could not open file '{}': {}".format(file_path,
                                                                 ioe.strerror)
        return {"success": False, "error_msg": error_msg}

    guessed_enc = None
    guessed_enc_confidence = None
    blanks = 0
    if chardet:
        byte_content = b"" # in python3 chardet operates on bytes
        lines_processed = 0
        for line in csv_file:
            if line.strip(): # omit blank lines
                lines_processed += 1
                if lines_processed <= test_lines:
                    byte_content += line
            else:
                blanks += 1
        chardet_result = chardet.detect(byte_content)
        guessed_enc = chardet_result["encoding"]
        guessed_enc_confidence = chardet_result["confidence"]

    csv_file.close()

    if enc is not None:
        used_encoding = enc
    elif guessed_enc is not None:
        used_encoding = guessed_enc
    else:
        used_encoding = locale.getpreferredencoding()

    text_content = ""
    with open(file_path, "r", encoding=used_encoding) as csv_file:
        try:
            lines_processed = 0
            for line in csv_file:
                if line.strip(): # omit blank lines
                    lines_processed += 1
                    text_content += line
                    if lines_processed > test_lines:
                        break
        except UnicodeError as ue:
            error = ('A UnicodeError occured while trying to read the csv ' +
                     'file ("{}") - it seems the encoding we used ({}) is ' +
                     'not correct.')
            error_msg = error.format(str(ue), used_encoding)
            return {"success": False, "error_msg": error_msg}

    sniffer = csv.Sniffer()
    try:
        dialect = sniffer.sniff(text_content)
        has_header = sniffer.has_header(text_content)
    except csv.Error as csve:
        error_msg = ("Error: An error occured while analyzing the file: '" +
                     str(csve) + "'. Maybe it is no valid CSV file?")
        return {"success": False, "error_msg": error_msg}
    result = CSVAnalysisResult(blanks, dialect, has_header, guessed_enc, guessed_enc_confidence)
    return {"success": True, "data": result}

def get_csv_file_content(file_name, enc=None, force_header=False, print_results=True):
    result = analyze_csv_file(file_name, enc=enc)
    if result["success"]:
        csv_analysis = result["data"]
        if print_results:
            print(csv_analysis)
    else:
        raise IOError(result["error_msg"])

    if enc is None:
        enc = csv_analysis.enc

    if enc is None:
        raise IOError("No encoding given for CSV file and automated detection failed.")

    dialect = csv_analysis.dialect

    csv_file = open(file_name, "r", encoding=enc)

    content = []
    reader = csv.reader(csv_file, dialect=dialect)
    header = []
    if csv_analysis.has_header or force_header:
        header.append(next(reader))
    for row in reader:
        content.append(row)
    csv_file.close()
    return (header, content)

def has_value(field):
    return len(field) > 0 and field != "NA"

def _process_oai_invoice(invoice_elem, namespaces, period=None):
    global EXCHANGE_RATES
    invoice_xpaths = {
        'fee_type': 'intact:fee_type',
        'amount': 'intact:ammount',
        'currency': 'intact:currency'
    }
    data = {}
    for elem, xpath in invoice_xpaths.items():
        result = invoice_elem.find(xpath, namespaces)
        if result is not None and result.text is not None:
            data[elem] = result.text
        else:
            msg = 'Could not process invoice data: Element "{}" not found!'
            print_r(msg.format(elem))
            return None
    if data['fee_type'] not in ['APC', 'Hybrid-OA']:
        msg = 'Could not process invoice data: Unknown fee_type "{}"'
        print_r(msg.format(data['fee_type']))
        return None
    if data['currency'] != 'EUR':
        cur = data['currency']
        if period is None:
            msg = 'Could not process invoice data: Currency is "{}" and no period for automated conversion was found.'
            print_r(msg.format(cur))
            return None
        if cur not in EXCHANGE_RATES:
            try:
                EXCHANGE_RATES[cur] = get_euro_exchange_rates(cur, "A")
            except ValueError as ve:
                msg = 'Could not process invoice data: Error while obtaining exchange rates for automated conversion: {}.'
                print_r(msg.format(str(ve)))
                return None
        try:
            exchange_rate = EXCHANGE_RATES[cur][period]
        except KeyError as ke:
            msg = 'Could not process invoice data: No annual exchange rate available for currency {} and period {}.'
            print_r(msg.format(cur, period))
            return None
        euro_amount = round(float(data['amount'])/float(exchange_rate), 2)
        msg = 'Automated conversion: {} {} -> {} EUR (period: {})'
        msg = msg.format(data['amount'], cur, euro_amount, period)
        print_b(msg)
        data['currency'] = 'EUR'
        data['amount'] = str(euro_amount)
    return data

def _auto_atof(str_value):
    """
    string to float conversion with best guessing of locale
    """
    str_value = str_value.strip()
    old_locale = locale.getlocale(locale.LC_NUMERIC)
    if re.compile(r'\d+\.\d+').match(str_value):
        locale.setlocale(locale.LC_NUMERIC, locale.normalize('en.utf-8'))
        float_value = locale.atof(str_value)
    elif re.compile(r'\d+\,\d+').match(str_value):
        locale.setlocale(locale.LC_NUMERIC, locale.normalize('de.utf-8'))
        float_value = locale.atof(str_value)
    else:
        try:
            float_value = float(str_value)
        except ValueError as ve:
            return None
    locale.setlocale(locale.LC_NUMERIC, old_locale)
    return float_value

def process_intact_xml(processing_instructions=None, *xml_content_strings):
    collection_xpath = ".//oai_2_0:metadata//intact:collection"
    record_xpath = ".//oai_2_0:record"
    identifier_xpath = ".//oai_2_0:header//oai_2_0:identifier"
    invoice_xpath = "intact:invoice"
    namespaces = {
        "oai_2_0": "http://www.openarchives.org/OAI/2.0/",
        "intact": "http://intact-project.org"
    }
    articles = []
    for content_string in xml_content_strings:
        root = ET.fromstring(content_string)
        records = root.findall(record_xpath, namespaces)
        counter = 0
        for record in records:
            article = {}
            identifier = record.find(identifier_xpath, namespaces)
            article["identifier"] = identifier.text
            collection = record.find(collection_xpath, namespaces)
            if collection is None:
                # Might happen with deleted records
                continue
            for elem, xpath in OAI_COLLECTION_CONTENT.items():
                article[elem] = "NA"
                if xpath is not None:
                    result = collection.find(xpath, namespaces)
                    if result is not None and result.text is not None:
                        article[elem] = result.text
            # JOIN2 institutions make use of the invoice variant
            invoices = collection.findall(invoice_xpath, namespaces)
            invoice_fee_type = None
            for invoice in invoices:
                invoice_data = _process_oai_invoice(invoice, namespaces, article['period'])
                if invoice_data:
                    # check for consistent fee types
                    if invoice_fee_type is None:
                        invoice_fee_type = invoice_data['fee_type']
                    elif invoice_fee_type != invoice_data['fee_type']:
                        msg = "Error: Record {} contains invoices with different OA fee types!"
                        print_r(msg.format(article['identifier']))
                        article['euro'] = 'NA'
                        break
                    if not has_value(article['euro']):
                        article['euro'] = invoice_data['amount']
                    else:
                        old_amount = _auto_atof(article['euro'])
                        new_amount = _auto_atof(invoice_data['amount'])
                        article['euro'] = str(old_amount + new_amount)
                        msg = "More than one APC amount found, adding values ({} + {} = {})."
                        print_b(msg.format(old_amount, new_amount, old_amount + new_amount))
            if processing_instructions:
                target_string = processing_instructions["generator"]
                for variable in processing_instructions["variables"]:
                    target_string = target_string.replace("%" + variable + "%", article[variable])
                article[processing_instructions["target"]] = target_string
            if article["euro"] == 'NA':
                print_r("Article skipped, no APC amount found.")
                continue
            euro_float = _auto_atof(article["euro"])
            if euro_float is None:
                msg = "Article skipped, invalid value found in euro field ({})."
                print_r(msg.format(article['euro']))
                continue
            if euro_float <= 0.0:
                msg = "Article skipped, non-positive APC amount found ({})."
                print_r(msg.format(article['euro']))
                continue
            if euro_float.is_integer():
                 article["euro"] = str(int(euro_float))
            else:
                article["euro"] = str(euro_float)
            if article["doi"] != "NA":
                norm_doi = get_normalised_DOI(article["doi"])
                if norm_doi is None:
                    article["doi"] = "NA"
                else:
                    article["doi"] = norm_doi
            articles.append(article)
            counter += 1
        print_g(str(counter) + " articles harvested.")
    return articles

def find_book_dois_in_crossref(isbn_list):
    """
    Take a list of ISBNs and try to obtain book/monograph DOIs from crossref.

    Args:
        isbn_list: A list of strings representing ISBNs (will not be tested for validity).
    Returns:
        A dict with a key 'success'. If the lookup was successful,
        'success' will be True and the dict will have a second entry 'dois'
        which contains a list of obtained DOIs as strings. The list may be empty if the lookup
        returned an empty result.
        If an error occured during lookup, 'success' will be False and the dict will
        contain a second entry 'error_msg' with a string value
        stating the reason.
    """
    ret_value = {
        "success": False,
        "dois": []
    }
    if type(isbn_list) != type([]) or len(isbn_list) == 0:
        ret_value['error_msg'] = "Parameter must be a non-empty list!"
        return ret_value
    filter_list = ["isbn:" + isbn.strip() for isbn in isbn_list]
    filters = ",".join(filter_list)
    route = "?filter=" + filters + "&rows=500"
    request = _build_crossref_request(route)
    try:
        ret = urlopen(request)
        content = ret.read()
        data = json.loads(content)
        if data["message"]["total-results"] == 0:
            ret_value["success"] = True
        else:
            for item in data["message"]["items"]:
                if item["type"] in ["monograph", "book", "edited-book"] and item["DOI"] not in ret_value["dois"]:
                    ret_value["dois"].append(item["DOI"])
            if len(ret_value["dois"]) == 0:
                msg = "No monograph/book DOI type found in  Crossref ISBN search result ({})!"
                raise ValueError(msg.format(url))
            else:
                ret_value["success"] = True
    except HTTPError as httpe:
        ret_value['error_msg'] = "HTTPError: {} - {}".format(httpe.code, httpe.reason)
    except URLError as urle:
        ret_value['error_msg'] = "URLError: {}".format(urle.reason)
    except ValueError as ve:
        ret_value['error_msg'] = str(ve)
    return ret_value

def title_lookup(lookup_title, acccepted_doi_types, auto_accept=False):
    empty_result = {
        "found_title": "",
        "similarity": 0,
        "doi": ""
    }
    params = {"rows": "100", "query.bibliographic": lookup_title}
    route = "?" + urlencode(params, quote_via=quote_plus)
    request = _build_crossref_request(route)

    skipped_stats = {}
    try:
        ret = urlopen(request)
        content = ret.read()
        data = json.loads(content)
        items = data["message"]["items"]
        most_similar = empty_result
        for item in items:
            if "title" not in item:
                continue
            if "type" not in item:
                continue
            if item["type"] not in acccepted_doi_types:
                if item["type"] not in skipped_stats:
                    skipped_stats[item["type"]] = 1
                else:
                    skipped_stats[item["type"]] += 1
                continue
            title = item["title"].pop()
            result = {
                "found_title": title,
                "similarity": Levenshtein.ratio(title.lower(), params["query.bibliographic"].lower()),
                "doi": item["DOI"]
            }
            if most_similar["similarity"] < result["similarity"]:
                most_similar = result
            # Also try a title: subtitle combination, can be helpful for books
            if "subtitle" in item:
                full_title = title + ": " + item["subtitle"].pop()
                result = {
                    "found_title": full_title,
                    "similarity": Levenshtein.ratio(full_title.lower(), params["query.bibliographic"].lower()),
                    "doi": item["DOI"]
                }
                if most_similar["similarity"] < result["similarity"]:
                    most_similar = result
    except HTTPError as httpe:
        error_msg = "An HTTPError occured during title lookup: {} - {}".format(httpe.code, httpe.reason)
        print_r(error_msg)
        return None
    if skipped_stats:
        msg = "Some search results were ignored due to non-accepted DOI types: "
        for name, count in skipped_stats.items():
            msg += "'" + str(name) + "': " + str(count) + ", "
        print_y(msg[:-2])
    if most_similar["doi"]:
        similarity = most_similar["similarity"]
        msg = "{} match for a final version found in Crossref (similarity: {}):"
        if similarity == 1.0:
            print_c(msg.format("Perfect", most_similar["similarity"]))
        elif similarity >= 0.9:
            print_g(msg.format("Good", most_similar["similarity"]))
        elif similarity >= 0.8:
            print_y(msg.format("Possible", most_similar["similarity"]))
        else:
            print_r(msg.format("No good", most_similar["similarity"]))
        msg_old = "    '{}' [title for existing DOI]"
        print(msg_old.format(lookup_title))
        msg_new = "    '{}' [title for discovered doi {}]"
        print(msg_new.format(most_similar["found_title"], most_similar["doi"]))
        if auto_accept and similarity >= 0.9:
            print_g("Result auto-accepted since the match similarity is sufficicent (>=0.9)")
            return most_similar["doi"]
        answer = input("Do you want to accept the new DOI? (y/n)")
        while answer not in ["y", "n"]:
            answer = input("Please type 'y' or 'n':")
        if answer == "y":
            return most_similar["doi"]
    else:
        print_r("Could not obtain a result with an accepted DOI type.")
        return None

def _extract_crossref_license(crossref_data):
    """
    Helper function to extract license information from a crossref JSON object
    """
    ret = None
    if 'message' in crossref_data:
        if 'license' in crossref_data['message']:
            for lic in crossref_data['message']['license']:
                 # Use the first license found unless there's a 'vor' version
                if ret is None:
                    ret = lic['URL']
                elif 'content-version' in lic and lic['content-version'] == 'vor':
                    ret = lic['URL']
    return ret

def _extract_crossref_isxn(crossref_data, identifier_type, representation_type):
    """
    Helper function to extract electronic/print ISSNs and ISBNS from a crossref JSON object
    """
    valid_identifier_types = ['issn', 'isbn']
    valid_representation_types = ['print', 'electronic']
    if identifier_type not in valid_identifier_types:
        raise ValueError('identifier_type must be one of ' + str(valid_identifier_types))
    if representation_type not in valid_representation_types:
        raise ValueError('identifier_type must be one of ' + str(valid_representation_types))
    ret = None
    id_type_key = identifier_type + '-type'
    if 'message' in crossref_data:
        if id_type_key in crossref_data['message']:
            for identifier in crossref_data['message'][id_type_key]:
                if identifier['type'] == representation_type:
                    ret = identifier['value']
                    break
    return ret

def _build_crossref_request(api_route):
    global CROSSREF_PLUS_TOKEN
    if CROSSREF_PLUS_TOKEN == "unset":
        if os.path.isfile("crossref_plus_token"):
            with open("crossref_plus_token", "r") as f:
                token = f.read()
                CROSSREF_PLUS_TOKEN = token.strip()
                print_c("API Key for Crossref Plus successfully loaded.")
        else:
            CROSSREF_PLUS_TOKEN = None
            print_y('Did not find a file "crossref_plus_token" with ' +
                    'an API key - the public Crossref API will be used.')
    url = 'https://api.crossref.org/works/' + api_route
    req = Request(url)
    req.add_header('User-Agent', USER_AGENT)
    if CROSSREF_PLUS_TOKEN is not None and CROSSREF_PLUS_TOKEN != "unset":
        req.add_header('Crossref-Plus-API-Token', CROSSREF_PLUS_TOKEN)
    return req

def get_metadata_from_ezb(issn):
    """
    Take an ISSN and obtain journal metadata from the EZB.
    """
    if not is_wellformed_ISSN(issn):
        return {"success": False,
                "error_msg": "Parse Error: '{}' is no valid ISSN".format(issn)
               }
    journal_xpaths = {
        "access_msg" : {
            "path": ".//ezb_detail_about_journal/journal/detail/access_conditions",
            "attrib": None
        },
        "access_color": {
            "path": ".//ezb_detail_about_journal/journal/journal_color",
            "attrib": "color"
         },
        "title": {
            "path": ".//ezb_detail_about_journal/journal/title",
            "attrib": None
        },
        "remarks": {
            "path": ".//ezb_detail_about_journal/journal/detail/remarks",
            "attrib": None
        },
        "categories": {
            "path": ".//ezb_detail_about_journal/journal/detail/categories/category",
            "attrib": None,
        },
        "doaj_link": {
            "path": ".//ezb_detail_about_journal/journal/publishing/doaj",
            "attrib": "url",
        }
    }
    url = "https://ezb.ur.de/searchres.phtml?bibid=AAAAA&jq_type1=QS&xmloutput=1&jq_term1=" + issn
    ret_value = {"success": True}
    try:
        request = requests.get(url)
        root = ET.fromstring(request.text)
        journal_xpath = ".//ezb_alphabetical_list_searchresult/alphabetical_order/journals/journal"
        result = root.findall(journal_xpath)
        data = []
        for journal in result:
            jourid = journal.attrib.get("jourid", None)
            if jourid is not None:
                j_url = "https://ezb.ur.de/detail.phtml?bibid=AAAAA&xmloutput=1&jour_id=" + jourid
                j_request = requests.get(j_url)
                j_root = ET.fromstring(j_request.text)
                j_data = {}
                for elem, path_info in journal_xpaths.items():
                    j_data[elem] = None
                    result = j_root.findall(path_info["path"])
                    if result is None:
                        continue
                    if path_info["attrib"] is None:
                        result_texts = [xml_elem.text for xml_elem in result if xml_elem.text is not None]
                        j_data[elem] = "; ".join(result_texts)
                    else:
                        result_attribs = [xml_elem.attrib.get(path_info["attrib"], "") for xml_elem in result]
                        j_data[elem] = "; ".join(result_attribs)
                data.append(j_data)
        ret_value["data"] = data
    except HTTPError as httpe:
        ret_value['success'] = False
        ret_value['error_msg'] = "HTTPError: {} - {}".format(httpe.code, httpe.reason)
    except URLError as urle:
        ret_value['success'] = False
        ret_value['error_msg'] = "URLError: {}".format(urle.reason)
    return ret_value

def get_metadata_from_crossref(doi_string):
    """
    Take a DOI and extract metadata relevant to OpenAPC from crossref.

    This method looks up a DOI in crossref and returns all metadata fields
    relevant to OpenAPC. The set of metadata returned depends on the crossref
    DOI type.

    Args:
        doi_string: A string representing a DOI. 'Pure' form (10.xxx),
        DOI Handbook notation (doi:10.xxx) or crossref-style
        (https://doi.org/10.xxx) are all acceptable.
    Returns:
        A dict with a key 'success'. If data extraction was successful,
        'success' will be True and the dict will have a second entry 'data'
        which contains the extracted metadata plus the doi type as another dict:

        {'doi_type': 'journal-article',
         'publisher': 'MDPI AG',
         'journal_full_title': 'Chemosensors',
         [...]
        }
        The dict will contain all keys in question, those where no data could
        be retreived will have a None value.

        If data extraction failed, 'success' will be False and the dict will
        contain both an entry 'error_msg' with a string value
        stating the reason and an entry 'exception' holding the exception object.
    """
    doi_types = {
        'journal-article': {
            'aliases': [],
            'data_fields': {
                'publisher': {
                    'access': 'path',
                    'path_elements': ['message', 'publisher']
                },
                'journal_full_title': {
                     'access': 'path',
                     'path_elements':  ['message', 'container-title', 0]
                },
                'issn': {
                    'access': 'path',
                    'path_elements':  ['message', 'ISSN', 0]
                },
                'license_ref': {
                    'access': 'function',
                    'func_name': '_extract_crossref_license',
                    'additional_params': []
                },
                'issn_print': {
                    'access': 'function',
                    'func_name': '_extract_crossref_isxn',
                    'additional_params': ['issn', 'print']
                },
                'issn_electronic': {
                    'access': 'function',
                    'func_name': '_extract_crossref_isxn',
                    'additional_params': ['issn', 'electronic']
                }
            }
        },
        'book': {
            'aliases': ['monograph', 'edited-book'],
            'data_fields': {
                'publisher': {
                    'access': 'path',
                    'path_elements': ['message', 'publisher']
                },
                'book_title': {
                    'access': 'path',
                    'path_elements':  ['message', 'title', 0]
                },
                'isbn': {
                    'access': 'path',
                    'path_elements':  ['message', 'ISBN', 0]
                },
                'license_ref': {
                    'access': 'function',
                    'func_name': '_extract_crossref_license',
                    'additional_params': []
                },
                'isbn_print': {
                    'access': 'function',
                    'func_name': '_extract_crossref_isxn',
                    'additional_params': ['isbn', 'print']
                },
                'isbn_electronic': {
                    'access': 'function',
                    'func_name': '_extract_crossref_isxn',
                    'additional_params': ['isbn', 'electronic']
                }
            }
        }
    }
    doi = get_normalised_DOI(doi_string)
    if doi is None:
        error_msg = 'Parse Error: "{}" is no valid DOI'.format(doi_string)
        return {'success': False, 'error_msg': error_msg, 'exception': None}

    req = _build_crossref_request(doi)
    ret_value = {'success': True}
    try:
        response = urlopen(req)
        content_string = response.read()
        data = json.loads(content_string)
        data_doi_type = data['message']['type']
        normalized_doi_type = None
        for doi_type, content in doi_types.items():
            if data_doi_type == doi_type or data_doi_type in content['aliases']:
                normalized_doi_type = doi_type
                break
        if normalized_doi_type is None:
            title = ''
            if 'title' in data['message'] and data['message']['title']:
                title = data['message']['title'][0]
            raise UnsupportedDoiTypeError(data_doi_type, doi_types, title)
        crossref_data = {'doi_type': normalized_doi_type}
        data_fields = doi_types[normalized_doi_type]['data_fields']
        for field, access_method in data_fields.items():
            if access_method['access'] == 'path':
                position = data
                for element in access_method['path_elements']:
                    try:
                        position = position[element]
                    except (KeyError, IndexError):
                        crossref_data[field] = None
                        break
                else:
                    crossref_data[field] = position
            elif access_method['access'] == 'function':
                function = globals()[access_method['func_name']]
                params = [data] + access_method['additional_params']
                crossref_data[field] = function(*params)
        ret_value['data'] = crossref_data
    except HTTPError as httpe:
        ret_value['success'] = False
        ret_value['error_msg'] = 'HTTPError: {} - {}'.format(httpe.code, httpe.reason)
        ret_value['exception'] = httpe
    except RemoteDisconnected as rd:
        ret_value['success'] = False
        ret_value['error_msg'] = 'Remote Disconnected: {}'.format(str(rd))
        ret_value['exception'] = rd
    except ConnectionResetError as cre:
        ret_value['success'] = False
        ret_value['error_msg'] = 'Connection Reset: {}'.format(str(cre))
        ret_value['exception'] = cre
    except URLError as urle:
        ret_value['success'] = False
        ret_value['error_msg'] = 'URLError: {}'.format(urle.reason)
        ret_value['exception'] = urle
    except ET.ParseError as etpe:
        ret_value['success'] = False
        ret_value['error_msg'] = 'ElementTree ParseError: {}'.format(str(etpe))
        ret_value['exception'] = etpe
    except UnsupportedDoiTypeError as udte:
        ret_value['success'] = False
        ret_value['error_msg'] = str(udte)
        ret_value['exception'] = udte
    return ret_value

def get_metadata_from_ror(ror_id):
    """
    Look up a ROR ID and extract metadata relevant to OpenAPC
    """
    ret = {"success": False}
    ror_id = ror_id.strip()
    if not ROR_RE.match(ror_id):
        msg = "Regex mismatch: {} does not seem to be a valid ROR ID."
        ret["error_msg"] = msg.format(ror_id)
        return ret
    url = "https://api.ror.org/organizations/"
    url += ror_id
    data = {}
    try:
        req = Request(url)
        response = urlopen(req)
        content_string = response.read()
        ror_data = json.loads(content_string)
        ror_name = None
        for name_dict in ror_data["names"]:
            for types in name_dict["types"]:
                if "ror_display" in types:
                    ror_name = name_dict["value"]
        data["institution"] = ror_name
    except HTTPError as httpe:
        ret['error_msg'] = 'HTTPError: {} - {}'.format(httpe.code, httpe.reason)
        return ret
    ret["data"] = data
    ret["success"] = True
    return ret

def search_institution_in_ror(name):
    """
    Look up an institution (exact name) in ROR and extract all metadata.
    May return more than one record.
    """
    ret = {"success": False}
    url = "https://api.ror.org/v2/organizations?"
    quoted_name = '"{}"'.format(name)
    url = url + urlencode({'query': quoted_name})
    data = {}
    try:
        req = Request(url)
        response = urlopen(req)
        content_string = response.read()
        data = json.loads(content_string)
    except HTTPError as httpe:
        ret['error_msg'] = 'HTTPError: {} - {}'.format(httpe.code, httpe.reason)
        return ret
    ret["data"] = data
    ret["success"] = True
    return ret

def get_metadata_from_pubmed(doi_string, retry=10):
    """
    Look up a DOI in Europe PMC and extract Pubmed ID and Pubmed Central ID

    Args:
        doi_string: A string representing a doi. 'Pure' form (10.xxx),
        DOI Handbook notation (doi:10.xxx) or crossref-style
        (https://doi.org/10.xxx) are all acceptable.
        retry: Max retries upon encountering malformed XML (PMC Rest API
        may deliever a blank page in rare cases). Retries will occur after
        a 3 seconds sleep interval.
    Returns:
        A dict with a key 'success'. If data extraction was successful,
        'success' will be True and the dict will have a second entry 'data'
        which contains the extracted metadata (pmid, pmcid) as another dict.

        If data extraction failed, 'success' will be False and the dict will
        contain a second entry 'error_msg' with a string value
        stating the reason.
    """
    doi = get_normalised_DOI(doi_string)
    if doi is None:
        return {"success": False,
                "error_msg": "Parse Error: '{}' is no valid DOI".format(doi_string)
               }
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=doi:"
    url += doi
    ret_value = {'success': True}
    try:
        request = requests.get(url)
        root = ET.fromstring(request.text)
        pubmed_data = {}
        xpaths = {
            "pmid": ".//resultList/result/pmid",
            "pmcid": ".//resultList/result/pmcid",
        }
        for elem, path in xpaths.items():
            result = root.findall(path)
            if result:
                pubmed_data[elem] = result[0].text
            else:
                pubmed_data[elem] = None
        ret_value['data'] = pubmed_data
    except HTTPError as httpe:
        ret_value['success'] = False
        ret_value['error_msg'] = "HTTPError: {} - {}".format(httpe.code, httpe.reason)
    except URLError as urle:
        ret_value['success'] = False
        ret_value['error_msg'] = "URLError: {}".format(urle.reason)
    except ET.ParseError as etpe:
        if retry > 0:
            msg = ("Encountered a ParseError while reading XML from Pubmed, " +
            "retrying after 3 seconds...")
            logging.warning(msg)
            sleep(3)
            return get_metadata_from_pubmed(doi_string, retry - 1)
        else:
            ret_value['success'] = False
            ret_value['error_msg'] = "ElementTree Parse Error: {}".format(etpe.msg)
    return ret_value

def get_euro_exchange_rates(currency, frequency="D"):
    """
    Obtain historical euro exchange rates against a certain currency from the European Central Bank.
    
    Take a currency and a frequency type (either daily, monthly average or yearly average rates) and
    return a dict containing all data provided by the ECB for the chosen parameters.
    
    Args:
        currency: A three-letter string representing a currency code according to ISO 4217
        frequency: Must be either "D" (daily), "M" (monthly) or "A" (annual). In the last two cases
                   the results will be average values for the given time frames.
    
    Returns:
        A dict of date strings mapping to exchange rates (as floats). Depending on the chosen
        freqency, the date format will either be "YYYY", "YYYY-MM" or "YYYY-MM-DD".
    """
    ISO_4217_RE = re.compile(r"[A-Z]{3}")
    FREQUENCIES = ["D", "M", "A"]
    
    URL_TEMPLATE = "https://data-api.ecb.europa.eu/service/data/EXR/{}.{}.EUR.SP00.A?format=csvdata"
    
    if not ISO_4217_RE.match(currency):
        raise ValueError('"' + currency + '" is no valid currency code!')
    if frequency not in FREQUENCIES:
        raise ValueError("Frequency must be one of " + ", ".join(FREQUENCIES))
    
    url = URL_TEMPLATE.format(frequency, currency)
    req = Request(url)
    response = urlopen(req)
    lines = []
    for line in response:
        lines.append(line.decode("utf-8"))
    reader = csv.DictReader(lines)
    result = {}
    for line in reader:
        date = line["TIME_PERIOD"]
        value = line["OBS_VALUE"]
        result[date] = value
    return result

def _process_euro_value(euro_value, round_monetary, row_num, index, ta_mode, additional_costs=False):
    if not has_value(euro_value):
        if not additional_costs:
            msg = "Line %s: Empty monetary value in column %s."
            if not ta_mode:
                logging.error(msg, row_num, index)
        return "NA"
    try:
        # Cast to float to ensure the decimal point is a dot (instead of a comma)
        euro = locale.atof(euro_value)
        if euro.is_integer():
            euro = int(euro)
        if re.match(r"^\d+\.\d{3}", str(euro)):
            if round_monetary:
                euro = round(euro, 2)
                msg = "Line %s: " + MESSAGES["digits_norm"]
                logging.warning(msg, row_num, euro_value, euro_value, euro)
            else:
                msg = "Line %s: " + MESSAGES["digits_error"]
                logging.error(msg, row_num, euro_value)
        if euro == 0:
            if not additional_costs:
                msg = "Line %s: Euro value is 0"
                if not ta_mode:
                    logging.error(msg, row_num)
        return str(euro)
    except ValueError:
        msg = "Line %s: " + MESSAGES["locale"]
        logging.error(msg, row_num, euro_value, index)
        return "NA"

def _process_period_value(period_value, row_num):
    if re.match(r"^\d{4}-[0-1]{1}\d(-[0-3]{1}\d)?$", period_value):
        msg = "Line %s: " + MESSAGES["period_format"]
        new_value = period_value[:4]
        logging.info(msg, row_num, period_value, new_value)
        return new_value
    return period_value

def _process_hybrid_status(hybrid_status, row_num):
    if not has_value(hybrid_status):
        msg = "Line %s: " + MESSAGES["no_hybrid_identifier"]
        logging.error(msg, row_num)
        return "NA"
    norm_value = get_hybrid_status_from_whitelist(hybrid_status)
    if norm_value is None:
        msg = "Line %s: " + MESSAGES["unknown_hybrid_identifier"]
        logging.error(msg, row_num, hybrid_status)
        return hybrid_status
    if norm_value != hybrid_status:
        msg = "Line %s: " + MESSAGES["hybrid_normalisation"]
        logging.warning(msg, row_num, hybrid_status, norm_value)
        return norm_value
    return hybrid_status

def _process_crossref_results(current_row, row_num, key, value):
    new_value = "NA"
    if value is not None:
        if key == "journal_full_title":
            unified_value = get_unified_journal_title(value)
            unified_value = unified_value.replace("&amp;", "&")
            if unified_value != value:
                msg = MESSAGES["unify"].format("journal title", value, unified_value)
                logging.warning(msg)
            new_value = unified_value
        elif key == "publisher":
            unified_value = get_unified_publisher_name(value)
            if unified_value != value:
                msg = MESSAGES["unify"].format("publisher name", value, unified_value)
                logging.warning(msg)
            new_value = unified_value
        # Fix ISSNs without hyphen
        elif key in ["issn", "issn_print", "issn_electronic"]:
            new_value = value
            if re.match(r"^\d{7}[\dxX]$", value):
                new_value = value[:4] + "-" + value[4:]
                msg = "Line %s: " + MESSAGES["issn_hyphen_fix"]
                logging.warning(msg, row_num, key, value, new_value)
        else:
            new_value = value
    return new_value

def _isbn_lookup(current_row, row_num, additional_isbns, isbn_handling):
    collected_isbns = []
    for isbn_field in ["isbn", "isbn_print", "isbn_electronic"]:
        if has_value(current_row[isbn_field]):
            collected_isbns.append(current_row[isbn_field])
    for isbn in additional_isbns:
        if has_value(isbn):
            collected_isbns.append(isbn)
    if len(collected_isbns) == 0:
        msg = ("Line %s: Neither a DOI nor an ISBN found, assuming default record type " +
               "journal-article")
        logging.warning(msg, row_num)
        return (None, "journal-article")
    query_isbns = []
    for isbn in collected_isbns:
        res = isbn_handling.test_and_normalize_isbn(isbn)
        if not res["valid"]:
            msg = "Invalid ISBN {}: {}".format(isbn, ISBNHandling.ISBN_ERRORS[res["error_type"]])
            logging.warning(msg)
        else:
            query_isbns.append(res["input_value"])
            if res["input_value"] != res["normalised"]:
                query_isbns.append(res["normalised"])
    cr_res = find_book_dois_in_crossref(query_isbns)
    if not cr_res["success"]:
        msg = "Line %s: Error while trying to look up ISBNs in Crossref: %s"
        logging.error(msg, row_num, cr_res["error_msg"])
        return (None, "book")
    elif len(cr_res["dois"]) == 0:
        msg = "Line %s: Performed Crossref ISBN lookup, no DOI found."
        logging.info(msg, row_num)
        return (None, "book")
    elif len(cr_res["dois"]) > 1:
        msg = "Line %s: Performed Crossref ISBN lookup, more than one DOI found (%s) -> Used first in list."
        logging.warning(msg, row_num, str(cr_res["dois"]))
        return (cr_res["dois"][0], None)
    else:
        msg = "Line %s: Performed Crossref ISBN lookup, DOI found (%s)."
        logging.info(msg, row_num, cr_res["dois"][0])
        return (cr_res["dois"][0], None)

def _process_isbn(row_num, isbn, isbn_handling):
    if not has_value(isbn):
        return "NA"
    # handle a potential white-space split
    isbn = isbn.replace(" ", "")
    norm_res = isbn_handling.test_and_normalize_isbn(isbn)
    if norm_res["valid"]:
        if norm_res["normalised"] != norm_res["input_value"]:
            msg = "Line %s: Normalisation: ISBN value tested and split (%s -> %s)"
            logging.info(msg, row_num, norm_res["input_value"], norm_res["normalised"])
        return norm_res["normalised"]
    else:
        # in case of an invalid split: Use the correct one. In all other cases: Drop the value
        if norm_res["error_type"] == 4:
            unsplit_isbn = isbn.replace("-", "")
            new_res = isbn_handling.test_and_normalize_isbn(unsplit_isbn)
            msg = "Line %s: ISBN value had an invalid split, used the correct one (%s -> %s)"
            logging.info(msg, row_num, isbn, new_res["normalised"])
            return new_res["normalised"]
        else:
            msg = "Line %s: Invalid ISBN value (%s), set to NA (reason: %s)"
            logging.warning(msg, row_num, norm_res["input_value"],
                            ISBNHandling.ISBN_ERRORS[norm_res["error_type"]])
            return "NA"

def _process_institution_value(institution, row_num, orig_file_path):
    global INSTITUTIONS_PATH_MAP
    if INSTITUTIONS_PATH_MAP is None:
        INSTITUTIONS_PATH_MAP = _create_institution_map_dict("openapc_data_dir")
    path = os.path.dirname(orig_file_path)
    data_path = path.split("data/").pop()
    if data_path in INSTITUTIONS_PATH_MAP:
        new_value = INSTITUTIONS_PATH_MAP[data_path]["institution"]
        if new_value != institution:
            msg = "Line %s: Normalisation: Institution name replaced via mapping file ('%s' -> '%s')"
            logging.warning(msg, row_num, institution, new_value)
            return new_value
    return institution

def _process_agreement_value(agreement, row_num):
    global CONTRACTS_LOOKUP
    if CONTRACTS_LOOKUP is None:
        CONTRACTS_LOOKUP = ContractsLookup()
    global ESAC_HANDLING
    if ESAC_HANDLING is None:
        ESAC_HANDLING = ESACHandling()
    ret = {
        "consortium": "NA",
        "contract_name": "NA",
        "identifier": "NA"
    }
    identifier_dict = CONTRACTS_LOOKUP.get_by_identifier(agreement)
    if identifier_dict is not None: # agreement is an esac id
        ret["identifier"] = agreement
        ret["contract_name"] = identifier_dict["contract_name"][0]
        ret["consortium"] = identifier_dict["consortium"][0]
        msg = "Line %s: agreement '%s' found as identifier in contracts.csv"
        logging.info(msg, row_num, agreement)
        return ret
    contract_name_dict = CONTRACTS_LOOKUP.get_by_contract_name(agreement)
    if contract_name_dict is not None:
        identifiers = contract_name_dict["identifier"]
        if len(identifiers) > 1:
            msg = "Line %s: agreement '%s' found as contract_name in contracts.csv, but the identifier is not unique (%s)"
            logging.error(msg, row_num, agreement, ", ".join(identifiers))
            return ret
        ret["identifier"] = contract_name_dict["identifier"][0]
        ret["contract_name"] = agreement
        ret["consortium"] = contract_name_dict["consortium"][0]
        msg = "Line %s: agreement '%s' found as contract_name in contracts.csv (identifier: %s)"
        logging.info(msg, row_num, agreement, ret["identifier"])
        return ret
    esac_entry = ESAC_HANDLING.get_esac_entry(agreement)
    if esac_entry is not None:
        publisher = esac_entry["Publisher"]
        if esac_entry["Publisher_OAPC"] != "":
            publisher = esac_entry["Publisher_OAPC"]
        contract_name = "{} {} agreement".format(esac_entry["Organization"], publisher)
        msg = "Line %s: agreement '%s' found in ESAC Registry, contract_name constructed from ESAC data: '%s'"
        logging.info(msg, row_num, agreement, contract_name)
        ret["identifier"] = agreement
        ret["contract_name"] = contract_name
        ret["consortium"] = esac_entry["Organization"]
        return ret
    ret["contract_name"] = agreement
    msg = "Line %s: agreement '%s' not found in contracts.csv or ESAC registry, value will be used as is"
    logging.info(msg, row_num, agreement)
    return ret

def _create_institution_map_dict(map_type):
    types = ["institution", "openapc_data_dir"]
    if map_type not in types:
        raise Exception("Invalid parameter for _create_institution_map_dict, must be one of: " + ", ".join(types))
    with open(INSTITUTIONS_FILE, "r") as ins_file:
        ret_dict = {}
        reader = csv.DictReader(ins_file)
        for line in reader:
            key = line[map_type]
            if has_value(key):
                ret_dict[key] = line
    return ret_dict

def _obtain_group_id(row, row_num):
    global CONTRACTS_LOOKUP
    if CONTRACTS_LOOKUP is None:
        CONTRACTS_LOOKUP = ContractsLookup()
    global INSTITUTIONS_NAME_MAP
    if INSTITUTIONS_NAME_MAP is None:
        INSTITUTIONS_NAME_MAP = _create_institution_map_dict("institution")
    ret = {
        "created": False,
        "group_id": "NA"
    }
    institution_entry = INSTITUTIONS_NAME_MAP.get(row["institution"])
    if institution_entry is None:
        msg = ("Line %s: Institution '%s' not present in institutions file, could not not obtain ROR for group_id generation")
        logging.error(msg, row_num, row["institution"])
        return ret
    ror = institution_entry["ror_id"]
    if not has_value(ror):
        msg = ("Line %s: Institution '%s' does not have a ROR ID in institutions file, using the cubes name instead")
        logging.warning(msg, row_num, row["institution"])
        ror = institution_entry["institution_cubes_name"]
    else:
        ror = ror[16:]
    identifier = row["identifier"]
    if not has_value(identifier):
        identifier = row["contract_name"]
    period = row["period"]
    group_id = ror + "_" + identifier + "_" + str(period)
    ret["group_id"] = group_id
    if CONTRACTS_LOOKUP.get_by_group_id(group_id) is not None:
        msg = ("Line %s: group_id '%s' already present in contracts.csv, article will be linked to this existing contract data")
        logging.warning(msg, row_num, group_id)
        return ret
    ret["created"] = True
    return ret

def process_row(row, row_num, column_map, num_required_columns, additional_isbn_columns,
                doab_analysis, doaj_analysis, issnl_handling=None, no_crossref_lookup=False, no_pubmed_lookup=False,
                no_doaj_lookup=False, no_title_lookup=False, preprint_auto_accept=False, 
                round_monetary=False, ta_mode=False, orig_file_path=None, crossref_max_retries=3):
    """
    Enrich a single row of data and reformat it according to OpenAPC standards.

    Take a csv row (a list) and a column mapping (a dict of CSVColumn objects)
    and return an enriched and re-arranged version which conforms to the Open
    APC data schema. The method will decide on which data schema to use depending
    on the identified publication type and possible flags.

    Args:
        row: A list of column values (as yielded by a UnicodeReader f.e.).
        row_num: The line number in the csv file, for logging purposes.
        column_map: A dict of CSVColumn Objects, mapping the row
                    cells to OpenAPC data schema fields.
        num_required_columns: An int describing the required length of the row
                              list. If not matched, an error is logged and the
                              row is returned unchanged.
        additional_isbn_columns: A list of ints designating row indexes as additional ISBN sources.
        doab_analysis: A DOABanalysis object to perform an offline DOAB lookup
        doaj_analysis: A DOAJAnalysis object to perform offline DOAJ lookups
        issnl_handling: An ISSNLHandling object to perform ISSN-L enrichment
        no_crossref_lookup: If true, no metadata will be imported from crossref.
        no_pubmed_lookup: If true, no_metadata will be imported from pubmed.
        no_doaj_lookup: If true, journals will not be checked for being
                        listended in the DOAJ.
        no_title_lookup: If true, titles will not be looked up in Crossref
        preprint_auto_accept: If true, DOIs for preprint lookups will be automatically accepted
                              if the match quality is high enough (title similarity => 0.9). Only
                              has an effect if no_title_lookup is False.
        round_monetary: If true, monetary values with more than 2 digits behind the decimal
                        mark will be rounded. If false, these cases will be treated as errors.
        ta_mode: If true, the row is assumed to originate from a ta article file and the according
                 data schema will be applied.
        crossref_max_retries: Max number of attempts to query the crossref API if a 504 error
                              is received.
        orig_file_path: Path of the csv file this row originates from, can be used for
                        automated institution name lookup.
     Returns:
        A list of values which represents the enriched and re-arranged variant
        of the input row. If no errors were logged during the process, this
        result will conform to the OpenAPC data schema.
    """
    if len(row) != num_required_columns:
        msg = "Line %s: " + MESSAGES["num_columns"]
        logging.error(msg, row_num, len(row), num_required_columns)
        return row

    empty_row = True
    for elem in row:
        if has_value(elem):
            empty_row = False
            break
    else:
        msg = "Line %s: " + MESSAGES["empty_row"]
        logging.warning(msg, row_num)

    current_row = {}
    record_type = None

    # Copy content of identified columns and apply special processing rules
    for csv_column in column_map.values():
        index, column_type = csv_column.index, csv_column.column_type
        if empty_row:
            current_row[column_type] = ""
            continue
        req = csv_column.requirement
        if column_type == "euro" and index is not None:
            current_row["euro"] = _process_euro_value(row[index], round_monetary, row_num, index, ta_mode, False)
        elif req["articles"] == CSVColumn.ADDITIONAL_COSTS or req["ta"] == CSVColumn.ADDITIONAL_COSTS and index is not None:
            current_row[column_type] = _process_euro_value(row[index], round_monetary, row_num, index, None, True)
        elif column_type == "period" and index is not None:
            current_row["period"] = _process_period_value(row[index], row_num)
        elif column_type == "is_hybrid" and index is not None:
            current_row["is_hybrid"] = _process_hybrid_status(row[index], row_num)
        elif column_type == "institution" and index is not None:
            current_row["institution"] = _process_institution_value(row[index], row_num, orig_file_path)
        elif column_type == "agreement" and index is not None and ta_mode:
            agreement_data = _process_agreement_value(row[index], row_num)
            current_row["identifier"] = agreement_data["identifier"]
            current_row["contract_name"] = agreement_data["contract_name"]
            current_row["consortium"] = agreement_data["consortium"]
            if has_value(agreement_data["identifier"]):
                current_row["agreement"] = agreement_data["identifier"]
            else:
                current_row["agreement"] = agreement_data["contract_name"]
        else:
            if index is not None and len(row[index]) > 0:
                current_row[column_type] = row[index]
            else:
                current_row[column_type] = "NA"

    doi = current_row["doi"]
    if not has_value(doi) and not empty_row:
        msg = ("Line %s: No DOI found")
        logging.info(msg, row_num)
        current_row["indexed_in_crossref"] = "FALSE"
        # lookup ISBNs in crossref
        additional_isbns = [row[i] for i in additional_isbn_columns]
        found_doi, r_type = _isbn_lookup(current_row, row_num, additional_isbns, doab_analysis.isbn_handling)
        if r_type is not None:
            record_type = r_type
        if found_doi is not None:
            # integrate DOI into row and restart
            logging.info("New DOI integrated, restarting enrichment for current line.")
            index = column_map["doi"].index
            row[index] = found_doi
            return process_row(row, row_num, column_map, num_required_columns, additional_isbn_columns,
                doab_analysis, doaj_analysis, issnl_handling, no_crossref_lookup, no_pubmed_lookup,
                no_doaj_lookup, no_title_lookup, preprint_auto_accept, round_monetary, offsetting_mode, orig_file_path)
        # lookup the book title in Crossref
        lookup_title = current_row["book_title"]
        if has_value(lookup_title):
            msg = ("Line %s: Trying to look up the book title ('%s') in Crossref...")
            logging.info(msg, row_num, lookup_title)
            book_doi = title_lookup(lookup_title, ["book", "monograph", "reference-book"])
            if book_doi:
                logging.info("New DOI integrated, restarting enrichment for current line.")
                index = column_map["doi"].index
                row[index] = book_doi
                return process_row(row, row_num, column_map, num_required_columns, additional_isbn_columns,
                    doab_analysis, doaj_analysis, issnl_handling, no_crossref_lookup, no_pubmed_lookup,
                    no_doaj_lookup, no_title_lookup, preprint_auto_accept, round_monetary, offsetting_mode, orig_file_path)
    if has_value(doi):
        # Normalise DOI
        norm_doi = get_normalised_DOI(doi)
        if norm_doi is not None and norm_doi != doi:
            current_row["doi"] = norm_doi
            msg = MESSAGES["doi_norm"].format(doi, norm_doi)
            logging.info(msg)
            doi = norm_doi
        # include crossref metadata
        if not no_crossref_lookup:
            crossref_result = get_metadata_from_crossref(doi)
            retries = 0
            while not crossref_result["success"] and crossref_result["error_msg"].startswith("HTTPError: 504"):
                if retries >= crossref_max_retries:
                    break
                # retry on gateway timeouts, crossref API is quite busy sometimes
                msg = "%s, retrying..."
                logging.warning(msg, crossref_result["error_msg"])
                retries += 1
                crossref_result = get_metadata_from_crossref(doi)
            if not crossref_result["success"]:
                exc = crossref_result["exception"]
                # check if a preprint lookup is possible
                if not no_title_lookup and type(exc) == UnsupportedDoiTypeError and exc.doi_type == "posted-content":
                    msg = ("Line %s: Found a DOI with type 'posted_content' (%s). This might " +
                           "be a case of a preprint DOI, trying to find the final version of the article...")
                    logging.info(msg, row_num, doi)
                    if not exc.crossref_title:
                        msg = "Line %s: Preprint lookup failed, no title could be extracted."
                        logging.warning(msg, row_num)
                    else:
                        article_doi = title_lookup(exc.crossref_title, ["journal-article"], preprint_auto_accept)
                        if article_doi:
                            logging.info("New DOI integrated, restarting enrichment for current line...")
                            index = column_map["doi"].index
                            row[index] = article_doi
                            return process_row(row, row_num, column_map, num_required_columns, additional_isbn_columns,
                                doab_analysis, doaj_analysis, issnl_handling, no_crossref_lookup, no_pubmed_lookup,
                                no_doaj_lookup, no_title_lookup, preprint_auto_accept, round_monetary, offsetting_mode, orig_file_path)
            if crossref_result["success"]:
                data = crossref_result["data"]
                record_type = data.pop("doi_type")
                logging.info("Crossref: DOI resolved: " + doi + " [" + record_type + "]")
                current_row["indexed_in_crossref"] = "TRUE"
                for key, value in data.items():
                    new_value = _process_crossref_results(current_row, row_num, key, value)
                    old_value = current_row[key]
                    current_row[key] = column_map[key].check_overwrite(old_value, new_value)
            else:
                msg = "Line %s: Crossref: Error while trying to resolve DOI %s: %s"
                logging.error(msg, row_num, doi, crossref_result["error_msg"])
                current_row["indexed_in_crossref"] = "FALSE"
                # lookup ISBNs in crossref and try to find a correct DOI
                additional_isbns = [row[i] for i in additional_isbn_columns]
                found_doi, r_type = _isbn_lookup(current_row, row_num, additional_isbns, doab_analysis.isbn_handling)
                if r_type is not None:
                    record_type = r_type
                if found_doi is not None:
                    # integrate DOI into row and restart
                    logging.info("New DOI integrated, restarting enrichment for current line.")
                    index = column_map["doi"].index
                    row[index] = found_doi
                    return process_row(row, row_num, column_map, num_required_columns, additional_isbn_columns,
                                       doab_analysis, doaj_analysis, issnl_handling, no_crossref_lookup, no_pubmed_lookup,
                                       no_doaj_lookup, no_title_lookup, preprint_auto_accept, round_monetary, offsetting_mode, orig_file_path)
        # include a possible ISSN-L
        if issnl_handling is not None and record_type == "journal-article":
            for issn_field in ["issn", "issn_print", "issn_electronic"]:
                issnl = issnl_handling.get_issnl(current_row[issn_field])
                if issnl is not None:
                    current_row["issn_l"] = issnl
                    break
        # include pubmed metadata
        if not no_pubmed_lookup and record_type == "journal-article":
            pubmed_result = get_metadata_from_pubmed(doi)
            if pubmed_result["success"]:
                logging.info("Pubmed: DOI resolved: " + doi)
                data = pubmed_result["data"]
                for key, value in data.items():
                    if value is not None:
                        new_value = value
                    else:
                        new_value = "NA"
                        msg = "WARNING: Element %s not found in in response for doi %s."
                        logging.debug(msg, key, doi)
                    old_value = current_row[key]
                    current_row[key] = column_map[key].check_overwrite(old_value, new_value)
            else:
                msg = "Line %s: Pubmed: Error while trying to resolve DOI %s: %s"
                logging.error(msg, row_num, doi, pubmed_result["error_msg"])

    # lookup in DOAJ. try the EISSN first, then ISSN and finally print ISSN
    if not no_doaj_lookup and not empty_row:
        issns = []
        new_value = "NA"
        if current_row["issn_electronic"] != "NA":
            issns.append(current_row["issn_electronic"])
        if current_row["issn"] != "NA":
            issns.append(current_row["issn"])
        if current_row["issn_print"] != "NA":
            issns.append(current_row["issn_print"])
        for issn in issns:
            lookup_result = doaj_analysis.lookup(issn)
            if lookup_result:
                msg = "DOAJ: Journal ISSN (%s) found in DOAJ offline copy ('%s')."
                logging.info(msg, issn, lookup_result)
                new_value = "TRUE"
                break
            else:
                msg = "DOAJ: Journal ISSN (%s) not found in DOAJ offline copy."
                new_value = "FALSE"
                logging.info(msg, issn)
        old_value = current_row["doaj"]
        current_row["doaj"] = column_map["doaj"].check_overwrite(old_value, new_value)
    if record_type != "journal-article" and not empty_row:
        collected_isbns = []
        for isbn_field in ["isbn", "isbn_print", "isbn_electronic"]:
            # test and split all ISBNs
            current_row[isbn_field] = _process_isbn(row_num, current_row[isbn_field], doab_analysis.isbn_handling)
            if has_value(current_row[isbn_field]):
                collected_isbns.append(current_row[isbn_field])
        additional_isbns = [row[i] for i in additional_isbn_columns]
        for isbn in additional_isbns:
            result = _process_isbn(row_num, isbn, doab_analysis.isbn_handling)
            if has_value(result):
                collected_isbns.append(result)
        if len(collected_isbns) == 0:
            logging.info("No ISBN found, skipping DOAB lookup.")
            current_row["doab"] = "NA"
        else:
            record_type = "book"
            logging.info("Trying a DOAB lookup with the following values: " + str(collected_isbns))
            for isbn in collected_isbns:
                doab_result = doab_analysis.lookup(isbn)
                if doab_result is not None:
                    current_row["doab"] = "TRUE"
                    msg = 'DOAB: ISBN %s found in normalized DOAB (%s, "%s")'
                    logging.info(msg, isbn, doab_result["publisher"], doab_result["book_title"])
                    if current_row["indexed_in_crossref"] == "TRUE":
                        msg = "Book already found in Crossref via DOI, those results take precedence"
                        logging.info(msg)
                    else:
                        for key in doab_result:
                            current_row[key] = doab_result[key]
                    if not has_value(current_row["isbn"]):
                        current_row["isbn"] = isbn
                    break
            else:
                current_row["doab"] = "FALSE"
                msg = "DOAB: None of the ISBNs found in DOAB"
                logging.info(msg)
    if ta_mode:
        record_type = "journal-article_transagree"
        current_row["period_from"] = current_row["period"]
        current_row["period_to"] = current_row["period"]
        current_row["cost_type"] = "NA"
        group_id_creation = _obtain_group_id(current_row, row_num)
        current_row["group_id"] = group_id_creation["group_id"]

    if record_type is None:
        msg = "Line %s: Could not identify record type, using default schema 'journal-article'"
        logging.warning(msg, row_num)
        record_type = "journal-article"

    result = []
    for field in COLUMN_SCHEMAS[record_type]:
        result.append(current_row[field])

    for _, column in column_map.items():
        if column.column_type == "added_unknown_column":
            result.append(row[column.index])

    ret = {record_type: result}

    additional_cost_data = False
    for csv_column in column_map.values():
        req = csv_column.requirement
        if csv_column.requirement["articles"] == CSVColumn.ADDITIONAL_COSTS:
            additional_cost_data = True
            break
        elif ta_mode and csv_column.requirement["ta"] == CSVColumn.ADDITIONAL_COSTS:
            additional_cost_data = True
            break

    if additional_cost_data:
        ret["additional_costs"] = []
        for field in COLUMN_SCHEMAS["additional_costs"]:
            if field in current_row:
                ret["additional_costs"].append(current_row[field])
            else:
                ret["additional_costs"].append("NA")

    # only write a contracts line if a group_id could be created in the first place
    if ta_mode and group_id_creation["created"]:
        ret["contracts"] = []
        for field in COLUMN_SCHEMAS["contracts"]:
            if field == "euro": # Do not copy article-level costs to contracts...
                  ret["contracts"].append("NA")
            else:
                ret["contracts"].append(current_row[field])

    return ret

def get_hybrid_status_from_whitelist(hybrid_status):
    """
    Obtain a boolean identifier for journal hybrid status by looking up possible
    synonyms in a whitelist.
    Args:
        hybrid status: A string describing the hybrid status of a journal.
    Returns:
        An OpenAPC-normalised boolean identifer (TRUE/FALSE) if the designation was found
        in a whitelist.
    """
    for boolean_value, whitelist in mappings.HYBRID_STATUS.items():
        if hybrid_status.strip().lower() in whitelist:
            return boolean_value
    return None

def get_column_type_from_whitelist(column_name):
    """
    Identify a CSV column type by looking up the name in a whitelist.

    Args:
        column_name: Name of a CSV column, usually extracted from the header.
    Returns:
        An APC-normed column type (as a string) if the column name was found in
        a whitelist, None otherwise.
    """
    for key, whitelist in mappings.COLUMN_NAMES.items():
        if column_name.strip().lower() in whitelist:
            return key
    return None

def get_unified_publisher_name(publisher):
    """
    Unify certain publisher names via a mapping table.

    CrossRef data is sometimes inconsistent when it comes to publisher names,
    these cases can be solved by returning a unified name from a mapping table.

    Args:
        publisher: A publisher as it is returned from the CrossRef API.
    Returns:
        Either a unified name or the original name as a string
    """
    return mappings.PUBLISHER_MAPPINGS.get(publisher, publisher)

def get_unified_journal_title(journal_full_title):
    """
    Unify certain journal titles via a mapping table.

    CrossRef data is sometimes inconsistent when it comes to journal titles,
    these cases can be solved by returning a unified name from a mapping table.

    Args:
        journal_full_title: A journal title as it is returned from the CrossRef API.
    Returns:
        Either a unified name or the original name as a string
    """

    return mappings.JOURNAL_MAPPINGS.get(journal_full_title, journal_full_title)

def get_corrected_issn_l(issn_l):
    return mappings.ISSN_L_CORRECTIONS.get(issn_l, issn_l)

def colorize(text, color):
    ANSI_COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "magenta": "\033[95m"
    }
    if color not in ANSI_COLORS:
        return text
    return ANSI_COLORS[color] + text + "\033[0m"

def print_b(text):
    print(colorize(text, "blue"))

def print_g(text):
    print(colorize(text, "green"))

def print_r(text):
    print(colorize(text, "red"))

def print_y(text):
    print(colorize(text, "yellow"))

def print_c(text):
    print(colorize(text, "cyan"))

def print_m(text):
    print(colorize(text, "magenta"))
