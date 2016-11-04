#!/usr/bin/python

from fabric.api import *
import sys
import os

# USAGE: $ fab -R pub get_ut:input={input_file},output={output_file}

env.roledefs = {
    'pub': ['openapc@pub'],
    'test': ['bup@pub'],
}

def prepare():
    local("git pull origin master")

def get_ut(input,output):
    if input == '' or output == '':
        sys.exit("Input file and output file are required.")

    put("bin/fetch.pl", "openapc/fetch.pl")
    in_file = os.path.basename(input)
    put(input, "openapc/" + in_file)

    with cd("openapc/"):
        print(blue("Running script!"))
        run("perl fetch.pl --input " + in_file + " --output tmp_ut.csv")
        get("tmp_ut.csv", "tmp_ut.csv")
        local("R CMD BATCH '--args tmp.txt " + output +"' R/isi_add.r")
        local("rm tmp_ut.csv")
