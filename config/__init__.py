import os

import root
import util


__root_location = os.path.dirname(os.path.abspath(root.__file__))
__pathes_file_name = "pathes.json"


def get_pathes_config_location():
    return util.join_pathes(__root_location, __pathes_file_name)


def get_root_location():
    return __root_location


def get_pathes_file_name():
    return __pathes_file_name
