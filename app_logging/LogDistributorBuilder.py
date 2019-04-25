from app_logging import _LogLevel
from app_logging.BaseLogger import BaseLogger
from app_logging.FileLogger import FileLogger
from app_logging.FolderLogger import FolderLogger
from app_logging.LogDistributor import LogDistributor
from app_logging.TransitFilter import TransitFilter
from config.provider import SettingsKeys
from config.provider.SettingsProvider import SettingsProvider


class _LoggerSettingOptions:
    type = "type"
    log_level = "log_level"
    destination = "destination"
    is_enabled = "is_enabled"


class _LoggerTypes:
    console = "console"
    folder = "folder"
    file = "file"


class LogDistributorBuilder:
    def setup(self, settings_location):
        settings_provider = SettingsProvider(location=settings_location)
        self.__loggers_settings = settings_provider.load()[SettingsKeys.logging][SettingsKeys.loggers]

    def build_all(self):
        log_distributors = []
        for logger_setting in self.__loggers_settings:
            if logger_setting[_LoggerSettingOptions.type] == _LoggerTypes.console:
                log_distributors.append(self.__build(logger_setting=logger_setting, distr_type=BaseLogger))
            elif logger_setting[_LoggerSettingOptions.type] == _LoggerTypes.folder:
                log_distributors.append(self.__build(logger_setting=logger_setting, distr_type=FolderLogger))
            elif logger_setting[_LoggerSettingOptions.type] == _LoggerTypes.file:
                log_distributors.append(self.__build(logger_setting=logger_setting, distr_type=FileLogger))
        return log_distributors

    @staticmethod
    def __build(distr_type, logger_setting):
        distributor = LogDistributor(
            logger=distr_type(
                log_level=logger_setting[_LoggerSettingOptions.log_level]
            ),
            transit_filter=TransitFilter(
                destination=logger_setting[_LoggerSettingOptions.destination],
                is_enabled=logger_setting[_LoggerSettingOptions.is_enabled]

            ))

        return distributor

    @staticmethod
    def build(log_level, destination, is_enabled, distr_type):
        distributor = LogDistributor(
            logger=distr_type(
                log_level=log_level
            ),
            transit_filter=TransitFilter(
                destination=destination,
                is_enabled=is_enabled

            ))

        return distributor

    @staticmethod
    def build_default():
        return LogDistributorBuilder.build(_LogLevel.TRACE, "", True, BaseLogger)
