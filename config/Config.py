import os

import root
from config import PathKeys
from config.Path import Path


class Config:
    settings = dict()
    pathes = dict()

    __root_location = root.__file__
    pathes_file_name = "pathes.json"
    default_pathes = {
        PathKeys.ROOT: Path(__root_location),
        PathKeys.LOG: Path(os.path.join(__root_location, "log")),
        PathKeys.SETTINGS: Path(os.path.join(__root_location, "settings.json")),
        PathKeys.CONSTANTS: Path(os.path.join(__root_location, "constants.json")),
        PathKeys.DEFAULT_SETTINGS: Path(os.path.join(__root_location, "constants-default.json")),
        PathKeys.DEFAULT_CONSTANTS: Path(os.path.join(__root_location, "settings-default.json")),
        PathKeys.GEN_OUT: Path(os.path.join(__root_location, "out"))
    }