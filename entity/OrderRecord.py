class OrderRecord:
    def __init__(self, id, order, status, timestamp, fill_price=None, fill_volume=None):
        self.__id = id
        self.__order = order
        self.__status = status
        self.__timestamp = timestamp

        if fill_price is None:
            self.__fill_price = order.get_init_price()
        else:
            self.__fill_price = fill_price

        if fill_price is None:
            self.__fill_volume = order.get_init_volume()
        else:
            self.__fill_volume = fill_volume

    def get_fill_price(self):
        return self.__fill_price

    def get_fill_volume(self):
        return self.__fill_volume

    def set_fill_price(self, value):
        self.__fill_price = value

    def set_fill_volume(self, value):
        self.__fill_volume = value

    def get_status(self):
        return self.__status

    def __str__(self):
        return "{},{},{},{},{},{}".format(str(self.__order), self.__fill_price, self.__fill_volume, self.__status, self.__timestamp, self.__id)
