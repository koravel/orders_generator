from config.provider import SettingsKeys
from service.database.mysql.CRUDService import CRUDService
from util.connection.MySQLConnection import MySQLConnection


class MySQLServiceBuilder:
    @staticmethod
    def build(settings, logger):
        return CRUDService(MySQLConnection(
            host=settings[SettingsKeys.mysql][SettingsKeys.host],
            port=settings[SettingsKeys.mysql][SettingsKeys.port],
            db=settings[SettingsKeys.mysql][SettingsKeys.database],
            user=settings[SettingsKeys.mysql][SettingsKeys.user],
            password=settings[SettingsKeys.mysql][SettingsKeys.password],
            logger=logger
        ),
            keep_connection_open=settings[SettingsKeys.mysql][SettingsKeys.keep_connection_open],
            attempts=settings[SettingsKeys.mysql][SettingsKeys.connection_attempts],
            delay=settings[SettingsKeys.mysql][SettingsKeys.connection_attempts_delay],
            instant_connection_attempts=settings[SettingsKeys.mysql][SettingsKeys.instant_connection_attempts],
            logger=logger
        )
