import os
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
    def setup(self, append, location, _log_level=_LogLevel.INFO):
        self.__append = append
        self.__location = location
        self.__log_level = _log_level
        self.__file = "{}.log".format(datetime.now().replace(microsecond=0)).replace(":", "_")

        if not path.isdir(location):
            os.mkdir(location)

    def __log(self, log_level, text):
        """
        Format: [current_time][log_level]: text
        """
        if self.__log_level >= log_level:
            log = "[{}][{}]: {}\n".format(datetime.now().replace(microsecond=0), _LogLevel.title[log_level], text)

            if self.__append is None:
                print(log)
            else:
                self.__append(log, path.join(self.__location, self.__file))

    def log_trace(self, text):
        self.__log(_LogLevel.TRACE, text)

    def log_debug(self, text):
        self.__log(_LogLevel.DEBUG, text)

    def log_info(self, text):
        self.__log(_LogLevel.INFO, text)

    def log_warn(self, text):
        self.__log(_LogLevel.WARN, text)

    def log_error(self, text):
        self.__log(_LogLevel.ERROR, text)

    def log_critical(self, text):
        self.__log(_LogLevel.CRITICAL, text)

    def log_fatal(self, text):
        self.__log(_LogLevel.FATAL, text)
