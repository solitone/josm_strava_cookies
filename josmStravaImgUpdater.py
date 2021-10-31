import os
import datetime
#import subprocess
from shutil import copy
import xml.etree.ElementTree as ET

from stravaCookieFetcher import *

class JosmStravaImgUpdater(object):
    def __init__(self):
        self.josmPreferences = "./fakepath.xml" # has to be set in OS-specific constructor

    def bakPrefs(self):
        bakfile = self.josmPreferences + '.' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.bak'
        copy(self.josmPreferences, bakfile)

    def updPrefs(self):
        stravaCookieFetcher = MacOsStravaCookieFetcher()
        stravaCookieFetcher.fetchCookies()
        cookieString = stravaCookieFetcher.getCookieString()

        ET.register_namespace('', "http://josm.openstreetmap.de/preferences-1.0")
        doc = ET.parse(self.josmPreferences)
        root = doc.getroot()
        for maptag in doc.findall("./{http://josm.openstreetmap.de/preferences-1.0}maps/{http://josm.openstreetmap.de/preferences-1.0}map/{http://josm.openstreetmap.de/preferences-1.0}tag[@key='url']"):
            if "strava.com" in maptag.attrib["value"]:
                print("Updating Strava Imagery URL...")
                fullUrl = maptag.attrib["value"]
                splittedUrl = fullUrl.split('?')
                baseUrl = splittedUrl[0]
                print("--> [" + baseUrl + "]")
                fullUrl = baseUrl + "?" + cookieString
                maptag.attrib["value"] = fullUrl
        print("Writing out preferences.xml...")
        doc.write(self.josmPreferences, encoding="UTF-8")

class MacOsJosmStravaImgUpdater(JosmStravaImgUpdater):
    def __init__(self):
        super(MacOsJosmStravaImgUpdater, self).__init__()
        self.josmPreferences = os.path.expanduser('~/Library/Preferences/JOSM/preferences.xml')
