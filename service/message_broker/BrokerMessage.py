from datetime import datetime


class BrokerMessage:
    def __init__(self, message, lifetime):
        self.message = message
        self.expired_at = datetime.now().timestamp() + lifetime

    def is_valid(self):
        """
        :return: is message valid for caching
        """
        return self.expired_at < datetime.now().timestamp()
