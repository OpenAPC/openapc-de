# -*- coding: UTF-8 -*-

import os
from urllib.request import urlretrieve

import pytest

from .. import openapc_toolkit as oat

CORRECT_ISBN_SPLITS = {
    "9782753518278": "978-2-7535-1827-8",
    "9780815726890": "978-0-8157-2689-0",
    "9788496820524": "978-84-96820-52-4",
    "9783837633269": "978-3-8376-3326-9",
    "9781947172395": "978-1-947172-39-5",
    "9788877137531": "978-88-7713-753-1",
    "9789289342582": "978-92-893-4258-2",
    "9789932021789": "978-9932-02-178-9",
    "9780472131792": "978-0-472-13179-2"
}

INVALID_ISBNS = [
    "97827535182784", # too long
    "978275351827", # too short
    "978275351827A", # not all digits
    "9772753518278", # invalid EAN prefix
    "9786712345678", # undefined registration group range for prefix 978
    "9786219123456" # undefined registrant range (9xxxxxx) for registration group 978-621 (Philippines)
]

INVALID_CHECK_DIGITS = [
    "9782753518279",
    "9780815726892",
    "9788496820523",
    "9783837633265",
    "9781947172399",
    "9788877137530",
    "9789289342588",
    "9789932021783"
]

@pytest.fixture(scope="module")
def range_file():
    index = 0
    tempfile_name = "TempRangeMessage.xml"
    while os.path.isfile(tempfile_name):
        index += 1
        tempfile_name = "TempRangeMessage_" + str(index) + ".xml"
    print('\nDownloading temporary RangeMessage file to "' + tempfile_name + '"...')
    urlretrieve("http://www.isbn-international.org/export_rangemessage.xml", tempfile_name)
    yield tempfile_name
    print('\nRemoving temporary RangeMessage file "' + tempfile_name + '"...')
    os.remove(tempfile_name)

def test_isbn_splits(range_file):
    for isbn, split_result in CORRECT_ISBN_SPLITS.items():
        result = oat.split_isbn(isbn, range_file)
        assert result["success"] == True
        assert result["value"] == split_result

def test_isbn_split_fails(range_file):
    for invalid_isbn in INVALID_ISBNS:
        result = oat.split_isbn(invalid_isbn, range_file)
        assert result["success"] == False
        
def test_check_digit_verification():
    for isbn in CORRECT_ISBN_SPLITS.keys():
        assert oat.isbn_has_valid_check_digit(isbn)
    for isbn in INVALID_CHECK_DIGITS:
        assert not oat.isbn_has_valid_check_digit(isbn)
