#!/usr/bin/env python3

import csv
from fabric.api import *
import sys
import os

# USAGE: $ fab -R pub get_ut:input={input_file},output={output_file}

env.roledefs = {
    #'pub': ['openapc@pub']
    'pub': ['bup@pub']
}

openapc_dir = "/home/openapc/openapc/"

def prepare():
    local("git pull origin master")

def get_ut(input,output):
    if input == '' or output == '':
        sys.exit("Input file and output file are required.")
    if os.path.isfile(input):
        in_file = os.path.basename(input)
    else:
        sys.exit("Input file is no valid file.")
    handle = open(input, "r", encoding="utf-8")
    csv_reader = csv.reader(handle)
    line = next(csv_reader)
    if len(line) == 19:
        offsetting = "--offsetting "
    elif len(line) == 18:
        offsetting = ""
    else:
        sys.exit("Invalid row length: First line must consist of either 18 or 19 columns.")
        
    put("bin/fetch.pl", openapc_dir + "fetch.pl")
    put(input, openapc_dir + in_file)

    with cd(openapc_dir):
        run("perl fetch.pl " + offsetting + "--input " + in_file + " --output tmp_ut.csv")
        get("tmp_ut.csv", "tmp_ut.csv")
        local("python/csv_column_modification.py -e utf8 -o -q tfftttttttttttttttt tmp_ut.csv copy") # Does not modify any data, only changes the CSV format to OpenAPC/Offsetting standard
        local("rm tmp_ut.csv")
        local("mv out.csv " + output)
