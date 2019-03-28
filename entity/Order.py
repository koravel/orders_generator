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
        self.__statuses = dict()
        self.__fill_price = 0
        self.__fill_volume = 0

    def add_status(self, status_title, timestamp):
        self.__statuses[status_title] = timestamp

    def set_fill_price(self, price):
        self.__fill_price = price

    def set_fill_volume(self, volume):
        self.__fill_volume = volume