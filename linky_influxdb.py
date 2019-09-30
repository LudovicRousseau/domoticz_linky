#!/usr/bin/env python3

#    linky_influxdb.py: get Linky data to file a InfluxDB database
#    copyright (c) 2018  ludovic rousseau, <ludovic.rousseau@free.fr>
#
#    this program is free software: you can redistribute it and/or modify
#    it under the terms of the gnu general public license as published by
#    the free software foundation, either version 3 of the license, or
#    (at your option) any later version.
#
#    this program is distributed in the hope that it will be useful,
#    but without any warranty; without even the implied warranty of
#    merchantability or fitness for a particular purpose.  see the
#    gnu general public license for more details.
#
#    you should have received a copy of the gnu general public license
#    along with this program.  if not, see <https://www.gnu.org/licenses/>.

import os
import sys
import json
from dateutil.relativedelta import relativedelta
import datetime

from pylinky import LinkyClient


def json_to_inflxudb(res, name, filename):
    with open(filename, "a") as f:
        for e in res:
            f.write("Linky %s=%f %s\n" % (name, e["conso"], e["time"]))


def main(username, password, filename):
    print("Connect")
    client = LinkyClient(username, password)

    print("Login as", username)
    client.login()

    #  data for the last 2 days, 1 mesure per 0.5 hour
    # today
    end = datetime.date.today()
    #  2 days ago
    begin = end - relativedelta(days=2)

    print("Fetch hour data")
    res_hour = client.get_data_per_period("hourly", begin, end)
    if len(res_hour) <= 1:
        print("ERROR: Pas de relevés horaires ?", file=sys.stderr)
    res_hour = client.format_data(res_hour, "%s000000000")

    print("Save to file")
    json_to_inflxudb(res_hour, "heure", filename)

    #  data for the last month, 1 mesure per day
    end = datetime.date.today()
    begin = end - relativedelta(months=1)

    print("Fetch day data")
    res_day = client.get_data_per_period("daily", begin, end)
    res_hour = client.format_data(res_day, "%s000000000")

    print("Save to file", filename)
    json_to_inflxudb(res_hour, "jour", filename)

    print("Close session")
    client.close_session()


if __name__ == "__main__":
    username = os.environ['LINKY_USERNAME']
    password = os.environ['LINKY_PASSWORD']
    sys.exit(main(username, password, sys.argv[1]))
