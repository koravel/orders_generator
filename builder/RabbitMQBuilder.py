from config.provider import SettingsKeys
from service.message_broker.rabbitmq.RabbitMQService import RabbitMQService
from util.connection.RabbitMQConnection import RabbitMQConnection


class RabbitMQBuilder:
    @staticmethod
    def build(settings, logger):
        return RabbitMQService(connection=RabbitMQConnection(
            host=settings[SettingsKeys.rabbit][SettingsKeys.host],
            port=settings[SettingsKeys.rabbit][SettingsKeys.port],
            vhost=settings[SettingsKeys.rabbit][SettingsKeys.vhost],
            user=settings[SettingsKeys.rabbit][SettingsKeys.user],
            password=settings[SettingsKeys.rabbit][SettingsKeys.password],
            retry_amount=settings[SettingsKeys.rabbit][SettingsKeys.retry_amount],
            retry_timeout=settings[SettingsKeys.rabbit][SettingsKeys.retry_timeout],
            logger=logger
        ),
            logger=logger)
