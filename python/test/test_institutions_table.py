# -*- coding: UTF-8 -*-

import csv
import os
import sys
import re
import time
import threading

import pytest
import requests

from .test_apc_csv import RowObject, DATA_FILES

sys.path.append(os.path.join(sys.path[0], "python"))
import openapc_toolkit as oat

INSTITUTIONS_FILE_PATH = "data/institutions.csv"
# List of all rows in the institutions table, encapsulated as RowObject
INSTITUTIONS_DATA = []
# List of all institution identifiers in the APC data set (as strings)
APC_INSTITUTIONS = []

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
    for row_object in INSTITUTIONS_DATA:
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
with open(DATA_FILES["apc"]["file_path"], "r") as f:
    reader = csv.reader(f)
    reader.__next__() # skip the header
    for row in reader:
        if row[0] not in APC_INSTITUTIONS:
            APC_INSTITUTIONS.append(row[0])
with open(INSTITUTIONS_FILE_PATH, "r") as f:
    reader = csv.reader(f)
    reader.__next__()
    for row in reader:
        # Use RowObject to store contextual information along with CSV rows for better error messages
        row_object = RowObject("institutions.csv", reader.line_num, row, None)
        INSTITUTIONS_DATA.append(row_object)
    run_url_threads()

@pytest.mark.parametrize("row_object", INSTITUTIONS_DATA)
def test_data_format(row_object):
    if len(row_object.row) != EXP_ROW_LENGTH:
        msg = MSG_HEAD + "Row does not consist of {} columns."
        msg = msg.format(row_object.file_name, row_object.line_number, EXP_ROW_LENGTH)
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", INSTITUTIONS_DATA)
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
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", INSTITUTIONS_DATA)
def test_cube_names(row_object):
    cube_name = row_object.row[1]
    if not oat.has_value(cube_name):
        msg = MSG_HEAD + "Cube name is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)
    if re.compile(r"\s").search(cube_name):
        msg = MSG_HEAD + "Cube name '{}' contains whitespace characters."
        msg = msg.format(row_object.file_name, row_object.line_number, cube_name)
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", INSTITUTIONS_DATA)
def test_institution_file_identifiers(row_object):
    institution = row_object.row[0]
    if not oat.has_value(institution):
        msg = MSG_HEAD + "Institution identifier is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)
    if institution not in APC_INSTITUTIONS:
        msg = MSG_HEAD + "Institution identifier '{}' does not occur in APC data set."
        msg = msg.format(row_object.file_name, row_object.line_number, institution)
        pytest.fail(msg)

@pytest.mark.parametrize("row_object", INSTITUTIONS_DATA)
def test_geo_data(row_object):
    continent = row_object.row[3]
    country = row_object.row[4]
    state = row_object.row[5]
    if not oat.has_value(continent):
        msg = MSG_HEAD + "Continent column is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)
    if not oat.has_value(country):
        msg = MSG_HEAD + "Country column is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)
    if not oat.has_value(state):
        msg = MSG_HEAD + "State column is empty."
        msg = msg.format(row_object.file_name, row_object.line_number)
        pytest.fail(msg)

@pytest.mark.parametrize("institution", APC_INSTITUTIONS)
def test_apc_file_identifiers(institution):
    for row_object in INSTITUTIONS_DATA:
        # There are more efficient ways to do this (f.e. assert set() == set()),
        # but those would not produce easily readable error messages
        if institution == row_object.row[0]:
            break
    else:
        msg = "APC data identifier '{}' does not occur in institution file."
        msg = msg.format(institution)
        pytest.fail(msg)
