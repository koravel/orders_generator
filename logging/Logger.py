import os
import traceback
from datetime import datetime
from os import path


class _LogLevel:
    OFF = 0
    FATAL = 1
    CRITICAL = 2
    ERROR = 3
    WARN = 4
    INFO = 5
    DEBUG = 6
    TRACE = 7

    title = {
        TRACE: "TRACE",
        DEBUG: "DEBUG",
        INFO: "INFO",
        WARN: "WARNING",
        ERROR: "ERROR",
        CRITICAL: "CRITICAL",
        FATAL: "FATAL"
    }


class Logger:
    def setup(self, append_method, location, _log_level=_LogLevel.INFO):
        self.__append_method = append_method
        self.__location = location
        self.__log_level = _log_level
        self.__file = "{}.log".format(datetime.now().replace(microsecond=0)).replace(":", "_")
        self.__out_error = False

        if not path.isdir(location):
            os.mkdir(location)

    def __log(self, log_level, text, include_traceback=False):
        """
        Format: [current_time][log_level]: text
        """
        if self.__log_level >= log_level:
            log = "[{}][{}]: {}\n".format(datetime.now().replace(microsecond=0), _LogLevel.title[log_level], text)
            if include_traceback:
                log = "{}\n{}".format(traceback.format_exc(), log)

            self.__transforming_log(log)

    def __transforming_log(self, log):
        if self.__append_method is None or self.__location is None:
            print(log)
            self.__transforming_log = print
        else:
            self.__append_method(log, path.join(self.__location, self.__file))

    def log_trace(self, text, include_traceback=False):
        self.__log(_LogLevel.TRACE, text, include_traceback)

    def log_debug(self, text, include_traceback=False):
        self.__log(_LogLevel.DEBUG, text, include_traceback)

    def log_info(self, text, include_traceback=False):
        self.__log(_LogLevel.INFO, text, include_traceback)

    def log_warn(self, text, include_traceback=False):
        self.__log(_LogLevel.WARN, text, include_traceback)

    def log_error(self, text, include_traceback=False):
        self.__log(_LogLevel.ERROR, text, include_traceback)

    def log_critical(self, text, include_traceback=False):
        self.__log(_LogLevel.CRITICAL, text, include_traceback)

    def log_fatal(self, text, include_traceback=False):
        self.__log(_LogLevel.FATAL, text, include_traceback)
