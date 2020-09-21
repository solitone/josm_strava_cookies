class StravaCFetchError(Exception):
    """Base class for exceptions in this module."""
    pass

class StravaCFetchCookieError(StravaCFetchError):
    def __init__(self, message):
        self.message = message

class StravaCFetchOsError(StravaCFetchError):
    def __init__(self, message):
        self.message = message

class StravaCFetchJosmprefsError(StravaCFetchError):
    def __init__(self, message):
        self.message=message
