import http.server
import socketserver
import time

from app_threading.TaskThread import TaskThread
from app_threading.ThreadPool import ThreadPool
from config.provider import SettingsKeys
from config.provider.SettingsProvider import SettingsProvider
from reporter.Repoter import Reporter
from service.file.FileWriteService import FileWriteService


class ReportSender:
    def __init__(self, logger):
        self.__logger = logger
        self.__settings = None
        self.__thread_pool = None

    def initialize(self, data_collector, settings_location=""):
        self.__data_collector = data_collector
        self.reporter = Reporter(self.__data_collector.data)

        if settings_location != "":
            settings_provider = SettingsProvider(location=settings_location, logger=self.__logger)
            self.__settings = settings_provider.load()

        self.host = self.__settings[SettingsKeys.reporter][SettingsKeys.host]
        self.port = self.__settings[SettingsKeys.reporter][SettingsKeys.port]


        Handler = http.server.SimpleHTTPRequestHandler
        self.server = socketserver.TCPServer((self.host, int(self.port)), Handler)
        self.ip, self.port = self.server.server_address


        self.__setup_thread_pool()

    def __setup_thread_pool(self):
        self.__thread_pool = ThreadPool(self.__logger)
        self.__thread_pool.setup(threads_max=self.__settings[SettingsKeys.system][SettingsKeys.threads_max],
                                 queue_max=self.__settings[SettingsKeys.system][SettingsKeys.queue_max])

        self.__thread_pool.set_event("stop_all")
        self.__thread_pool.unset_event("stop_all")

        report_server_thread = TaskThread("report_server_loop", self.__thread_pool, self.__logger)
        report_server_thread.setup(task=self.server_loop)
        report_server_thread.setDaemon(True)

        report_thread = TaskThread("report_loop", self.__thread_pool, self.__logger)
        report_thread.setup(task=self.report_loop)

        self.__thread_pool.add_thread(thread=report_server_thread)
        self.__thread_pool.add_thread(thread=report_thread)

    def run(self):
        print("Report sender serving at {}:{}".format(self.host, self.port))
        self.__thread_pool.start_thread("report_server_loop")
        self.__thread_pool.start_thread("report_loop")

    def report_loop(self, events, data, logger):
        stop_event = events["stop_all"]

        while not stop_event.is_set():
            self.generate_report()
            time.sleep(1)
        self.server.shutdown()

    def server_loop(self, events, data, logger):
        self.server.serve_forever()

    def stop(self):
        self.__thread_pool.set_event("stop_all")

    def generate_report(self):
        result = self.reporter.get_report()
        FileWriteService.write(obj=result, obj_location="./index.html")
