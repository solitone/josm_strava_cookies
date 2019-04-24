import platform

from stravaImgUpdater import *
from stravaImgUpdError import *

try:
    if (platform.system() == "Darwin"):
        stravaImgUpdater = MacOsStravaImgUpdater()
    else:
        raise UpdImgPrefsOsError(platform.system())

    stravaImgUpdater.getCookies()
    print("Backing up preferences.xml...")
    stravaImgUpdater.bakPrefs()
    stravaImgUpdater.updPrefs()
    print("Done.")

except StravaImgUpdOsError as e:
    print("Only Safari on macOS currently supported.")
    print("Detected OS: " + e.message)
except StravaImgUpdCookieError as e:
    print("No Strava cookies found!")
    print(e.message)
