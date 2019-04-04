from config.provider import GenSettingsKeys
from entity.Order import Order
from generator.CurrencyPairGenerator import CurrencyPairGenerator
from generator.DescriptionGenerator import DescriptionGenerator
from generator.DirectionGenerator import DirectionGenerator
from generator.IdGenerator import IdGenerator
from generator.PriceDeviationGenerator import PriceDeviationGenerator
from generator.TagGenerator import TagGenerator
from generator.TimestampGenerator import TimestampGenerator
from generator.VolumeGenerator import VolumeGenerator


class OrderConstructor:
    def __init__(self, gen_settings, logger):
        self.__logger = logger
        self.__orders_amount = gen_settings[GenSettingsKeys.orders_amount]
        self.__id_length = gen_settings[GenSettingsKeys.id_length]
        self.__currency_pairs = gen_settings[GenSettingsKeys.currency_pairs]
        self.__descriptions = gen_settings[GenSettingsKeys.descriptions]
        self.__tags = gen_settings[GenSettingsKeys.tags]
        self.__days_amount = gen_settings[GenSettingsKeys.days_amount]
        self.__init_date = gen_settings[GenSettingsKeys.date]
        self.__volume_precision = gen_settings[GenSettingsKeys.volume_precision]
        self.__directions = gen_settings[GenSettingsKeys.direction]

    def setup_generators(self, x, y, a, c, m, t0):
        """
         Setup order data generator
         'id_generator' - fixed length ids
         'currency_generator' - id of currency pair
         'direction_generator' - id of direction
         'description_generator' - id of direction
         'tag_generator' - array of tag ids
         'timestamp_generator' - date from config value,
         that depends on orders amount, days amount, weekends
         'volume_generator' - order volume, just integers
         All data related to ids etc. can be found in gen-settings-default.json
        """
        try:
            self.order_id_generator = IdGenerator(self.__logger, self.__id_length).get_sequence(
                length=self.__orders_amount, x=x, y=y)

            self.currency_generator = CurrencyPairGenerator(self.__logger,
                                                            currency_pairs=self.__currency_pairs).get_sequence(
                length=self.__orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.direction_generator = DirectionGenerator(self.__logger).get_sequence(length=self.__orders_amount, x=x, y=y)

            self.description_generator = DescriptionGenerator(self.__logger,
                                                              descriptions_amount=len(self.__descriptions)).get_sequence(
                length=self.__orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.tag_generator = TagGenerator(self.__logger, tags_amount=len(self.__tags), ).get_arr_sequence(
                length=self.__orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.timestamp_generator = TimestampGenerator(self.__logger, date=self.__init_date,
                                                          days_amount=self.__days_amount).get_sequence(
                length=self.__orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.volume_generator = VolumeGenerator(self.__logger).get_sequence(
                length=self.__orders_amount, volume_precision=self.__volume_precision, x=x, y=y, a=a, c=c, m=m, t0=t0)

        except:
            self.__logger.log_error("Order construction setup error")
        else:
            self.__logger.log_info("Order generators initialized successfully")

    def __generate_plain_order(self, position):
        """
        Creates order with data generators
        """
        try:
            currency_pair, init_price = self.currency_generator.__next__()

            order = Order(id = self.order_id_generator.__next__(),
                          position = position,
                          currency_pair = currency_pair,
                          direction = self.__directions[self.direction_generator.__next__()],
                          description = self.__descriptions[self.description_generator.__next__()],
                          tags = self.__get_tags_string(self.tag_generator.__next__(), ' '),
                          initial_timestamp = self.timestamp_generator.__next__(),
                          init_price = init_price,
                          init_volume = self.volume_generator.__next__()
                          )
        except Exception as ex:
            raise ex
        else:
            return order

    def __get_tags_string(self, next_arr, separator):
        """
        Convert ids array to tag string
        """
        tags = ""
        for id in next_arr:
            tags += self.__tags[id] + separator
        return tags[:-1]

    def get_sequence(self):
        """
       Returns orders generator
       """
        self.__logger.log_info("Generating {} orders...".format(self.__orders_amount))
        i = 1
        try:
            for i in range(self.__orders_amount):
                order = self.__generate_plain_order(i)
                self.__logger.log_trace(order)
                yield order
        except:
            self.__logger.log_error("Unable to generate orders")
        finally:
            self.__logger.log_info("Generated {} orders.".format(i + 1))
