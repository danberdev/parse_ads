#!/bin/sh
DIR="$(dirname "$(readlink -f "$0")")"
cd $DIR

. ./venv/bin/activate
./parse_ads.py
