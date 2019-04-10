from config.provider import SettingsKeys
from service.database.mysql.MySQLService import MySQLService
from service.message_broker.rabbitmq.RabbitMQService import RabbitMQService
from util.connection.MySQLConnection import MySQLConnection
from util.connection.RabbitMQConnection import RabbitMQConnection


def clear_services(config, logger):
    mysql_service = MySQLService(
        MySQLConnection(
            host=config.settings[SettingsKeys.mysql][SettingsKeys.host],
            port=config.settings[SettingsKeys.mysql][SettingsKeys.port],
            db=config.settings[SettingsKeys.mysql][SettingsKeys.database],
            user=config.settings[SettingsKeys.mysql][SettingsKeys.user],
            password=config.settings[SettingsKeys.mysql][SettingsKeys.password],
            logger=logger
        ),
        keep_connection_open=config.settings[SettingsKeys.mysql][SettingsKeys.keep_connection_open],
        logger=logger
    )

    rabbitmq_service = RabbitMQService(connection=RabbitMQConnection(
        host=config.settings[SettingsKeys.rabbit][SettingsKeys.host],
        port=config.settings[SettingsKeys.rabbit][SettingsKeys.port],
        vhost=config.settings[SettingsKeys.rabbit][SettingsKeys.vhost],
        user=config.settings[SettingsKeys.rabbit][SettingsKeys.user],
        password=config.settings[SettingsKeys.rabbit][SettingsKeys.password],
        logger=logger
    ),
        logger=logger)

    mysql_service.execute_query("truncate {};".format(config.settings[SettingsKeys.mysql][SettingsKeys.order_table]))
    rabbitmq_service.purge_queue("red")
    rabbitmq_service.purge_queue("green")
    rabbitmq_service.purge_queue("blue")
