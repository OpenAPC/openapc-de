#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json

MAPPINGS_DICT = None
MAPPINGS_FILE = "mappings.json"

def load_mappings_json(mappings_file=None):
    global MAPPINGS_DICT
    if mappings_file is None:
        mappings_file = MAPPINGS_FILE
    with open(mappings_file, "r") as handle:
        content = handle.read()
        MAPPINGS_DICT = json.loads(content)

def save_mappings_json(mappings_file=None):
    if MAPPINGS_DICT is None:
        load_mappings_json()
    if mappings_file is None:
        mappings_file = MAPPINGS_FILE
    with open(mappings_file, "w") as handle:
        json.dump(MAPPINGS_DICT, handle, ensure_ascii=False, indent=2, sort_keys=True)

def __getattr__(name):
    '''
    Backwards compatibility, mapping dicts were module attributes before
    '''
    global MAPPINGS_DICT
    if MAPPINGS_DICT is None:
        load_mappings_json()
    if name in MAPPINGS_DICT.keys():
        return MAPPINGS_DICT[name]
    else:
        raise Exception("mappings.json does not have a property '{}'".format(name))
