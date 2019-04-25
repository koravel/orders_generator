import time
from datetime import datetime, timedelta
from threading import Event

from app_threading.TaskThread import TaskThread
from builder.MySQLServiceBuilder import MySQLServiceBuilder
from config.provider import SettingsKeys
from config.provider.SettingsProvider import SettingsProvider
from tracking import ReportDataKeys
from tracking.DataCollector import DataCollector
from tracking import select_report_data_query


class ReportDataCollector(DataCollector):
    def __init__(self, logger):
        super(ReportDataCollector, self).__init__()
        self.__logger = logger
        self.__settings = None

        self.data = dict()

        self.__setup_zone_params(ReportDataKeys.red)
        self.__setup_zone_params(ReportDataKeys.green)
        self.__setup_zone_params(ReportDataKeys.blue)

        self.data[ReportDataKeys.rabbit_consumed] = 0

        self.data[ReportDataKeys.mysql_red] = 0
        self.data[ReportDataKeys.mysql_green] = 0
        self.data[ReportDataKeys.mysql_blue] = 0
        self.data[ReportDataKeys.mysql_total] = 0

    def initialize(self, settings_location):
        self.__settings = SettingsProvider(location=settings_location, logger=self.__logger).load()

        self.__setup_services()

        self.stop_event = Event()
        self.stop_event.set()
        self.stop_event.clear()

        self.sql_info_thread = TaskThread("sql_info_thread", None, self.__logger)
        self.sql_info_thread.setup(task=self.__update_sql_info_loop, events={"stop_all": self.stop_event})

    def __setup_services(self):
        self.__mysql_service = MySQLServiceBuilder.build(self.__settings, self.__logger)

    def __update_sql_info_loop(self, events, data, logger):
        stop_event = events["stop_all"]
        while not stop_event.is_set():
            time.sleep(1)
            db_info = self.__mysql_service.execute_query(query=select_report_data_query, fetch=True, commit=True,
                                                         attempts=self.__settings[SettingsKeys.mysql][
                                                             SettingsKeys.connection_attempts],
                                                         delay=self.__settings[SettingsKeys.mysql][
                                                             SettingsKeys.connection_attempts_delay],
                                                         instant_connection_attempts=self.__settings[SettingsKeys.mysql][
                                                             SettingsKeys.instant_connection_attempts],
                                                         )

            self.set_data(key=ReportDataKeys.mysql_red, object=db_info[0][0] + db_info[0][1])
            self.set_data(key=ReportDataKeys.mysql_blue, object=db_info[0][2] + db_info[0][3])
            self.set_data(key=ReportDataKeys.mysql_green, object=db_info[0][4])
            self.set_data(key=ReportDataKeys.mysql_total, object=db_info[0][5])

    def run(self):
        self.sql_info_thread.start()

    def stop(self):
        self.stop_event.set()

    def __setup_zone_params(self, key):
        self.data[key] = {
            ReportDataKeys.amount: 0,
            ReportDataKeys.avg: datetime.now() - datetime.now(),
            ReportDataKeys.min: timedelta(seconds=10),
            ReportDataKeys.max: datetime.now() - datetime.now(),
            ReportDataKeys.sum: datetime.now() - datetime.now()
        }

    def get_data(self, key=None, second_key=None):
        try:
            if key is None:
                return self.data

            if second_key is None:
                return self.data[key]
            return self.data[key][second_key]
        except:
            return None

    def set_data(self, object, key=None, second_key=None):
        try:
            if key is None:
                self.data = object
            if second_key is None:
                self.data[key] = object
            else:
                self.data[key][second_key] = object
        except Exception as ex:
            raise ex
