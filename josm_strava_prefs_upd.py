import platform
import sys

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
    print("Only Chrome/Firefox on macOS/linux/Windows (plus Safari on macOS) are supported.", file=sys.stderr)
    print("Detected OS: " + e.message, file=sys.stderr)
except StravaCFetchCookieError as e:
    print("No Strava cookies found!", file=sys.stderr)
    print(e.message, file=sys.stderr)
except StravaCFetchJosmprefsError as e:
    print("Couldn't locate JOSM preferences file.", file=sys.stderr)
    print( e.message, file=sys.stderr)
