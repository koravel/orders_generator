from datetime import datetime

from launcher.App import App


class Main:
    config = None
    logger = None
    path_provider = None
    settings_provider = None
    gen_settings_provider = None
    timings = dict()

    @staticmethod
    def initialize():
        Main.timings["setup"] = datetime.now()
        Main.config, \
        Main.logger, \
        Main.path_provider, \
        Main.settings_provider, \
        Main.gen_settings_provider = App.initialize()
        Main.timings["setup"] = datetime.now() - Main.timings["setup"]


    @staticmethod
    def run():
        Main.timings["gen"] = datetime.now()
        order_records = App.generate(Main.config, Main.logger)
        Main.timings["gen"] = datetime.now() - Main.timings["gen"]

        file_name = "{}.out".format(datetime.now().replace(microsecond=0)).replace(":", "_")

        Main.timings["to_file"] = datetime.now()
        App.to_file(Main.config, order_records, file_name)
        Main.timings["to_file"] = datetime.now() - Main.timings["to_file"]

        Main.timings["from_file"] = datetime.now()
        order_records = App.from_file(Main.config, file_name)
        Main.timings["from_file"] = datetime.now() - Main.timings["from_file"]

        Main.timings["mysql"] = datetime.now()
        #App.to_mysql(Main.config, Main.logger, order_records)
        Main.timings["mysql"] = datetime.now() - Main.timings["mysql"]

        Main.timings["proto"] = datetime.now()
        proto_records = App.to_proto(order_records)
        Main.timings["proto"] = datetime.now() - Main.timings["proto"]

        Main.timings["rabbit"] = datetime.now()
        App.to_rabbitmq(Main.config, Main.logger, proto_records)
        Main.timings["rabbit"] = datetime.now() - Main.timings["rabbit"]

        App.report(Main.logger, Main.timings, proto_records)

    @staticmethod
    def finalize():
        App.finalize(Main.config, Main.path_provider, Main.settings_provider, Main.gen_settings_provider)


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
