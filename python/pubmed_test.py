#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Look up a DOI in PubMed.

This script looks up a DOI in pubmed.
"""

import argparse

from openapc_toolkit import get_metadata_from_pubmed as gmfp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("doi", help="A DOI to look up in pubmed.")
    args = parser.parse_args()

    res = gmfp(args.doi)
    if res["success"]:
        for key, value in res["data"].items():
            print(key, ":", value)
    else:
        print(res["error_msg"])

if __name__ == '__main__':
    main()
