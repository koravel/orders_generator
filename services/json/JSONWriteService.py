from services.file.FileWriteService import FileWriteService
from services.json.JSONCoder import JSONCoder


class JSONWriteService(FileWriteService):
    @staticmethod
    def write(obj, obj_location, extended_encoder=None):
        super().write(JSONCoder.encode(obj, extended_encoder), obj_location)
