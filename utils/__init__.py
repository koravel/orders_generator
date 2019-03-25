import os
from datetime import datetime
from utils.Logger import Logger

# Global logger instance
logger = Logger()


def delete_excess_files(directory, max):
    """
    Delete excess files in directory, if amount more than max, starts with first file(may be incorrect in some OS)
    """
    files_amount = -1
    try:
        files = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]
        files_amount = len(files)

        while files_amount >= max:
            os.remove(os.path.join(directory, files[0]))
            files = [name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))]
            files_amount = len(files)
    except:
        logger.log_warn("Excess files in '{}' directory was not deleted correctly, {} files left"
                        .format(directory, files_amount))


def get_date_file_name(extension):
    """
    Format 'now' datetime and create file name
    with a given extension like this: 'YYYY_MM_DD hh_mm_ss.ext'
    """
    return "{}.{}".format(datetime.now().replace(microsecond=0), extension).replace(":", "_")
