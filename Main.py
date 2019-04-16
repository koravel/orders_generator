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
            proto_records = App.to_proto(batch)

            App.to_rabbitmq(proto_records)

        App.start_rabbit_consuming()
        App.start_writing_to_mysql(Main.config)
        App.start_reporting()

    @staticmethod
    def finalize():
        App.finalize(Main.config)


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
