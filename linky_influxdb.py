#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates energy consumption InfluxDB from Enedis (ERDF) consumption data
collected via their website (API).
"""

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import datetime
import linky_json
import sys


USERNAME = os.environ['LINKY_USERNAME']
PASSWORD = os.environ['LINKY_PASSWORD']

def json_to_inflxudb(res, name, filename):
    with open(filename, "w") as f:
        for e in res:
            f.write("Linky %s=%f %s\n" % (name, e['conso'], e['time']))


# Main script
def main(filename):
    print("logging in as %s..." % USERNAME)
    token = linky_json.linky.login(USERNAME, PASSWORD)
    print("logged in successfully!")

    print("retrieving data...")
    today = datetime.date.today()

    # Par heure
    # Yesterday and the day before
    res_hour = linky_json.linky.get_data_per_hour(token,
            linky_json.dtostr(today - linky_json.relativedelta(days=2)),
            linky_json.dtostr(today))

    print("got data!")

    res_heure_json = linky_json.export_hours_values_json_format(res_hour,
        "%s000000000")

    json_to_inflxudb(res_heure_json, "heure", filename)

    # par jour
    # données disponible depuis le 8/2/2018
    res_day = linky_json.linky.get_data_per_day(token,
        linky_json.dtostr(today - linky_json.relativedelta(days=1, months=1)),
        linky_json.dtostr(today - linky_json.relativedelta(days=1)))

    res_jour_json = linky_json.export_days_values_json_format(res_day,
        "%s000000000")

    json_to_inflxudb(res_jour_json, "jour", filename)


if __name__ == "__main__":
    main(sys.argv[1])
