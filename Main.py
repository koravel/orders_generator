from datetime import datetime

from launcher.App import App


class Main:
    config = None
    timings = dict()

    @staticmethod
    def initialize():
        Main.config = App.initialize()

    @staticmethod
    def run():
        order_records = App.generate(Main.config)
        for batch in order_records:
            file_name = "{}.out".format(datetime.now().replace(microsecond=0)).replace(":", "_")

            # App.to_file(Main.config, order_records, file_name)

            # order_records = App.from_file(Main.config, file_name)

            # App.to_mysql(Main.config, Main.logger, order_records)

            proto_records = App.to_proto(batch)

            App.to_rabbitmq(proto_records)

        App.from_rabbit_to_mysql(Main.config)

        App.report()

    @staticmethod
    def finalize():
        App.finalize(Main.config)


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
