import time

from app_logging.LogDistributorBuilder import LogDistributorBuilder
from app_logging.Logger import Logger
from config.provider import PathKeys, SettingsKeys
from config.provider.PathProvider import PathProvider
from config.provider.SettingsProvider import SettingsProvider
from launcher.Consumer import Consumer
from launcher.Generator import Generator
from launcher.ProtoConverter import ProtoConverter
from launcher.ReportSender import ReportSender
from launcher.Sender import Sender
from tracking.ReportDataCollector import ReportDataCollector


class Main:
    pathes = None
    logger = None
    consumer = None
    sender = None
    generator = None
    report_sender = None
    data_collector = None

    @staticmethod
    def initialize():
        log_distributor_builder = LogDistributorBuilder()
        default_log_distributor = log_distributor_builder.build_default()

        logger = Logger()
        logger.setup([default_log_distributor])

        path_provider = PathProvider(logger=logger)

        pathes = path_provider.load(load_default=True)

        log_distributor_builder.setup(pathes[PathKeys.SETTINGS].location)
        log_distributors = log_distributor_builder.build_all()

        logger.setup(log_distributors=log_distributors)

        data_collector = ReportDataCollector(logger)
        data_collector.initialize(pathes[PathKeys.SETTINGS].location)

        Main.generator = Generator(logger)
        Main.generator.initialize(pathes[PathKeys.GEN_SETTINGS].location)
        Main.generator.add_collector(data_collector)

        Main.sender = Sender(logger)
        Main.sender.initialize(pathes[PathKeys.SETTINGS].location)

        Main.consumer = Consumer(logger)
        Main.consumer.initialize(pathes[PathKeys.SETTINGS].location, pathes[PathKeys.GEN_SETTINGS].location)
        Main.consumer.add_collector(data_collector)

        Main.report_sender = ReportSender(logger)
        Main.report_sender.initialize(data_collector, pathes[PathKeys.SETTINGS].location)

        Main.logger = logger
        Main.pathes = pathes
        Main.data_collector = data_collector

    @staticmethod
    def run():
        Main.consumer.run()
        Main.sender.run()
        Main.report_sender.run()
        Main.data_collector.run()

        order_records_generator = Main.generator.generate()
        for batch in order_records_generator:
            Main.sender.add_batch_to_buffer(ProtoConverter.convert_batch(batch))

    @staticmethod
    def finalize():
        stop_delay = SettingsProvider(
            location=Main.pathes[PathKeys.SETTINGS].location,
            logger=Main.logger).load()[SettingsKeys.system][SettingsKeys.manual_stop]
        if stop_delay > 0:
            time.sleep(stop_delay)

        Main.sender.stop()
        Main.consumer.stop()
        Main.report_sender.stop()
        Main.data_collector.stop()


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
