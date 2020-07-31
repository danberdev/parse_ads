#!/bin/sh

scriptdir="$(dirname $0)"
cd $0

. ./venv/bin/activate
./parse_ads.py
