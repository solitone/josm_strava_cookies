import mechanize
from http import cookiejar

LOGIN_URL = "https://strava.com/login"
AUTH_URL = "https://heatmap-external-a.strava.com/auth"

class StravaBrowser(object):
    def __init__(self):
        self.browser = mechanize.Browser()
        self.cookiejar = cookiejar.CookieJar()
        self.browser.set_cookiejar(self.cookiejar)

    def stravaLogin(self, email, password):
        browser = self.browser

        browser.open(LOGIN_URL)
        browser.select_form(nr = 0) # selects the first form on the login page

        ##### 1 #####
        # POST https://www.strava.com/session, email=<STRAVA EMAIL>, password=<STRAVA PASSWORD>
        # -> Sets _strava4_session, strava_remember_id, and strava_remember_token cookies
        browser.form['email'] = email
        browser.form['password'] = password
        browser.form['remember_me'] = ['on']
        browser.submit()

        ##### 2 #####
        # GET https://heatmap-external-a.strava.com/auth with session cookies set
        # -> Sets CloudFront-Signature, CloudFront-Policy, and CloudFront-Key-Pair-Id cookies
        browser.open(AUTH_URL)
