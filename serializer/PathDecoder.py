import json


# override JSON decoder for PathProvider data structure
from config.Path import Path


class PathDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    @staticmethod
    def object_hook(obj):
        """
         Rewrite default decode method of Path object
        """
        if 'location' in obj:
            return Path(obj.get('location'), obj.get('is_remote'))
        return obj
