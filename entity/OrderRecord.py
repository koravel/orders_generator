class OrderRecord:
    def __init__(self, id, order, status, timestamp, zone, fill_price=None, fill_volume=None):
        self.__id = id
        self.order = order
        self.__status = status
        self.__timestamp = timestamp
        self.__zone = zone

        if fill_price is None:
            self.__fill_price = order.get_init_price()
        else:
            self.__fill_price = fill_price

        if fill_price is None:
            self.__fill_volume = order.get_init_volume()
        else:
            self.__fill_volume = fill_volume

    def get_zone(self):
        return self.__zone

    def get_status(self):
        return self.__status

    def get_id(self):
        return self.__id

    def get_timestamp(self):
        return self.__timestamp

    def get_fill_price(self):
        return self.__fill_price

    def get_fill_volume(self):
        return self.__fill_volume

    def set_fill_price(self, value):
        self.__fill_price = value

    def set_fill_volume(self, value):
        self.__fill_volume = value

    def __str__(self):
        return "{},{},{},{},{},{},{}".format(str(self.order), self.__fill_price, self.__fill_volume, self.__status, self.__timestamp, self.__id, self.__zone)
