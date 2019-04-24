class UpdImgPrefsError(Exception):
    """Base class for exceptions in this module."""
    pass

class UpdImgPrefsCookieError(UpdImgPrefsError):
    pass

class UpdImgPrefsOsError(UpdImgPrefsError):
    def __init__(self, message):
        self.message = message
