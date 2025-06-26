# -*- coding: UTF-8 -*-

import os
from sys import path
from urllib.request import urlretrieve

import pytest

path.append(os.path.join(path[0], "python"))
import openapc_toolkit as oat

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

NORMALIZATION_TESTS = {
    "978-1-4780-0716-6": { # valid split
        "valid": True,
        "input_value": "978-1-4780-0716-6",
        "normalised": "978-1-4780-0716-6"
    },
    "9783848760510": { # valid unsplit
        "valid": True,
        "input_value": "9783848760510",
        "normalised": "978-3-8487-6051-0"
    },
    "978-10-4780-0716-6": { # invalid split, too long
        "valid": False,
        "input_value": "978-10-4780-0716-6",
        "error_type": 2
    },
    "978-1-478-0716-6": { # invalid split, too short
        "valid": False,
        "input_value": "978-1-478-0716-6",
        "error_type": 1
    },
    "978-14-780-0716-6": { # invalid split, wrong segmenation
        "valid": False,
        "input_value": "978-14-780-0716-6",
        "error_type": 3
    },
    "97838487605109": { # invalid unsplit, too long
        "valid": False,
        "input_value": "97838487605109",
        "error_type": 0
    },
}

@pytest.fixture(scope="module")
def isbn_handling():
    yield oat.ISBNHandling(temp_file_dir=".", force_update=True, make_backup=True, verbose=True)
    print('\nRemoving temporary RangeMessage file "ISBNRangeFile.xml"...')
    os.remove("ISBNRangeFile.xml")

@pytest.mark.parametrize("isbn, split_result", CORRECT_ISBN_SPLITS.items())
def test_isbn_splits(isbn, split_result, isbn_handling):
    result = isbn_handling.split_isbn(isbn)
    assert result["success"] == True
    assert result["value"] == split_result

@pytest.mark.parametrize("invalid_isbn", INVALID_ISBNS)
def test_isbn_split_fails(invalid_isbn, isbn_handling):
    result = isbn_handling.split_isbn(invalid_isbn)
    assert result["success"] == False

@pytest.mark.parametrize("isbn", CORRECT_ISBN_SPLITS.keys())
def test_valid_check_digits(isbn, isbn_handling):
    assert isbn_handling.isbn_has_valid_check_digit(isbn)
      
@pytest.mark.parametrize("isbn", INVALID_CHECK_DIGITS)
def test_invalid_check_digits(isbn, isbn_handling):
    assert not isbn_handling.isbn_has_valid_check_digit(isbn)
    
@pytest.mark.parametrize("isbn, expected_result", NORMALIZATION_TESTS.items())
def test_normalization(isbn, expected_result, isbn_handling):
    result = isbn_handling.test_and_normalize_isbn(isbn)
    assert set(result.keys()) == set(expected_result.keys())
    for key in result:
        assert result[key] == expected_result[key]
