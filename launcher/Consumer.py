import time

from builder.MySQLServiceBuilder import MySQLServiceBuilder
from builder.RabbitMQBuilder import RabbitMQBuilder
from app_threading.TaskThread import TaskThread
from app_threading.ThreadPool import ThreadPool
from config.provider import SettingsKeys, GenSettingsKeys
from config.provider.SettingsProvider import SettingsProvider
from serializer.proto.OrderRecord_pb2 import OrderRecord
from entity.OrderRecord import OrderRecord as OrderRecordDTO
from tracking import ReportDataKeys, select_report_data_query
from tracking.DataProvider import DataProvider


class Consumer(DataProvider):
    def add_collector(self, collector):
        self.__collectors.append(collector)

    def remove_collector(self, collector):
        self.__collectors.remove(collector)

    def __init__(self, logger):
        self.__logger = logger
        self.__settings = None
        self.__thread_pool = None
        self.__collectors = []
        self.__rabbitmq_service = None
        self.__mysql_service = None

        self.__queues = []
        self.__batch_buffer = []

    def initialize(self, settings_location, gen_settings_location):
        settings_provider = SettingsProvider(location=settings_location, logger=self.__logger)
        self.__settings = settings_provider.load()

        gen_settings_provider = SettingsProvider(location=gen_settings_location, logger=self.__logger)
        gen_settings = gen_settings_provider.load()

        self.__batch_amount = gen_settings[GenSettingsKeys.portion_amount]

        self.__setup_thread_pool()
        self.__setup_services()

    def run(self):
        self.__thread_pool.start_thread("rabbit_consuming")
        self.__thread_pool.start_thread("mysql_writing")

    def stop(self):
        self.__thread_pool.set_event("stop_all")

    def __setup_thread_pool(self):
        self.__thread_pool = ThreadPool(self.__logger)
        self.__thread_pool.setup(threads_max=self.__settings[SettingsKeys.system][SettingsKeys.threads_max],
                                 queue_max=self.__settings[SettingsKeys.system][SettingsKeys.queue_max])

        self.__thread_pool.set_event("stop_all")
        self.__thread_pool.unset_event("stop_all")

        consume_thread = TaskThread("rabbit_consuming", self.__thread_pool, self.__logger)
        mysql_thread = TaskThread("mysql_writing", self.__thread_pool, self.__logger)

        consume_thread.setup(task=self.__run_consuming)
        mysql_thread.setup(task=self.__run_writing_to_mysql)

        self.__thread_pool.add_thread(thread=consume_thread)
        self.__thread_pool.add_thread(thread=mysql_thread)

    def __setup_services(self):
        self.__rabbitmq_service = RabbitMQBuilder.build(self.__settings, self.__logger)
        self.__queues = self.__settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.queues]

        self.__mysql_service = MySQLServiceBuilder.build(self.__settings, self.__logger)

        if self.__settings[SettingsKeys.system]["clear"]:
            from launcher import clear_services
            clear_services(self.__settings, self.__mysql_service, self.__rabbitmq_service)

    def __consume_callback(self, ch, method, properties, body):
        order_record = OrderRecord()
        order_record.ParseFromString(body)
        values = [
            order_record.order_id,
            order_record.status,
            order_record.timestamp,
            order_record.currency_pair,
            order_record.direction,
            order_record.init_price,
            order_record.fill_price,
            order_record.init_volume,
            order_record.fill_volume,
            order_record.tags,
            order_record.description
        ]
        self.__batch_buffer.append(values)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        for collector in self.__collectors:
            consumed = collector.get_data(ReportDataKeys.rabbit_consumed) + 1
            collector.set_data(key=ReportDataKeys.rabbit_consumed, object=consumed)

    def __run_consuming(self, events, data, logger):
        for queue_name in self.__queues:
            self.__rabbitmq_service.consume_message(queue_name=queue_name, on_consume_callback=self.__consume_callback)

        consume_thread = TaskThread("pika_start_consuming", self.__thread_pool, self.__logger)
        consume_thread.setup(task=self.__run_pika_consume)
        consume_thread.setDaemon(True)

        self.__thread_pool.add_thread(thread=consume_thread)
        self.__thread_pool.start_thread("pika_start_consuming")

        stop_event = events["stop_all"]
        while not stop_event.is_set():
            time.sleep(1)
        self.__rabbitmq_service.stop_consuming()

    def __run_pika_consume(self, events, data, logger):
        self.__rabbitmq_service.start_consuming()

    def __batch_to_mysql(self):
        try:
            if len(self.__batch_buffer) >= self.__batch_amount:
                amount = self.__batch_amount
            else:
                amount = len(self.__batch_buffer)

            self.__mysql_service.insert_many(location=self.__settings[SettingsKeys.mysql][SettingsKeys.order_table],
                                             fields=OrderRecordDTO.text_fields, values=self.__batch_buffer[:amount])
            self.__batch_buffer = self.__batch_buffer[amount:]
        except:
            self.__logger.log_error()

    def __run_writing_to_mysql(self, events, data, logger):
        stop_event = events["stop_all"]
        while not stop_event.is_set():
            time.sleep(self.__settings[SettingsKeys.mysql][SettingsKeys.batch_delay])
            if len(self.__batch_buffer) > 0:
                self.__batch_to_mysql()
