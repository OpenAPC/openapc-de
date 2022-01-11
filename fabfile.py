#!/usr/bin/env python3

import csv
import sys
import os

from fabric2 import task

# USAGE: $ fab2 get_ut {input_file} {output_file} {true,false}

openapc_dir = "/home/openapc/openapc/"
host = ["bup@pub"]

@task(hosts=host)
def get_ut(con, input_file, output_file, refresh):
    if input_file == '' or output_file == '':
        sys.exit("input_file file and output_file file are required.")
    if os.path.isfile(input_file):
        in_file = os.path.basename(input_file)
    else:
        sys.exit("input_file file is no valid file.")
    if refresh.lower().strip() == "true":
        refresh_param = "--refresh "
    elif refresh.lower().strip() == "false":
        refresh_param = ""
    else:
        sys.exit("Refresh parameter must either be true or false.")
        
    con.put("bin/fetch.pl", openapc_dir + "fetch.pl")
    con.put(input_file, openapc_dir + in_file)

    perl_cmd = "cd {} && perl fetch.pl {}--input {} --output doi_ut_mapping.csv".format(openapc_dir, refresh_param, in_file)
    print(perl_cmd)
    con.run(perl_cmd)
    con.get("doi_ut_mapping.csv", "doi_ut_mapping.csv")
    if refresh_param == "--refresh ":
        con.local("python/csv_column_modification.py -e utf8 -o -q tfftttttttttttttttttt " + input_file + " delete 15")
        con.local("python/csv_column_modification.py -e utf8 -o -q tfftttttttttttttttttt " + input_file + " insert 15 ut NA")
    con.local("python/csv_value_copy.py -e utf8 -e2 utf8 -f -o -q tfftttttttttttttttttt doi_ut_mapping.csv 0 1 " + input_file + " 3 15")
    con.local("rm doi_ut_mapping.csv")
    con.local("mv out.csv " + output_file)
