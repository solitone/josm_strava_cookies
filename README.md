# josm_strava_cookies

Utility for setting Strava cookies in JOSM preferences. This allows to
get high-resolution [Strava Heatmaps](https://www.strava.com/heatmap)
as an overlay in JOSM.  Permission has been granted by Strava,
see https://wiki.openstreetmap.org/wiki/Strava
and https://wiki.openstreetmap.org/wiki/Permissions/Strava

## Requirements
This tool relies on Python 3, which comes pre-installed on
most *x systems.  For macOS, a convenient way to install Python 3 is
homebrew; see, e.g.,
https://docs.python-guide.org/starting/install3/osx/

For Safari users on macOS, no further packages are needed.
For Chrome or Firefox users, please install the package `browser_cookie3`
(from command line, run `$ pip3 install browser_cookie3`):
https://github.com/borisbabic/browser_cookie3

This tool supports macOS and Linux. Support for Chrome/Firefox on Windows has
been added but not yet tested--test reports are welcome!

## Usage
1. Browse to the [Strava Heatmap](https://www.strava.com/heatmap) and setup
a Strava account.
2. Log in with your Strava credentials, flagging the *remember me* checkbox.
Move the map and zoom in and out to be sure that the required cookies
are present.
3. In JOSM preferences, activate the Strava imagery URLs that you need.
4. Change each default imagery URL string from e.g.:
```
tms[3,11]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles/run/bluered/{zoom}/{x}/{y}.png
```
to:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/bluered/{zoom}/{x}/{y}.png
```
5. Close JOSM.
6. If using Safari on macOS: grant Terminal with full disk access
(macOS System Preferences > Security & Privacy > Privacy > Full Disk
  Access > Add the Terminal application).
7. From the command line, run `$ python3 josm_strava_prefs_upd.py`
8. The imagery URL should be updated to:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/bluered/{zoom}/{x}/{y}.png?Key-Pair-Id=<YOUR_KEY_PAIR_ID_COOKIE_VALUE>&Policy=<YOUR_POLICY_COOKIE_VALUE>&Signature=<YOUR_SIGNATURE_COOKIE_VALUE>
```

### Cartograph support
Since version 1.4, macOS users can prepare Strava Heatmap TMS URLs also
for [Cartograph](https://www.cartograph.eu). Cartograph runs under iOS
and macOS, as well as Android.

The script `util/icloud_carto_omapdef.sh` writes Strava URLs in an
[online map definition file](https://www.cartograph.eu/help_onlinemapimport).
An online map definition file is a JSON file that can be imported directly
in Cartograph. The file is saved on iCloud, in the `Cartograph Pro` folder:
`<HOME>/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro`.
After importing the map definition file in Cartograph, the following maps
will be available in the *Manage Maps* menu:
- Strava Heatmap (all)
- Strava Heatmap (ride)
- Strava Heatmap (run)
- Strava Heatmap (winter)

Before importing a new map definition file to update the Strava URLs,
remove any Strava Heatmap from the map.

There is a similar script `util/icloud_carto_gen_urls.sh` which saves
in the same location a file containing just the Strava URLs.
Those URLs should then be copied and pasted manually in Cartograph.

## Licence
- `josm_strava_cookies` is distributed under the GPL v3.0.
- `BinaryCookieReader.py` is distributed under the ...
http://www.securitylearn.net/2012/10/27/cookies-binarycookies-reader/
