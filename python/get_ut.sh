#!/bin/sh

cd ..
if [ "$1" = "refresh" ]; then
    fab2 get-ut python/out.csv python/out.csv true
else
    fab2 --prompt-for-passphrase --prompt-for-login-password get-ut python/out.csv python/out.csv false
fi
cd python
