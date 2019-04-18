from config.provider import SettingsKeys

def clear_services(config, mysql_service, rabbitmq_service):
    mysql_service.execute_query("truncate {};".format(config.settings[SettingsKeys.mysql][SettingsKeys.order_table]))
    rabbitmq_service.purge_queue("red")
    rabbitmq_service.purge_queue("green")
    rabbitmq_service.purge_queue("blue")
