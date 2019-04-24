import os
import datetime
import subprocess
from shutil import copy
import xml.etree.ElementTree as ET

from stravaImgUpdError import *

class StravaImgUpdater():
    def __init__(self):
        self.keyPairId = ""
        self.policy = ""
        self.signature = ""
        self.preferences = "./fakepath.xml" # has to be set in OS-specific constructor

    def bakPrefs(self):
        bakfile = self.preferences + '.' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.bak'
        copy(self.preferences, bakfile)

    def updPrefs(self):
        ET.register_namespace('', "http://josm.openstreetmap.de/preferences-1.0")
        doc = ET.parse(self.preferences)
        root = doc.getroot()
        for maptag in doc.findall("./{http://josm.openstreetmap.de/preferences-1.0}maps/{http://josm.openstreetmap.de/preferences-1.0}map/{http://josm.openstreetmap.de/preferences-1.0}tag[@key='url']"):
            if "strava.com" in maptag.attrib["value"]:
                print("Updating Strava Imagery URL...")
                fullUrl = maptag.attrib["value"]
                splittedUrl = fullUrl.split('?')
                baseUrl = splittedUrl[0]
                print("--> [" + baseUrl + "]")
                cookieString = "Key-Pair-Id=" + self.keyPairId + "&Policy=" + self.policy + "&Signature=" + self.signature
                fullUrl = baseUrl + "?" + cookieString
                maptag.attrib["value"] = fullUrl
        print("Writing out preferences.xml...")
        doc.write(self.preferences, encoding="UTF-8")

class MacOsStravaImgUpdater(StravaImgUpdater):
    def __init__(self):
        self.preferences = os.path.expanduser('~/Library/Preferences/JOSM/preferences.xml')

    def getCookies(self):
        cookieReaderScript = "python ./BinaryCookieReader.py " + os.path.expanduser('~/Library/Cookies/Cookies.binarycookies')
        process = subprocess.Popen(cookieReaderScript, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        result = out.split('\n')
        for lin in result:
            if "CloudFront-Key-Pair-Id" in lin:
                self.keyPairId = lin.split('=')[1].split(';')[0]
            elif "CloudFront-Policy" in lin:
                self.policy = lin.split('=')[1].split(';')[0]
            elif "CloudFront-Signature" in lin:
                self.signature = lin.split('=')[1].split(';')[0]

        if (self.keyPairId == "" or self.policy == "" or self.signature == ""):
            message = "Open Safari, browse to the Strava Heatmap, and login with your Strava account."
            raise StravaImgUpdCookieError(message)
