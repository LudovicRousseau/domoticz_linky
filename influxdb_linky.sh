#!/bin/sh

set -au
set -e

SCRIPT="$0"
BASE_DIR=$(dirname "${SCRIPT}")
export BASE_DIR
CFG_FILE="domoticz_linky.cfg"

# check configuration file
if [ -f "${BASE_DIR}"/"${CFG_FILE}" ]
then
  . "${BASE_DIR}"/"${CFG_FILE}"
  export LINKY_USERNAME
  export LINKY_PASSWORD
  "${BASE_DIR}"/linky_influxdb.py data.txt

  curl -XPOST "$INFLUXDB_HOST/write?db=$INFLUXDB_DATABASE" \
	  --user $INFLUXDB_USER:$INFLUXDB_PASSWORD \
	  --data-binary @data.txt
else
    echo "Config file is missing ["${BASE_DIR}"/"${CFG_FILE}"]"
    exit 1
fi
