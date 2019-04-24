# josm_strava_cookies
Utility for setting Strava cookies in JOSM preferences. This allows to get a high resolution Strava Heatmap.

## Requirements
- python 2 is required. The pre-installed version that comes with macOS does work.
- Currently, only macOS and the Safari browser are supported.

## Usage
1. Go to https://www.strava.com/heatmap and setup a Strava account.
2. Log in with your Strava credentials, flagging the "remember me" checkbox.
3. In JOSM preferences, activate the Strava imagery URLs that you need.
4. Change each default imagery URL string from e.g.:
tms[3,11]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles/run/bluered/{zoom}/{x}/{y}.png
to:
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/bluered/{zoom}/{x}/{y}.png
5. Run the script from the command line with:
$ python upd_strava_prefs.py
6. The imagery URL should be updated to:
tms[3,15]:https://heatmap-external-{switch:a,b,c}.strava.com/tiles-auth/run/bluered/{zoom}/{x}/{y}.png?Key-Pair-Id=<YOUR_KEY_PAIR_ID_COOKIE_VALUE>&Policy=<YOUR_POLICY_COOKIE_VALUE>&Signature=<YOUR_SIGNATURE_COOKIE_VALUE>

## Licence
- josm_strava_cookies is distributed under the GPL v3.0.
- BinaryCookieReader.py is distributed under the ...
http://www.securitylearn.net/2012/10/27/cookies-binarycookies-reader/
