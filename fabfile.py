#!/usr/bin/env python3

import csv
from fabric.api import *
import sys
import os

# USAGE: $ fab -R pub get_ut:input={input_file},output={output_file},refresh={true,false}

env.roledefs = {
    'pub': ['bup@pub']
}

openapc_dir = "/home/openapc/openapc/"

def prepare():
    local("git pull origin master")

def get_ut(input,output,refresh):
    if input == '' or output == '':
        sys.exit("Input file and output file are required.")
    if os.path.isfile(input):
        in_file = os.path.basename(input)
    else:
        sys.exit("Input file is no valid file.")
    if refresh.lower().strip() == "true":
        refresh_param = "--refresh "
    elif refresh.lower().strip() == "false":
        refresh_param = ""
    else:
        sys.exit("Refresh parameter must either be true or false.")
        
    put("bin/fetch.pl", openapc_dir + "fetch.pl")
    put(input, openapc_dir + in_file)

    with cd(openapc_dir):
        run("perl fetch.pl " + refresh_param + "--input " + in_file + " --output doi_ut_mapping.csv")
        get("doi_ut_mapping.csv", "doi_ut_mapping.csv")
        local("python/csv_value_copy.py -e utf8 -e2 utf8 -f -o -q tfftttttttttttttttttt doi_ut_mapping.csv 0 1 " + input + " 3 15")
        local("rm doi_ut_mapping.csv")
        local("mv out.csv " + output)
