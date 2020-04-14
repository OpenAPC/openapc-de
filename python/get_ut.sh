#!/bin/sh

cd ..
fab -R pub get_ut:python/out.csv,python/out.csv
cd python
