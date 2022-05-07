import platform
import sys

from colorama import Fore, Style
from getpass import getpass

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

    stravaEmail = input(f"{Fore.CYAN}**** Enter your Strava account email:{Style.RESET_ALL} ")
    stravaPassword = getpass(f"{Fore.CYAN}**** Enter your Strava account password:{Style.RESET_ALL} ")

    print("Backing up preferences.xml...")
    stravaImgUpdater.bakPrefs()
    print("Updating preferences.xml...")
    stravaImgUpdater.updPrefs(stravaEmail, stravaPassword)
    print("Done.")

except StravaCFetchOsError as e:
    print("Only macOS/linux/Windows are supported.", file=sys.stderr)
    print("Detected OS: " + e.message, file=sys.stderr)
except StravaCFetchCookieError as e:
    print("Strava cookies unavailable.", file=sys.stderr)
    print(e.message, file=sys.stderr)
except StravaCFetchJosmprefsError as e:
    print("Couldn't locate JOSM preferences file.", file=sys.stderr)
    print( e.message, file=sys.stderr)
