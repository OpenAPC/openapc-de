#!/usr/bin/python

from fabric.api import *
import sys

# USAGE: $ fab -R pub get_ut {input_file} {output_file}

env.roledefs = {
    'pub': ['openapc@pub'],
}

def prepare():
    local("git pull origin master")

def get_ut(input_file,output_file):
    if input_file == '' or output_file == '':
        sys.exit("Input file and output file are required.")

    put("bin/fetch.pl", "openapc/fetch.pl")
    put("data/" + input_file, "openapc/" + input_file)

    with cd("openapc/"):
        run("perl fetch.pl --input " + input_file + " --output tmp_ut.csv")
        get("tmp_ut.csv", "tmp_ut.csv")
        local("R CMD BATCH R/isi_add.r tmp.txt " + output_file)
        local("rm tmp_ut.csv")
