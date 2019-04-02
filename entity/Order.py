class StatusKeys:
    title = "title"
    timestamp = "timestamp"


class Order:
    def __init__(self, id, position, currency_pair, direction, description, tags,
                 initial_timestamp, init_price, init_volume, statuses=None, fill_price=0, fill_volume=0):
        self.id = id
        self.position = position
        self.currency_pair = currency_pair
        self.direction = direction
        self.description = description
        self.tags = tags
        self.initial_timestamp = initial_timestamp
        self.init_price = init_price
        self.init_volume = init_volume
        self.statuses = statuses
        self.fill_price = fill_price
        self.fill_volume = fill_volume

    def __str__(self):
        return "{},{},{},{},{},{},{},{},\n{}\n{}".format(
            self.id, self.currency_pair, self.direction, self.description,
            self.init_price, self.init_volume, self.fill_price, self.fill_volume, self.tags, self.statuses)
