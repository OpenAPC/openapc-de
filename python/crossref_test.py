#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Look up a DOI in crossref.

This script looks up a DOI in Crossref.
Prints a listing of fields that could be received and are relevant to OpenAPC,
an error message otherwise.
"""

import argparse
import json
from urllib.request import urlopen, Request

from openapc_toolkit import get_metadata_from_crossref as gmfc

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("doi", help="A DOI to look up in crossref.")
    parser.add_argument("-r", "--raw", action="store_true", help="Print the raw Crossref XML.")
    args = parser.parse_args()
    if args.raw:
        url = 'https://api.crossref.org/works/' + args.doi
        req = Request(url)
        response = urlopen(req)
        content = response.read()
        data = json.loads(content)
        print(json.dumps(data, indent = 2))
    else:
        res = gmfc(args.doi)
        if res["success"]:
            for key, value in res["data"].items():
                print(key, ":", value)
        else:
            print(res["error_msg"])

if __name__ == '__main__':
    main()
