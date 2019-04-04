class Order:
    def __init__(self, id, position, currency_pair, direction, description, tags,
                 initial_timestamp, init_price, init_volume):
        self.__id = id
        self.__position = position
        self.__currency_pair = currency_pair
        self.__direction = direction
        self.__description = description
        self.__tags = tags
        self.__initial_timestamp = initial_timestamp
        self.__init_price = init_price
        self.__init_volume = init_volume

    def get_init_price(self):
        return self.__init_price

    def get_init_volume(self):
        return self.__init_volume

    def get_initial_timestamp(self):
        return self.__initial_timestamp

    def set_initial_timestamp(self, value):
        self.__initial_timestamp = value

    def set_position(self, value):
        self.__position = value

    def get_position(self):
        return self.__position

    def __str__(self):
        return "{},{},{},{},{},{},{}".format(
            self.__id, self.__currency_pair, self.__direction, self.__description,
            self.__init_price, self.__init_volume, self.__tags)
