class StravaImgUpdError(Exception):
    """Base class for exceptions in this module."""
    pass

class StravaImgUpdCookieError(StravaImgUpdError):
    def __init__(self, message):
        self.message = message

class StravaImgUpdOsError(StravaImgUpdError):
    def __init__(self, message):
        self.message = message
