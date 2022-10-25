# -*- coding: UTF-8 -*-

import csv
import os
import sys
import re
import time
import threading

import pytest
import requests
from warnings import warn

from .test_apc_csv import RowObject, DATA_FILES

sys.path.append(os.path.join(sys.path[0], "python"))
import openapc_toolkit as oat

# Contains list of rows in the institutions and translation files, encapsulated as RowObject
DATA = {
    "institutions": [],
    "translation_countries": [],
    "translation_institution_groups": [],
    "translation_institution_types": []
}

# List of all OpenAPC institutional identifiers (as strings)
INSTITUTIONS = []

# List of all institutional identifiers (as strings) in the apc_de file
INSTITUTIONS_APC_DE = []

# List of all ROR IDs
ROR_IDS = []

ROR_ID_REGEX = re.compile(r"https:\/\/ror.org\/[a-z0-9]{9}")

# Holds all currently active URLRequestThreads
THREAD_POOL = []
# Maximum number of parallel threads
THREAD_POOL_SIZE = 10

FINISHED_THREADS = []

# Prefix for all error messages
MSG_HEAD = "{}, line {}: "

# Number of expected columns in the institutions file 
EXP_ROW_LENGTH = 12

class URLRequestThread(threading.Thread):
    """
    Make a threaded request to the info_url and report non-200 status codes

    Args:
        row_object: A test_apc_csv.RowObject which encapsulates information
        on a single row from the institutions table.
    """

    # spoof the user agent to avoid being rejected by some sites
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    def __init__(self, row_object):
        # assigning a name is not strictly necessary, but can useful for debugging purposes
        super().__init__(name = row_object.row[1] + "_thread")
        self.row_object = row_object
        self.url = row_object.row[10]
        self.status_code = None

    def run(self):
        response = requests.get(self.url, timeout=10, headers=URLRequestThread.headers)
        # Are there other codes besides 200 which indicate a success? Wait and see.
        if response.status_code != 200:
            self.status_code = response.status_code

def _cleanup_thread_pool():
    """
    Clean up the THREAD_POOL.

    Threads which are no longer alive (which means their run()
    method has finished) are moved to FINISHED_THREADS.
    """
    global THREAD_POOL, FINISHED_THREADS
    still_running = []
    for thread in THREAD_POOL:
        if thread.is_alive():
            still_running.append(thread)
        else:
            FINISHED_THREADS.append(thread)
    THREAD_POOL = still_running

def run_url_threads():
    """
    Create parallel URLRequestThreads for all info_urls and start them.

    Fill up the THREAD_POOL with threads, then clean them up in regular
    intervals and add new ones whenever there's room.
    Unfortunately we cannot make calls to pytest.fail() directly in a
    thread's run() method as this would interfere with the built-in
    exception handling of the Thread class. We have to do the
    thread runs before the other tests and store the results (finished
    threads) in the FINISHED_THREADS list. We can then parametrize
    over this list later (test_info_urls) to generate readable error
    reports.
    """
    global THREAD_POOL
    for row_object in DATA["institutions"]:
        if oat.has_value(row_object.row[10]):
            thread = URLRequestThread(row_object)
            while len(THREAD_POOL) >= THREAD_POOL_SIZE:
                _cleanup_thread_pool()
                time.sleep(0.2)
            THREAD_POOL.append(thread)
            thread.start()
    # Wait until all threads have finished
    while len(THREAD_POOL) > 0:
        _cleanup_thread_pool()
        time.sleep(0.2)

# Prepare the test data
for data_file, metadata in DATA_FILES.items():
    with open(metadata["file_path"], "r") as f:
        reader = csv.reader(f)
        reader.__next__() # skip the header
        for row in reader:
            if row[0] not in INSTITUTIONS:
                INSTITUTIONS.append(row[0])
            if data_file == "apc" and row[0] not in INSTITUTIONS_APC_DE:
                INSTITUTIONS_APC_DE.append(row[0])
for base_name, data in DATA.items():
    file_path = os.path.join("data", base_name + ".csv")
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        reader.__next__()
        for row in reader:
            # Use RowObject to store contextual information along with CSV rows for better error messages
            row_object = RowObject(base_name, reader.line_num, row, None)
            data.append(row_object)
run_url_threads()

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_data_format(row_object):
    if len(row_object.row) != EXP_ROW_LENGTH:
        msg = MSG_HEAD + "Row does not consist of {} columns."
        msg = msg.format(row_object.file_name, row_object.line_number, EXP_ROW_LENGTH)
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_data_dirs(row_object):
    data_dir = row_object.row[6]
    if oat.has_value(data_dir):
        if not os.path.isdir(os.path.join("data", data_dir)):
            msg = MSG_HEAD + "Directory '{}' does not exist."
            msg = msg.format(row_object.file_name, row_object.line_number, data_dir)
            pytest.fail(msg)

