#!/bin/bash

set -au
set -e

CFG_FILE="domoticz_linky.cfg"

cd $(dirname $0)

# check configuration file
if [ -f "${CFG_FILE}" ]
then
  source "${CFG_FILE}"
  export LINKY_USERNAME
  export LINKY_PASSWORD
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
