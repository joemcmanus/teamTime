#!/usr/bin/env python3
# File    : teamtime.py
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


import argparse
import csv
import re
import sys
from datetime import datetime
from os import path
from typing import Iterable, List

from prettytable import PrettyTable
from pytz import timezone

from teamtime.team_member import TeamMember


def main():
    args = parse_args()

    exit_if_args_invalid(args)
    table = PrettyTable()

    team_members = load_team_members_from_file(args.src)

    if args.name:
        fixed_name = args.name.capitalize()
        team_members = filter_team_members_by_name(team_members, fixed_name)

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


def parse_args() -> argparse.Namespace:
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


def exit_if_args_invalid(args: argparse.Namespace):
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
            # These imports are slow. Only import them if the user really needs them.
            global pd
            global go

            import pandas as pd
            import plotly.graph_objects as go
        except Exception:
            print("Missing mapping libs, try pip3 install pandas plotly geopy")
            sys.exit(1)


def load_team_members_from_file(src_file_path: str) -> List[TeamMember]:
    with open(src_file_path, mode="r", encoding="utf-8", newline="") as infile:
        reader = csv.reader(infile)
        team_members = [TeamMember(row) for row in reader]

    return team_members


def filter_team_members_by_name(
    team_members: List[TeamMember], fixed_name: str
) -> List[TeamMember]:
    team_members = [tm for tm in team_members if tm.name == fixed_name]

    return team_members


def add_comp_table_rows(team_members: Iterable[TeamMember], table: PrettyTable, comp_time: str):
    local_time = get_local_time(comp_time)

    for tm in team_members:
        table.add_row([tm.name, compare_time(local_time, tm.timezone), local_time])


def get_local_time(comp_time: str) -> datetime:
    now = datetime.now()
    hour, minute = comp_time.split(":")
    return datetime(now.year, now.month, now.day, int(hour), int(minute))


def compare_time(local_time: datetime, time_zone: str) -> str:
    return local_time.astimezone(timezone(time_zone)).strftime("%Y-%m-%d %H:%M")


def add_regular_rows(team_members: Iterable[TeamMember], table: PrettyTable):
    for tm in team_members:
        table.add_row([tm.name, tm.time])


def sort_table(table: PrettyTable, sort_option: str, rev: bool):
    if sort_option == "name":
        table.sortby = table.field_names[0]
    else:
        table.sortby = table.field_names[1]

    table.reversesort = rev


def show_map(team_members: List[TeamMember]):
    team_geo_data = [(tm.latitude, tm.longitude, f"{tm.name} {tm.time}") for tm in team_members]
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
