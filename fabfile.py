#!/usr/bin/python

from fabric.api import *

# USAGE: $ fab -R pub get_ut

env.roledefs = {
    'pub': ['openapc@pub'],
}

def prepare():
    local("git pull origin master")

def get_ut():
    put("bin/fetch.pl", "openapc/fetch.pl")
    put("data/apc_de.csv", "openapc/apc_de.csv")

    with cd("openapc/"):
        run("perl fetch.pl apc_de.csv")
        get("apc_de_ut.csv", "apc_de_ut.csv")
        local("R CMD BATCH R/isi_add.r")
        local("rm apc_de_ut.csv")