@pytest.mark.parametrize("thread", FINISHED_THREADS)
def test_info_urls(thread):
    if thread.status_code is not None:
        msg = MSG_HEAD + "HTTP request to '{}' returned status code {}"
        msg = msg.format(thread.row_object.file_name, thread.row_object.line_number, thread.url, thread.status_code)
        warn(msg)

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_cubes_names(row_object):
    institution = row_object.row[0]
    cubes_name = row_object.row[1]
    if not oat.has_value(cubes_name) and institution in INSTITUTIONS_APC_DE:
        msg = MSG_HEAD + "Institution '{}' occurs in the apc_de file, but the cubes name is empty."
        msg = msg.format(row_object.file_name, row_object.line_number, institution)
        pytest.fail(msg)
    if oat.has_value(cubes_name) and not institution in INSTITUTIONS_APC_DE:
        msg = MSG_HEAD + "A cubes name was assigned for institution '{}', but it has no entries in the apc_de file."
        msg = msg.format(row_object.file_name, row_object.line_number, institution)
        pytest.fail(msg)
    if re.compile(r"\s").search(cubes_name):
        msg = MSG_HEAD + "Cube name '{}' contains whitespace characters."
        msg = msg.format(row_object.file_name, row_object.line_number, cubes_name)
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_ror_ids(row_object):
    global ROR_IDS
    ror_id = row_object.row[7]
    if oat.has_value(ror_id):
        if not ROR_ID_REGEX.match(ror_id):
            msg = MSG_HEAD + "ROR ID '{}' is not well-formed."
            msg = msg.format(row_object.file_name, row_object.line_number, ror_id)
            pytest.fail(msg)
        if ror_id not in ROR_IDS:
            ROR_IDS.append(ror_id)
        else:
            msg = MSG_HEAD + "ROR ID '{}' occurs more than once."
            msg = msg.format(row_object.file_name, row_object.line_number, ror_id)
            pytest.fail(msg)

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_institution_file_identifiers(row_object):
    institution = row_object.row[0]
    if not oat.has_value(institution):
        msg = MSG_HEAD + "Institution identifier is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)
    if institution not in INSTITUTIONS:
        msg = MSG_HEAD + "Institution identifier '{}' does not occur in any data set."
        msg = msg.format(row_object.file_name, row_object.line_number, institution)
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_geo_data(row_object):
    continent = row_object.row[3]
    country = row_object.row[4]
    state = row_object.row[5]
    cubes_name = row_object.row[1]
    if not oat.has_value(country):
        msg = MSG_HEAD + "Country column is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)
    if oat.has_value(cubes_name):
        if not oat.has_value(continent):
            msg = MSG_HEAD + "A cubes name was assigned ({}), but the continent column is empty."
            msg = msg.format(row_object.file_name, row_object.line_number, cubes_name)
            pytest.fail(msg)
        if not oat.has_value(state):
            msg = MSG_HEAD + "A cubes name was assigned ({}), but the state column is empty."
            msg = msg.format(row_object.file_name, row_object.line_number, cubes_name)
            pytest.fail(msg)

@pytest.mark.parametrize("row_object", DATA["institutions"])
def test_translations(row_object):
    country = row_object.row[4]
    ins_type = row_object.row[8]
    ins_group = row_object.row[9]
    if oat.has_value(country):
        for row_object in DATA["translation_countries"]:
            if row_object.row and country == row_object.row[0]:
                break
        else:
            msg = "country '{}' does not have an entry in the translation_countries file."
            msg = msg.format(country)
            pytest.fail(msg)
    if oat.has_value(ins_type):
        for row_object in DATA["translation_institution_types"]:
            if row_object.row and ins_type == row_object.row[0]:
                break
        else:
            msg = "type '{}' does not have an entry in the translation_institution_types file."
            msg = msg.format(ins_type)
            pytest.fail(msg)
    if oat.has_value(ins_group):
        for row_object in DATA["translation_institution_groups"]:
            if row_object.row and ins_group == row_object.row[0]:
                break
        else:
            msg = "group '{}' does not have an entry in the translation_institution_groups file."
            msg = msg.format(ins_group)
            pytest.fail(msg)

@pytest.mark.parametrize("institution", INSTITUTIONS)
def test_apc_file_identifiers(institution):
    for row_object in DATA["institutions"]:
        # There are more efficient ways to do this (f.e. assert set() == set()),
        # but those would not produce easily readable error messages
        if institution == row_object.row[0]:
            break
    else:
        msg = "institutional identifier '{}' does not occur in institution file."
        msg = msg.format(institution)
        pytest.fail(msg)
