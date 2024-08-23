#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Remove empty lines (= rows without any cost data) from an additional_costs file.
"""

import argparse
import re

from shutil import move

EMPTY_LINE_RE = re.compile(r'^(".*?"|NA),NA,NA,NA,NA,NA,NA,NA,NA$')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The file to squash.")
    parser.add_argument("--in_place", "-i", action="store_true", help="Modify the file in place. Otherwise, only generate an out.csv")
    args = parser.parse_args()
    
    with open(args.file, "r") as in_file:
        with open("out.csv", "w") as out_file: 
            for line in in_file:
                if not EMPTY_LINE_RE.match(line):
                    out_file.write(line)
    if args.in_place:
        move("out.csv", args.file)

if __name__ == '__main__':
    main()

