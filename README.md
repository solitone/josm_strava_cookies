# josm_strava_cookies

Utility for setting Strava cookies in JOSM preferences. This allows to
get high-resolution [Strava Heatmaps](https://www.strava.com/heatmap)
as an overlay in JOSM.  Permission has been granted by Strava,
see https://wiki.openstreetmap.org/wiki/Strava
and https://wiki.openstreetmap.org/wiki/Permissions/Strava

## Requirements
This tool runs on macOS, linux, and Windows operating systems.

It relies on Python 3, which comes pre-installed on
most *x systems.  For macOS, a convenient way to install Python 3 is
homebrew; see, e.g.,
https://docs.python-guide.org/starting/install3/osx/. For Windows, see
https://www.python.org/downloads/windows/.

The following packages are also required:
- TODO `browser_cookie3`, run `$ pip3 install browser_cookie3` from command line;
- ... TODO ...

A Strava account is required. Facebook/Google/Apple login to Strava is not
supported.

## Usage
1. Browse to the [Strava Heatmap](https://www.strava.com/heatmap) and setup
a Strava account.
2. In JOSM preferences, activate the Strava imagery URLs that you need.
3. Change each default imagery URL string from e.g.:
```
tms[3,11]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles/run/hot/{zoom}/{x}/{y}.png
```
to:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/hot/{zoom}/{x}/{y}.png
```
4. Close JOSM.
5. From the command line, run `$ python3 josm_strava_prefs_upd.py`.
6. Provide the email/password of your Strava account.
6. The imagery URL should be updated to:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/hot/{zoom}/{x}/{y}.png?Key-Pair-Id=<YOUR_KEY_PAIR_ID_COOKIE_VALUE>&Policy=<YOUR_POLICY_COOKIE_VALUE>&Signature=<YOUR_SIGNATURE_COOKIE_VALUE>
```
When JOSM can no longer display the hi-res heatmap, it means cookies have
expired. You need to repeat the procedure from step 5.

### Cartograph Maps support
It is also possible to prepare Strava Heatmap TMS URLs for
[Cartograph Maps](https://www.cartograph.eu). Cartograph Maps runs under iOS
and macOS, as well as Android.

Run `$ python3 carto_strava_omapdef.py` to write out Strava URLs in an
[online map definition file](https://www.cartograph.eu/help_onlinemapimport).
An online map definition file is a JSON file that can be imported directly
in Cartograph Maps.

A choice will be offered to save the omapdef file either in the current
directory or in iCloud. The latter option is only relevant for macOS users, and
the file will be saved in the
`<HOME>/Library/Mobile Documents/com~apple~CloudDocs/Cartograph Pro` folder,
for an easy import into Cartograph Maps from mobile devices.

After importing the map definition file in Cartograph Maps, the following maps
will be available in the *Manage Maps* menu:
- Strava Heatmap (all)
- Strava Heatmap (ride)
- Strava Heatmap (run)
- Strava Heatmap (winter)

When Cartograph Maps can no longer display the hi-res heatmap, it means
Strava authentication cookies have expired. Remove any previous Strava Heatmap
from Cartograph Maps, relaunch `carto_strava_omapdef.py`, and import the new
oampdef file in Cartograph Maps.

## How it works
Hi-res heatmap is available to Strava registered users only. When you click to
https://www.strava.com/heatmap and login to Strava, your browser gets several
cookies that it uses to show Strava servers you are authorized to download
the hi-res map.

The authentication process consist of three steps:

1. User fills login form at https://strava.com/login.
2. Upon submit, browser sends a POST request to https://www.strava.com/session,
email=<STRAVA_EMAIL>, password=<STRAVA_PASSWORD>, remember-me checkbox set,
and receives _strava4_session, strava_remember_id, and strava_remember_token
cookies from server.
3. Browser sends a GET request to https://heatmap-external-a.strava.com/auth
with session cookies set, and gets CloudFront-Signature, CloudFront-Policy, and
CloudFront-Key-Pair-Id cookies from server.

The last three cookies are those needed to allow browser to download
the high-res heatmap. Concatenating the cookie strings to the TMS URLs (as
shown below) allows external applications (such as JOSM or Cartograph Maps)
to download the hi-res tiles from Strava.

Example TMS URL:
```
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/hot/{zoom}/{x}/{y}.png?Key-Pair-Id=<YOUR_KEY_PAIR_ID_COOKIE_VALUE>&Policy=<YOUR_POLICY_COOKIE_VALUE>&Signature=<YOUR_SIGNATURE_COOKIE_VALUE>
```
Cookies expire, so it is necessary to re-login to Strava from time to
time to get up to date cookies.

## Licence
`josm_strava_cookies` is distributed under the GPL v3.0.
