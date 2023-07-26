#!/bin/bash

DIR="issnltables"
LATEST_FILE=`date -d "1 day ago" +%Y%m%d`".ISSN-to-ISSN-L.txt"

if ! [[ -d $DIR ]] ; then
    echo -e "\033[1;33mDirectory $DIR not found, creating...\033[0m"
    mkdir $DIR
fi

if ! [[ -f $DIR"/"$LATEST_FILE ]] ; then
    echo -e "\033[1;33mLatest issn_l mapping file ("$LATEST_FILE") not found, downloading a fresh copy...\033[0m"
    cd $DIR
    # 26/02/19: Added --no-check-certificate, remove when certificates issues with issn.org are resolved   
    wget --no-check-certificate "http://www.issn.org/wp-content/uploads/2014/03/issnltables.zip"
    unzip "issnltables.zip"
    rm "issnltables.zip"
    cd ..
fi

./issn_l_enrichment.py -e utf8 -o -q tfftttttttttttttttt out_journal-article.csv $DIR"/"$LATEST_FILE


