class Path:
    def __init__(self, _location, _is_remote=False):
        self.location = _location
        self.is_remote = _is_remote

    def isoformat(self):
        """
        Rewrite default 'to json'-method
        """
        return {"location": self.location, "is_remote": self.is_remote}
