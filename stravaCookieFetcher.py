import os
import subprocess

from stravaCFetchError import *

class StravaCookieFetcher(object):
    def __init__(self):
        self.keyPairId = ""
        self.policy = ""
        self.signature = ""
        self.cookieString = ""

    def setCookieString(self):
        if (self.keyPairId == "" or self.policy == "" or self.signature == ""):
            message = "setCookieString() must be called after fetchCookies()"
            raise StravaCFetchCookieError(message)
        self.cookieString = "Key-Pair-Id=" + self.keyPairId + "&Policy=" + self.policy + "&Signature=" + self.signature

    def getCookieString(self):
        return self.cookieString


class MacOsStravaCookieFetcher(StravaCookieFetcher):
    # def __init__(self):
    #     super(MacOsStravaCookieFetcher, self).__init__()

    def fetchCookies(self):
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
            raise StravaCFetchCookieError(message)
