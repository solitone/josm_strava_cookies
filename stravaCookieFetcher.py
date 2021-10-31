import os
import subprocess
from stravaCFetchError import *

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

    def fetchFirefoxCookies(self):
        import browser_cookie3
        # import only here, so browser_cookie3 is _not_ required on vanilla macOS/Safari
        cookiejar = browser_cookie3.firefox()
        self.processCookieJar(cookiejar, 'Firefox')

    def fetchChromeCookies(self):
        import browser_cookie3
        # import only here, so browser_cookie3 is _not_ required on vanilla macOS/Safari
        cookiejar = browser_cookie3.chrome()
        self.processCookieJar(cookiejar, 'Chrome')

    def processCookieJar(self, cookiejar, browser):
        for cookie in cookiejar:
            if "CloudFront-Key-Pair-Id" in cookie.name:
                self.keyPairId = cookie.value
            elif "CloudFront-Policy" in cookie.name:
                self.policy = cookie.value
            elif "CloudFront-Signature" in cookie.name:
                self.signature = cookie.value
        if (self.keyPairId == "" or self.policy == "" or self.signature == ""):
            self.deleteCookieInfo()
            message = "No usable Strava-heatmap cookies in %s"%browser
            raise StravaCFetchCookieError(message)
        self.setCookieString()

    def fetchCookies(self):
        try:
            self.fetchChromeCookies()
            return
        except Exception as e:
            print( e )
            print( "Couldn't retrieve appropriate cookies from Chrome, moving on." )
        try:
            self.fetchFirefoxCookies()
            return
        except Exception as e:
            print( e )
            print( "Couldn't retrieve appropriate cookies from Firefox." )
            print( "All supported browsers have been tried unsuccessfully." )
        message = ( "Open https://www.strava.com/heatmap in any supported browser, and log in with your Strava account." )
        raise StravaCFetchCookieError(message)



class MacOsStravaCookieFetcher(StravaCookieFetcher):
    def fetchSafariCookies(self):
        # get the dir where file stravaCookieFetcher.py is saved
        pyFileDir = os.path.dirname(os.path.realpath(__file__))
        cookieReaderScript = (
                                "python3 " + pyFileDir + "/BinaryCookieReader.py "
                                + os.path.expanduser('~/Library/Cookies/Cookies.binarycookies')
                             )
        process = subprocess.Popen(cookieReaderScript, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        try:
            out=out.decode('utf-8')
            result=out.split('\n')
        except Exception as e:
            ## no access to Safari cookies
            result=None
        if result is None:
            message = "No usable Strava-heatmap cookies in Safari"
            raise StravaCFetchCookieError(message)
        for lin in result:
            if "CloudFront-Key-Pair-Id" in lin:
                self.keyPairId = lin.split('=')[1].split(';')[0]
            elif "CloudFront-Policy" in lin:
                self.policy = lin.split('=')[1].split(';')[0]
            elif "CloudFront-Signature" in lin:
                self.signature = lin.split('=')[1].split(';')[0]
        if (self.keyPairId == "" or self.policy == "" or self.signature == ""):
            self.deleteCookieInfo()
            message = "No usable Strava-heatmap cookies in Safari"
            raise StravaCFetchCookieError(message)
        self.setCookieString()


    def fetchCookies(self):
        ## On macOS, support Safari on top of the default Chrome and Firefox
        try:
            self.fetchSafariCookies()
            return
        except StravaCFetchCookieError as e:
            print( e )
            print( "Couldn't retrieve appropriate cookies from Safari, moving on" )
        super().fetchCookies()
