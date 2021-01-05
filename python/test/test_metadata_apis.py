# -*- coding: UTF-8 -*-

import os
from sys import path
from time import sleep
from urllib.request import urlretrieve

import pytest
import warnings

path.append(os.path.join(path[0], "python"))
import openapc_toolkit as oat

CROSSREF_METADATA_TEST_CASES = {
    "10.3390/robotics6020009": { # journal_article
        'success': True, 
        'data': {
            'doi_type': 'journal_article',
            'publisher': 'MDPI AG',
            'prefix': 'MDPI AG',
            'journal_full_title': 'Robotics',
            'issn': '2218-6581',
            'issn_print': None,
            'issn_electronic': '2218-6581',
            'license_ref': 'https://creativecommons.org/licenses/by/4.0/'
        }
    },
    "10.3998/mpub.11325807": { # book_title
        'success': True,
        'data': {
            'doi_type': 'book_title',
            'prefix': 'University of Michigan Library',
            'publisher': 'University of Michigan Press',
            'book_title': "Kafka's Zoopoetics",
            'isbn': '9780472131792',
            'isbn_print': '9780472131792',
            'isbn_electronic': '9780472126514',
            'license_ref': None
        }
    },
    "11.234/5678.9": { # no valid DOI
        'success': False, 
        'error_msg': "Parse Error: '11.234/5678.9' is no valid DOI"
    },
    "10.5194/acp-2018-644": { # unsupported DOI type
        'success': False,
        'error_msg': 'Unsupported DOI type "posted_content" (OpenAPC only supports the following types: journal_article, book_title'
    }
}

CROSSREF_ISBN_LOOKUP_TEST_CASES = [
    (["9780814214121"], {
        "success": True,
        "dois": ["10.26818/9780814214121"]
    }),
    (["9780472131792"], {
        "success": True,
        "dois": ["10.3998/mpub.11325807"]
    }),
    (["9781501748288"], {
        "success": True,
        "dois": []
    }),
    (["9781912656660"], {
        "success": True,
        "dois": []
    })
]

@pytest.mark.parametrize("doi, expected_result", CROSSREF_METADATA_TEST_CASES.items())
def test_crossref(doi, expected_result):
    answer = oat.get_metadata_from_crossref(doi)
    assert set(expected_result.keys()) == set(answer.keys())
    assert answer["success"] in [True, False]
    if answer["success"] == False:
        assert answer["error_msg"] == expected_result["error_msg"]
    else:
        assert set(expected_result["data"].keys()) == set(answer["data"].keys())
        for key in expected_result["data"].keys():
            if expected_result["data"][key] != answer["data"][key]:
                # Crossref metadata is subject to changes not controlled by us, so we only
                # issue a warning here.
                msg = 'Crossref: Unexpected metadata content for field {}: "{}" (Expected "{}")'
                msg = msg.format(key, answer["data"][key], expected_result["data"][key])
                warnings.warn(UserWarning(msg))
    sleep(1)

@pytest.mark.parametrize("isbn_list, expected_result", CROSSREF_ISBN_LOOKUP_TEST_CASES)
def test_isbn_doi_lookup(isbn_list, expected_result):
    answer = oat.find_book_dois_in_crossref(isbn_list)
    assert set(answer.keys()) == set(expected_result.keys())
    if expected_result["success"] == True:
        assert answer["dois"] == expected_result["dois"]
    sleep(1)
