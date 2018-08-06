#!/usr/bin/env python3

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
        
    put("bin/fetch.pl", openapc_dir + "fetch.pl")
    put(input, openapc_dir + in_file)

    with cd(openapc_dir):
        run("perl fetch.pl --input " + in_file + " --output tmp_ut.csv")
        get("tmp_ut.csv", "tmp_ut.csv")
        local("python/csv_column_modification.py -e utf8 -o -q tffttttttttttttttt tmp_ut.csv copy") # Does not modify any data, only changes the CSV format to OpenAPC standard
        local("rm tmp_ut.csv")
        local("mv out.csv " + output)
