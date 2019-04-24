import platform
import os
import datetime
import subprocess
from shutil import copy
import xml.etree.ElementTree as ET
from uipErrors import *

keyPairId = ""
policy = ""
signature = ""

def getStravaCookies():
    cookieReaderScript = "python ./BinaryCookieReader.py " + os.path.expanduser('~/Library/Cookies/Cookies.binarycookies')
    process = subprocess.Popen(cookieReaderScript, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = process.communicate()
    result = out.split('\n')
    for lin in result:
        if "CloudFront-Key-Pair-Id" in lin:
            global keyPairId
            keyPairId = lin.split('=')[1].split(';')[0]
            #print("Key-Pair-Id = " + keyPairId)
        elif "CloudFront-Policy" in lin:
            global policy
            policy = lin.split('=')[1].split(';')[0]
            #print("Policy = " + policy)
        elif "CloudFront-Signature" in lin:
            global signature
            signature = lin.split('=')[1].split(';')[0]
            #print("Signature = " + signature)

def bakPrefs():
    bakfilename = '~/Library/Preferences/JOSM/preferences.xml.' + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + '.bak'
    copy(os.path.expanduser('~/Library/Preferences/JOSM/preferences.xml'), os.path.expanduser(bakfilename))

def updPrefs():
    ET.register_namespace('', "http://josm.openstreetmap.de/preferences-1.0")
    doc = ET.parse(os.path.expanduser('~/Library/Preferences/JOSM/preferences.xml'))
    root = doc.getroot()
    for maptag in doc.findall("./{http://josm.openstreetmap.de/preferences-1.0}maps/{http://josm.openstreetmap.de/preferences-1.0}map/{http://josm.openstreetmap.de/preferences-1.0}tag[@key='url']"):
        if "strava.com" in maptag.attrib["value"]:
            print("Updating Strava Imagery URL...")
            fullUrl = maptag.attrib["value"]
            splittedUrl = fullUrl.split('?')
            baseUrl = splittedUrl[0]
            print("--> [" + baseUrl + "]")
            cookieString = "Key-Pair-Id=" + keyPairId + "&Policy=" + policy + "&Signature=" + signature
            fullUrl = baseUrl + "?" + cookieString
            maptag.attrib["value"] = fullUrl
    print("Writing out preferences.xml...")
    doc.write(os.path.expanduser('~/Library/Preferences/JOSM/preferences.xml'), encoding="UTF-8")

try:
    if (platform.system() != "Darwin"):
        raise UpdImgPrefsOsError(platform.system())

    getStravaCookies()
    if (keyPairId == "" or policy == "" or signature == ""):
        raise UpdImgPrefsCookieError

    print("Backing up preferences.xml...")
    bakPrefs()
    updPrefs()
    print("Done.")

except UpdImgPrefsOsError as e:
    print("Only Safari on macOS currently supported.")
    print("Detected OS: " + e.message)
except UpdImgPrefsCookieError as e:
    print("No Strava cookies found!")
    print("Open Safari, browse to the Strava Heatmap, and login with your Strava account.")
