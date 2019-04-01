from config.SettingsProvider import SettingsProvider
from config.PathProvider import PathProvider
from config.ConfigManager import ConfigManager
from generator.constant.OrderGenConstantsProvider import OrderGenConstantsProvider


class Main:
    @staticmethod
    def initialize():
        providers = [
            PathProvider,
            SettingsProvider,
            #OrderGenConstantsProvider
        ]
        ConfigManager.load(providers)

    @staticmethod
    def run():
        pass

    @staticmethod
    def destroy():
        providers = [
            PathProvider,
            SettingsProvider,
            #OrderGenConstantsProvider
        ]
        ConfigManager.save(providers)


if __name__ == "__main__":
    #Main.initialize()
    #Main.run()
    #Main.destroy()
