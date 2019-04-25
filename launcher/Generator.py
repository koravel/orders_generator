from datetime import datetime

from analysis.RecordsDataProcessor import RecordsDataProcessor
from config.provider import GenSettingsKeys
from generator.OrderRecordConstructor import OrderRecordConstructor
from config.provider.SettingsProvider import SettingsProvider
from tracking import ReportDataKeys
from tracking.DataProvider import DataProvider


class Generator(DataProvider):
    def __init__(self, logger):
        self.__logger = logger
        self.__settings = None
        self.__collectors = []

    def add_collector(self, collector):
        self.__collectors.append(collector)

    def remove_collector(self, collector):
        self.__collectors.remove(collector)

    def initialize(self, settings_location):
        gen_settings_provider = SettingsProvider(location=settings_location, logger=self.__logger)

        self.__settings = gen_settings_provider.load()

    def generate(self):
        order_record_constructor = OrderRecordConstructor(self.__settings, self.__logger)
        order_record_constructor.setup_generators(
            x=self.__settings[GenSettingsKeys.x],
            y=self.__settings[GenSettingsKeys.y],
            a=self.__settings[GenSettingsKeys.a],
            c=self.__settings[GenSettingsKeys.c],
            m=self.__settings[GenSettingsKeys.m],
            t0=self.__settings[GenSettingsKeys.t0])

        order_record_sequence = order_record_constructor.get_sequence()

        records = []

        order_records_amount = order_record_constructor.get_order_records_amount()

        counter = int(order_records_amount / self.__settings[GenSettingsKeys.portion_amount])
        timer = datetime.now()
        for record in order_record_sequence:
            records.append(record)

            for collector in self.__collectors:
                collector.set_data(key=record.get_zone(),
                                   second_key=ReportDataKeys.gen_time,
                                   object=datetime.now() - timer)

                collector.set_data(object=RecordsDataProcessor.get_result(collector.get_data(), zone=record.get_zone()))

            if len(records) == self.__settings[GenSettingsKeys.portion_amount] and counter > 0:
                counter -= 1

                yield records
                records = []

            timer = datetime.now()

        if len(records) > 0:
            yield records
