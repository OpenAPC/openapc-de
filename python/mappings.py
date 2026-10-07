#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json

MAPPINGS_DICT = None

def load_mappings_json():
    global MAPPINGS_DICT
    with open("mappings.json", "r") as handle:
        content = handle.read()
        MAPPINGS_DICT = json.loads(content)

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
