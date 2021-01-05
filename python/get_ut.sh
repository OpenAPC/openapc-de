#!/bin/sh

cd ..
if [ "$1" = "refresh" ]; then
    fab -R pub get_ut:python/out.csv,python/out.csv,true
else
    fab -R pub get_ut:python/out.csv,python/out.csv,false
fi
cd python
