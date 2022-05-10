import os
import subprocess
import sys

from stravacookies import StravaBrowser, StravaCFetchError, StravaCFetchCookieError, StravaCFetchOsError, StravaCFetchJosmprefsError

class StravaCookieFetcher(object):
    def __init__(self):
        self.deleteCookieInfo()

    def deleteCookieInfo(self):
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

    def processCookieJar(self, cookiejar):
        for cookie in cookiejar:
            if "CloudFront-Key-Pair-Id" in cookie.name:
                self.keyPairId = cookie.value
            elif "CloudFront-Policy" in cookie.name:
                self.policy = cookie.value
            elif "CloudFront-Signature" in cookie.name:
                self.signature = cookie.value
        if (self.keyPairId == "" or self.policy == "" or self.signature == ""):
            self.deleteCookieInfo()
            message = "Authentication Strava cookies not found."
            raise StravaCFetchCookieError(message)
        self.setCookieString()

    def fetchCookies(self, stravaEmail, stravaPassword):
        try:
            browser = StravaBrowser()
            browser.stravaLogin(stravaEmail, stravaPassword)
            self.processCookieJar(browser.cookiejar)
        except StravaCFetchCookieError as e:
            print(e, file=sys.stderr)
            message = "Logged in successfully, but could not get authentication cookies."
            raise StravaCFetchCookieError(message)
        except Exception as e:
            print(e, file=sys.stderr)
            message = "Make sure to provide correct Strava login information."
            raise StravaCFetchCookieError(message)
