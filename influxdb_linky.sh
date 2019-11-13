#!/bin/bash

set -au
set -e

if [ $# -ne 1 ]
then
	echo "Usage: $0 config_file.cfg"
	exit 2
fi

CFG_FILE="$1"

cd $(dirname $0)

# check configuration file
if [ -f "${CFG_FILE}" ]
then
  source "${CFG_FILE}"
  rm -f data.txt
  ./linky_influxdb.py data.txt

  curl -XPOST "$INFLUXDB_HOST/write?db=$INFLUXDB_DATABASE" \
	  --silent \
	  --user $INFLUXDB_USER:$INFLUXDB_PASSWORD \
	  --data-binary @data.txt
else
    echo "Config file is missing ["${CFG_FILE}"]"
    exit 1
fi
