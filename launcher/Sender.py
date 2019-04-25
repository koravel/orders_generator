from app_threading.TaskThread import TaskThread
from app_threading.ThreadPool import ThreadPool
from builder.RabbitMQBuilder import RabbitMQBuilder
from config.provider import SettingsKeys
from config.provider.SettingsProvider import SettingsProvider


class Sender:
    def __init__(self, logger):
        self.__logger = logger
        self.__settings = None
        self.__thread_pool = None
        self.__collectors = []
        self.__rabbitmq_service = None
        self.__buffer = []

        self.__queues = []
        self.__exchange_name = ""

    def add_array_to_buffer(self, obj):
        self.__buffer.extend(obj)

    def add_batch_to_buffer(self, obj):
        self.__buffer.append(obj)

    def yield_to_buffer(self, collection):
        for item in collection:
            self.__buffer.append(item)

    def initialize(self, settings_location):
        settings_provider = SettingsProvider(location=settings_location, logger=self.__logger)

        self.__settings = settings_provider.load()

        self.setup_thread_pool()

        self.setup_services()

    def run(self):
        self.__thread_pool.start_thread(obj="rabbitmq_sending")

    def stop(self):
        self.__thread_pool.set_event("stop_all")

    def setup_thread_pool(self):
        self.__thread_pool = ThreadPool(self.__logger)
        self.__thread_pool.setup(threads_max=self.__settings[SettingsKeys.system][SettingsKeys.threads_max],
                                 queue_max=self.__settings[SettingsKeys.system][SettingsKeys.queue_max],
                                 allow_duplicate_names_process=True)

        self.__thread_pool.set_event("stop_all")
        self.__thread_pool.unset_event("stop_all")

        sending_thread = TaskThread("rabbitmq_sending", self.__thread_pool, self.__logger)

        sending_thread.setup(task=self.to_rabbitmq)

        self.__thread_pool.add_thread(thread=sending_thread)

    def setup_services(self):
        self.__rabbitmq_service = RabbitMQBuilder.build(self.__settings, self.__logger)

        self.__exchange_name = self.__settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.exchange_name]
        exchange_mode = self.__settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.exchange_mode]
        self.__queues = self.__settings[SettingsKeys.rabbit][SettingsKeys.order_record_config][SettingsKeys.queues]

        self.__rabbitmq_service.declare_router(self.__exchange_name, exchange_mode)

        for queue_name in self.__queues:
            self.__rabbitmq_service.declare_queue(queue_name)
            self.__rabbitmq_service.bind_queue(queue_name, self.__exchange_name, queue_name)

    def to_rabbitmq(self, events, data, logger):
        stop_event = events["stop_all"]
        while not stop_event.is_set():
            if len(self.__buffer) > 0:
                for record in self.__buffer[0]:
                    self.__rabbitmq_service.send_message(self.__exchange_name, record.zone, record.SerializeToString())
                self.__buffer.remove(self.__buffer[0])
