# -*- coding: utf-8 -*-

import json
import platform

from string import Template

from stravaCookieFetcher import *
from stravaCFetchError import *

urlTemplate = Template("https://heatmap-external-a.strava.com/tiles-auth/$activity/bluered/{z}/{x}/{y}.png?$cookieString")
activities = {  "both": "both",
                "ride": "ride",
                "run": "run",
                "winter": "winter"}
mapNames = {"both": "Strava Heatmap (all)",
            "ride": "Strava Heatmap (ride)",
            "run": "Strava Heatmap (run)",
            "winter": "Strava Heatmap (winter)"}

try:
    if (platform.system() == "Darwin"):
        stravaCookieFetcher = MacOsStravaCookieFetcher()
    else:
        raise StravaCFetchOsError(platform.system())

    stravaCookieFetcher.fetchCookies()
    cookieString = stravaCookieFetcher.getCookieString()

    maps = []

    for key in activities:
        url = urlTemplate.substitute(activity = activities[key], cookieString = cookieString)

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

    print(json.dumps(onlinemap))



except StravaCFetchOsError as e:
    print("Only Safari on macOS currently supported.")
    print("Detected OS: " + e.message)
except StravaCFetchCookieError as e:
    print("No Strava cookies found!")
    print(e.message)
