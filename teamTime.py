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
        from mpl_toolkits.basemap import Basemap
        import numpy as np
        import matplotlib.pyplot as plt
        import pandas as pd
        from geopy.geocoders import Nominatim
        import mplcursors
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

data= pd.DataFrame(list(zip(staffLat,staffLon,labels)), columns=['lat', 'lon','labels'])

#create the map
m=Basemap(llcrnrlon=-160, llcrnrlat=-75,urcrnrlon=160,urcrnrlat=80)
m.drawmapboundary(fill_color='#A6CAE0', linewidth=0)
m.fillcontinents(color='grey', alpha=0.7, lake_color='grey')
m.drawcoastlines(linewidth=0.1, color="white")

#Add a marker from the lat/lon
m.plot(data['lon'], data['lat'], linestyle='none', marker="o", markersize=16, alpha=0.6, c="orange", markeredgecolor="black", markeredgewidth=1)
mplcursors.cursor(hover=True)


plt.show()

