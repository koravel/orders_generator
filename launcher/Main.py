from launcher.App import App


class Main:
    config = None
    logger = None
    path_provider = None
    settings_provider = None
    gen_settings_provider = None

    @staticmethod
    def initialize():
        Main.config, \
        Main.logger, \
        Main.path_provider, \
        Main.settings_provider, \
        Main.gen_settings_provider = App.initialize()


    @staticmethod
    def run():
        order_records = App.generate(Main.config, Main.logger)

        from datetime import datetime
        file_name = "{}.out".format(datetime.now().replace(microsecond=0)).replace(":", "_")

        App.to_file(Main.config, order_records, file_name)

        order_records = App.from_file(Main.config, file_name)

        App.to_mysql(Main.config, Main.logger, order_records)

        App.to_rabbitmq(Main.config, Main.logger, order_records)
    @staticmethod
    def finalize():
        App.finalize(Main.config, Main.path_provider, Main.settings_provider, Main.gen_settings_provider)


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
