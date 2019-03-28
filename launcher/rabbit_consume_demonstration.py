import traceback

import service.database.mysql as mysql
import service.message_broker.rabbitmq as rabbit
import config
import config.PathProvider as provider
import root
import util
import service.file as sf

counter = 0


def callback(ch, method, properties, body):
    global counter
    try:
        connector = mysql.default_connect()
        body = body.decode("utf-8")
        body = str(body).replace('order_notes', 'order_notes_rabbit', 1)
        mysql.execute_query(body, connector)
        counter += 1
        util.logger.log_info("Insert data from message: {}. Total processed messages:{}".format(body, counter))
        mysql.close(connector)
    except:
        util.logger.log_warn(traceback.format_exc())


def from_rabbitmq_queue():
    try:
        rabbit_connection = rabbit.open_connection(config.settings["rabbit"]["host"])
        channel = rabbit_connection.channel()
        rabbit.declare_queue(channel, config.settings["rabbit"]["routing_key"])
        util.logger.log_info("Start messages consuming")
        print("To finish press Ctrl+C...")
        rabbit.consume_messages(channel, config.settings["rabbit"]["routing_key"], callback=callback)
        rabbit.close_connection(rabbit_connection)
        util.logger.log_info("Finish messages consuming")
    except:
        util.logger.log_warn(traceback.format_exc())


def setup():
    provider.load(root.__file__)
    try:
        log_path = "{}_rabbit".format(provider.pathes["LOG"].location)
        util.logger.setup(sf.append, log_path)
        config.load()
    except:
        util.logger.log_level = 1
        util.logger.log_fatal(traceback.format_exc())
    else:
        util.logger.log_level = config.settings["log_level"]
        util.delete_excess_files(log_path, config.settings["logger_files_max"])


def run():
    from_rabbitmq_queue()


if __name__ == "__main__":
    setup()
    run()
