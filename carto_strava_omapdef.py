# -*- coding: utf-8 -*-

import json
import platform
import sys

from pathlib import Path
from string import Template

from stravaCookieFetcher import *
from stravaCFetchError import *

# Set location where output file will be written
outdir = "./"
print("If you are on MacOS, you can save the map file directly in the Cartograph folder")
print("in iCloud, otherwise it will be saved in the current working directory.")
while True:
    print("Do you want to save the map file in iCloud (y/N)?")
    answer = input()
    if (answer == "y" or answer == "Y"):
        outdir = str(Path.home()) + "/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro/"
        break
    elif (answer == "n" or answer == "N" or answer == ""):
        # leave outdir unchanged
        break

# Set heatmap color
colors = {  "hot": "hot",
            "blue": "blue",
            "purple": "purple",
            "gray": "gray",
            "red": "bluered"}
print("What map color do you want?")
for color in colors:
    print ("  " + color)
while True:
    print("?")
    answer = input()
    if answer in colors:
        break
color = answer

activities = {  "all": "all",
                "ride": "ride",
                "run": "run",
                "winter": "winter"}

mapNames = {"all": "Strava Heatmap (all)",
            "ride": "Strava Heatmap (ride)",
            "run": "Strava Heatmap (run)",
            "winter": "Strava Heatmap (winter)"}

urlTemplate = Template("https://heatmap-external-a.strava.com/tiles-auth/$activity/$color/{z}/{x}/{y}.png?$cookieString")

try:
    if (platform.system() == "Darwin"):
        stravaCookieFetcher = MacOsStravaCookieFetcher()
    elif( platform.system() == 'Linux' ):
        stravaCookieFetcher = StravaCookieFetcher()
    elif( platform.system() == 'Windows' ):
        stravaCookieFetcher = StravaCookieFetcher()
    else:
        raise StravaCFetchOsError(platform.system())

    stravaCookieFetcher.fetchCookies()
    cookieString = stravaCookieFetcher.getCookieString()

    maps = []

    for key in activities:
        url = urlTemplate.substitute(activity = activities[key], color = colors[color], cookieString = cookieString)

        map = {
            "name": mapNames[key],
            "type": "ONLINE", # Possible values: "ONLINE" or "WMS"
            "url": url,
            "attribution": "© Strava",
            "description": "",
            "defaultLatitude": 45.0781,
            "defaultLongitude": 7.6761,
            "defaultZoom": 11,
            "minZoom": 2,
            "maxZoom": 22,
            "projection": "EPSG_4326", # Possible values: "EPSG_4326" (default) or "EPSG_900913"
            "headers": [
                {
                "key": "User-Agent",
                "value": "Cartograph"
                }
            ]
        }
        maps.append(map)

    onlinemap = {
        "version": 2,
        "maps": maps
    }

    print(json.dumps(onlinemap), file=open(outdir + "carto_strava.onlinemap", "w"))

except StravaCFetchOsError as e:
    print("Only Chrome/Firefox on macOS/Linux/Windows (plus Safari on macOS) are currently supported.", file=sys.stderr)
    print("Detected OS: " + e.message, file=sys.stderr)
except StravaCFetchCookieError as e:
    print("No Strava cookies found!", file=sys.stderr)
    print(e.message, file=sys.stderr)
