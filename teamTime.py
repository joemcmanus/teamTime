#!/usr/bin/env python3

from datetime import datetime
from pytz import timezone
from prettytable import PrettyTable
import argparse
import csv




parser = argparse.ArgumentParser(description='Time Table')
parser.add_argument('--name', help="Optional name to search for", action="store")
parser.add_argument('--src', help="Optional src file, defaults to staff.csv", action="store", default="staff.csv")
parser.add_argument('--map', help="Draw map", action="store_true")
args=parser.parse_args()

def makeTime(staffName, staffZone):
    staffTime=datetime.now(timezone(staffZone)).strftime('%Y-%m-%d %H:%M')
    return staffTime

def getLocation(staffCity):
    geolocator = Nominatim(user_agent='teamTime')
    location = geolocator.geocode(staffCity)
    return((location.latitude), (location.longitude))


try: 
    with open(args.src, mode='r') as infile:
        reader = csv.reader(infile)
        staff={rows[0]:rows[1] for rows in reader } 
except:
    print("ERROR: Unable to read {}".format(args.src))
    quit()

if args.name: 
    staffName=args.name.capitalize()
    if staffName in staff:
        print(makeTime(staffName, staff[staffName]))
    quit()

if args.map:
    try:
        import pandas as pd
        from geopy.geocoders import Nominatim
        import plotly.graph_objects as go

    except: 
        print("ERROR: Basemap not found, can be downloaed:")
        print("ERROR: wget https://github.com/matplotlib/basemap/archive/v1.1.0.tar.gz") 
        quit()


staffLat=[]
staffLon=[]
labels=[]
table=PrettyTable()
table.add_row(["now()", datetime.now().strftime('%Y-%m-%d %H:%M')])
table.field_names=["Person", "Local Time"]
with open(args.src, mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        staffName=row[0]
        staffTime=makeTime(row[0], row[1])
        staffCity=row[2].strip()
        table.add_row([staffName, staffTime])
        if args.map:
            latitude, longitude=getLocation(staffCity)
            staffLat.append(latitude)
            staffLon.append(longitude)
            labels.append(staffName + " " + staffTime)

table.sortby = "Person"
print(table)
if not args.map:
    quit()

df= pd.DataFrame(list(zip(staffLat,staffLon,labels)), columns=['lat', 'lon','labels'])
#create the map
fig = go.Figure(data=go.Scattergeo( 
    lon=df['lon'], lat=df['lat'],text=df['labels'],mode='markers'))

fig.update_layout( title='Team Time', geo_scope='world',)

fig.show()

