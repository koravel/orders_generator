from launcher.App import App


class Main:
    config = None
    logger = None
    path_provider = None
    settings_provider = None
    gen_settings_provider = None

    @staticmethod
    def initialize():
        Main.config, Main.logger, Main.path_provider, Main.settings_provider, Main.gen_settings_provider = App.initialize()


    @staticmethod
    def run():
        orders = App.generate(Main.config, Main.logger)
        App.to_file(Main.config, orders)

    @staticmethod
    def finalize():
        App.finalize(Main.config, Main.path_provider, Main.settings_provider, Main.gen_settings_provider)


if __name__ == "__main__":
    Main.initialize()
    Main.run()
    Main.finalize()
