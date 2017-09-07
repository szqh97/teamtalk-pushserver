#!/bin/sh

current_dir=$(pwd)
cd ../../../pb/
./create.sh
cp -r gen/python/IM $current_dir

