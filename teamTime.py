#!/usr/bin/env python3

from datetime import datetime
from pytz import timezone
from prettytable import PrettyTable
import argparse
import csv

parser = argparse.ArgumentParser(description='Time Table')
parser.add_argument('--name', help="Optional name to search for", action="store")
parser.add_argument('--src', help="Optional src file, defaults to staff.csv", action="store", default="staff.csv")
args=parser.parse_args()

def makeTime(staffName, staffZone):
    staffTime=datetime.now(timezone(staffZone)).strftime('%Y-%m-%d %H:%M')
    return staffTime

with open(args.src, mode='r') as infile:
    reader = csv.reader(infile)
    staff={rows[0]:rows[1] for rows in reader } 
    

if args.name: 
    staffName=args.name.capitalize()
    if staffName in staff:
        print(makeTime(staffName, staff[staffName]))
    quit()


table=PrettyTable()
table.add_row(["now()", datetime.now().strftime('%Y-%m-%d %H:%M')])
table.field_names=["Person", "Local Time"]
for staffName in sorted(staff.keys()):
    table.add_row([staffName, makeTime(staffName, staff[staffName])])

print(table)
