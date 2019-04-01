class ConfigManager:
    @staticmethod
    def load(providers):
        for provider in providers:
            provider.load()

    @staticmethod
    def save(providers):
        for provider in providers:
            provider.save()
