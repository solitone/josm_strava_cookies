import platform

from josmStravaImgUpdater import *
from stravaCFetchError import *

try:
    if (platform.system() == "Darwin"):
        stravaImgUpdater = MacOsJosmStravaImgUpdater()
    elif (platform.system() == "Linux"):
        stravaImgUpdater = LinuxJosmStravaImgUpdater()
    elif (platform.system() == "Windows"):
        stravaImgUpdater = WindowsJosmStravaImgUpdater()
    else:
        raise StravaCFetchOsError(platform.system())

    print("Backing up preferences.xml...")
    stravaImgUpdater.bakPrefs()
    stravaImgUpdater.updPrefs()
    print("Done.")

except StravaCFetchOsError as e:
    print("Only Chrome/Firefox on OSX/Linux/Windows (plus Safari on OSX) are supported.")
    print("Detected OS: " + e.message)
except StravaCFetchCookieError as e:
    print("No Strava cookies found!")
    print(e.message)
except StravaCFetchJosmprefsError as e:
    print("Couldn't locate JOSM preferences file.")
    print( e.message )
