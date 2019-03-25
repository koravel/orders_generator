from services.file.FileReadService import FileReadService
from services.json.JSONCoder import JSONCoder


class JSONReadService(FileReadService):
    @staticmethod
    def read(obj_location, extended_decoder=None):
        try:
            result = JSONCoder.decode(super().read_all(obj_location), extended_decoder)
        except Exception as ex:
            raise ex
        else:
            return result
