import os
from datetime import datetime

from llogging.BaseLogger import BaseLogger
from service.file.FileWriteService import FileWriteService


class FolderLogger(BaseLogger):
    def _write_to_destination(self, folder_path, log):
        file_path = os.path.join(folder_path, "{}.log".format(datetime.now().replace(microsecond=0)).replace(":", "_"))

        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        FileWriteService.append(log, file_path)
