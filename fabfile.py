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
        get("apc_de_ut.csv", "data/apc_de.csv")
        local("git diff data/apc_de.csv")
