import platform

from stravaJosmImgUpdater import *
from stravaCFetchError import *

try:
    if (platform.system() == "Darwin"):
        stravaJosmImgUpdater = MacOsStravaJosmImgUpdater()
    else:
        raise StravaCFetchOsError(platform.system())

    print("Backing up preferences.xml...")
    stravaJosmImgUpdater.bakPrefs()
    stravaJosmImgUpdater.updPrefs()
    print("Done.")

except StravaCFetchOsError as e:
    print("Only Safari on macOS currently supported.")
    print("Detected OS: " + e.message)
except StravaCFetchCookieError as e:
    print("No Strava cookies found!")
    print(e.message)
