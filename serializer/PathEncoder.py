import json


# override JSON encoder for PathProvider data structure
from config.Path import Path


class PathEncoder(json.JSONEncoder):
    def default(self, o):
        """
         Rewrite default encode method of Path object
        """
        if isinstance(o, Path):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)
