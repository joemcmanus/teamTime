#!/usr/bin/env python3
# File    : teamTime.py
# Author  : Joe McManus josephmc@alumni.cmu.edu
# Version : 0.6  10/17/2019 Joe McManus
# Copyright (C) 2019 Joe McManus

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


from datetime import datetime
from pytz import timezone
from prettytable import PrettyTable
from os import path
import argparse
import csv
import re
from typing import Iterable, List
import sys


class TeamMember:
    def __init__(self, csv_row: List):
        self.name = csv_row[0]
        self.timezone = csv_row[1]
        self.time = get_current_formatted_time(self.timezone)
        self.city = csv_row[2].strip()
        self._geo_location = None

    @property
    def _location(self):
        if self._geo_location is None:
            geolocator = Nominatim(user_agent="teamTime")
            self._geo_location = geolocator.geocode(self.city)

        return self._geo_location

    @property
    def latitude(self):
        return self._location.latitude

    @property
    def longitude(self):
        return self._location.longitude


def get_current_formatted_time(staffZone, format_="%Y-%m-%d %H:%M"):
    staffTime = datetime.now(timezone(staffZone)).strftime(format_)
    return staffTime


def main():
    args = parse_args()

    exit_if_args_invalid(args)

    table = PrettyTable()

    team_members = load_team_members_from_file(args.src)

    if args.name:
        fixedName = args.name.capitalize()
        team_members = filter_team_members_by_name(team_members, fixedName)

    if args.comp:
        table.field_names = ["Person", "Their Time", "Your Time"]
        add_comp_table_rows(team_members, table, args.comp)
    else:
        table.field_names = ["Person", "Local Time"]

        add_regular_rows(team_members, table)
        table.add_row(["now()", datetime.now().strftime("%Y-%m-%d %H:%M")])

    sort_table(table, args.sort, args.rev)

    table.align["Person"] = "l"
    print(table)

    if args.map:
        show_map(team_members)


def parse_args():
    parser = argparse.ArgumentParser(description="Time Table")
    parser.add_argument("--name", help="Optional name to search for", action="store")
    parser.add_argument("--comp", help="Compare times of team members.", action="store")
    parser.add_argument(
        "--src",
        help="Optional src file, defaults to staff.csv",
        action="store",
        default="staff.csv",
    )
    parser.add_argument("--map", help="Draw map", action="store_true")
    parser.add_argument(
        "--sort",
        help="Field to sort by <time|name>. Defaults to name.",
        action="store",
        default="name",
    )
    parser.add_argument("--rev", help="Reverse the sort order", action="store_true")

    return parser.parse_args()


def exit_if_args_invalid(args):
    if not path.isfile(args.src):
        print("ERROR: Unable to read {}".format(args.src))
        sys.exit(1)

    if args.comp:
        pattern = re.compile(r"\d{1,2}:\d{2}")
        if not pattern.match(args.comp):
            print("ERROR: Please use 24 hour time format, i.e. --comp 10:00")
            sys.exit(1)

    if args.sort not in ["name", "time"]:
        print("ERROR: Please specify a sort argument of 'name' or 'time'")
        sys.exit(1)

    if args.map:
        try:
            global pd
            global Nominatim
            global go

            import pandas as pd
            from geopy.geocoders import Nominatim
            import plotly.graph_objects as go
        except Exception:
            print("Missing mapping libs, try pip3 install pandas plotly geopy")
            sys.exit(1)


def load_team_members_from_file(src_file_path):
    with open(src_file_path, mode="r", encoding="utf-8", newline="") as infile:
        reader = csv.reader(infile)
        team_members = [TeamMember(row) for row in reader]

    return team_members


def filter_team_members_by_name(team_members, fixedName):
    team_members = [tm for tm in team_members if tm.name == fixedName]

    return team_members


def add_comp_table_rows(
    team_members: Iterable[TeamMember], table: PrettyTable, comp_time: str
):
    localTime = get_local_time(comp_time)
    for tm in team_members:
        table.add_row([tm.name, compareTime(localTime, tm.timezone), localTime])


def get_local_time(comp_time):
    now = datetime.now()
    getHour, getMinute = comp_time.split(":")
    return datetime(now.year, now.month, now.day, int(getHour), int(getMinute))


def compareTime(localTime, staffZone):
    remoteTime = localTime.astimezone(timezone(staffZone)).strftime("%Y-%m-%d %H:%M")
    return remoteTime


def add_regular_rows(
    team_members: Iterable[TeamMember], table: PrettyTable
):
    for tm in team_members:
        table.add_row([tm.name, tm.time])


def sort_table(table, sort_option, rev):
    if sort_option == "name":
        table.sortby = table.field_names[0]
    else:
        table.sortby = table.field_names[1]

    table.reversesort = rev


def show_map(team_members):
    team_geo_data = [
        (tm.latitude, tm.longitude, f"{tm.name} {tm.time}") for tm in team_members
    ]
    # Convert lists to Pandas data frames
    df = pd.DataFrame(team_geo_data, columns=["lat", "lon", "labels"])

    # create the map
    fig = go.Figure(
        data=go.Scattergeo(
            lon=df["lon"],
            lat=df["lat"],
            text=df["labels"],
            mode="markers",
            marker_size=12,
            marker_line_width=2,
        )
    )

    fig.update_layout(
        title="Team Time",
    )

    fig.show()


if __name__ == "__main__":
    main()
