from datetime import datetime

from config.provider import GenSettingsKeys
from entity.Order import Order, StatusKeys
from generator.CurrencyPairGenerator import CurrencyPairGenerator
from generator.DescriptionGenerator import DescriptionGenerator
from generator.DirectionGenerator import DirectionGenerator
from generator.IdGenerator import IdGenerator
from generator.PriceDeviationGenerator import PriceDeviationGenerator
from generator.LastStatusGenerator import LastStatusGenerator
from generator.TagGenerator import TagGenerator
from generator.TimestampGenerator import TimestampGenerator
from generator.VolumeGenerator import VolumeGenerator


class OrderConstructor:
    def __init__(self, gen_settings, logger):
        self.logger = logger
        self.orders_amount = gen_settings[GenSettingsKeys.orders_amount]
        self.id_length = gen_settings[GenSettingsKeys.id_length]
        self.currency_pairs = gen_settings[GenSettingsKeys.currency_pairs]
        self.descriptions = gen_settings[GenSettingsKeys.descriptions]
        self.tags = gen_settings[GenSettingsKeys.tags]
        self.days_amount = gen_settings[GenSettingsKeys.days_amount]
        self.init_date = gen_settings[GenSettingsKeys.date]
        self.price_precision = gen_settings[GenSettingsKeys.price_precision]
        self.volume_precision = gen_settings[GenSettingsKeys.volume_precision]
        self.statuses = gen_settings[GenSettingsKeys.statuses]
        self.directions = gen_settings[GenSettingsKeys.direction]
        self.weekends = gen_settings[GenSettingsKeys.weekends]

        self.red_percent = gen_settings[GenSettingsKeys.zones_percents][0]
        self.green_percent = gen_settings[GenSettingsKeys.zones_percents][1]
        self.blue_percent = gen_settings[GenSettingsKeys.zones_percents][2]

        self.one_state_red_percent = gen_settings[GenSettingsKeys.one_state_percent]["Red"]
        self.one_state_blue_percent = gen_settings[GenSettingsKeys.one_state_percent]["Blue"]

        self.red_zone_amount = self.orders_amount * self.red_percent
        self.green_zone_amount = self.orders_amount * self.green_percent
        self.blue_zone_amount = self.orders_amount * self.blue_percent

        self.red_zone_finish = self.red_zone_amount
        self.green_zone_finish = self.red_zone_finish + self.green_zone_amount
        self.blue_zone_finish = self.green_zone_finish + self.blue_zone_amount

        self.one_state_red_finish = self.red_zone_finish * self.one_state_red_percent
        self.one_state_blue_start = self.green_zone_finish + (1 - self.one_state_blue_percent) * self.blue_zone_amount

    def setup_generators(self, x, y, a, c, m, t0, min=-16384, max=16384):
        """
         Setup order data generator
         'id_generator' - fixed length ids
         'currency_generator' - id of currency pair
         'direction_generator' - id of direction
         'description_generator' - id of direction
         'tag_generator' - array of tag ids
         'date_generator' - date from constant + additive,
         that depends on orders amount, days amount, weekends
         'price_generator' - additive to currency pair value
         'volume_generator' - order volume, just integers
         'last_status_generator' - id of status of set 'rejected/partial_filled/filled'
         All data related to ids etc. can be found in generator.constant
        """
        try:
            self.id_generator = IdGenerator(self.logger, self.id_length).get_sequence(length=self.orders_amount, x=x, y=y)

            self.currency_generator = CurrencyPairGenerator(self.logger, currency_pairs=self.currency_pairs).get_sequence(
                length=self.orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.direction_generator = DirectionGenerator(self.logger).get_sequence(length=self.orders_amount, x=x, y=y)

            self.description_generator = DescriptionGenerator(self.logger, descriptions_amount=len(self.descriptions)).get_sequence(
                length=self.orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.tag_generator = TagGenerator(self.logger, tags_amount=len(self.tags),).get_arr_sequence(
                length=self.orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            timestamp_generator_instance = TimestampGenerator(self.logger, date=self.init_date, days_amount=self.days_amount)

            self.timestamp_generator = timestamp_generator_instance.get_sequence(
                length=self.orders_amount, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.timestamp_add_sec_generator = timestamp_generator_instance.get_additive_ms_sequence(
                length=self.orders_amount * 3, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.price_generator = PriceDeviationGenerator(self.logger, price_precision=self.price_precision).get_sequence(
                length=self.orders_amount, x=x, y=y)

            self.volume_generator = VolumeGenerator(self.logger).get_sequence(
                length=self.orders_amount, volume_precision=self.volume_precision, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.last_status_generator = LastStatusGenerator(self.logger).get_sequence(
                length=self.orders_amount, statuses=self.statuses, x=x, y=y, a=a, c=c, m=m, t0=t0)
        except:
            self.logger.log_error("Order construction setup error", include_traceback=True)
        else:
            self.logger.log_info("Generators initialized successfully")

    def __generate_plain_order(self, position):
        """
        Creates order with data generators
        """
        try:
            price_additive = self.price_generator.__next__()
            price_diff = 1 - price_additive
            volume = self.volume_generator.__next__()

            id = self.id_generator.__next__()
            direction = self.directions[self.direction_generator.__next__()]
            currency_pair, currency_value = self.currency_generator.__next__()
            description = self.descriptions[self.description_generator.__next__()]
            tags = self.__get_tags_string(self.tag_generator.__next__())
            initial_timestamp = self.timestamp_generator.__next__()
            init_price = currency_value
            fill_price = currency_value + price_additive
            init_volume = volume
            fill_volume = volume * price_diff

            order = Order(id, position, currency_pair, direction, description, tags,
                          initial_timestamp, init_price, init_volume, dict(), fill_price, fill_volume)

            order.statuses = self.__generate_zoned_status(order)
        except Exception as ex:
            raise ex
        else:
            return order

    def __generate_status_data(self, status, order):
        """
        Creates order with status and status date, adds to order data
        """
        try:
            timestamp = round(self.__get_status_timestamp(status, order.initial_timestamp), 3)
            if self.__is_weekend(timestamp):
                if status != self.statuses[0]:
                    old_timestamp = timestamp
                    while self.__is_weekend(timestamp):
                        timestamp += 86400
                    self.logger.log_trace(
                        "[Order][{}] Add {} sec to timestamp: {}. Previous value {} was a weekend".format
                        (order["id"], timestamp - old_timestamp, timestamp, old_timestamp))
            result = {
                StatusKeys.title: status,
                StatusKeys.timestamp: timestamp
            }
        except Exception as ex:
            raise ex
        else:
            return result

    def get_sequence(self):
        """
       Returns orders generator
       """
        self.logger.log_info("Generating {} orders...".format(self.orders_amount))
        i = 0
        try:
            for i in range(self.orders_amount):
                order = self.__generate_plain_order(i)
                self.logger.log_trace(order)
                yield order
        except:
            self.logger.log_error("Unable to generate orders", include_traceback=True)
        finally:
            self.logger.log_info("Generated {} orders...".format(i + 1))

    def __get_tags_string(self, next_arr):
        """
        Convert ids array to tag string
        """
        tags = ""
        for id in next_arr:
            tags += self.tags[id] + ','
        return tags[:-1]

    def __get_status_timestamp(self, status, initial_timestamp):
        """
        Returns date of order record depending on the note status:
        'New' : initial date - additive
        'To provider' : just initial date
        'Rejected/Partial filled/Filled' : initial date + additive
        """
        date_additive = self.timestamp_add_sec_generator.__next__()
        if status == self.statuses[0]:
            initial_timestamp -= date_additive
        elif status in self.statuses[2:4]:
            initial_timestamp += date_additive
        return initial_timestamp

    def __get_fill_values(self, status, initial_price, initial_volume, fill_price, fill_volume):
        """
        Returns fill price and volume of order note depending on the note status
        'New/To provider/Rejected' : zeros
        'Partial filled' : fill values
        'Filled' : initial values
        """
        if status == self.statuses[4]:
            return initial_price, initial_volume
        elif status == self.statuses[3]:
            return fill_price, fill_volume
        else:
            return 0, 0

    def __is_weekend(self, timestamp):
        """
        Checks is timestamp weekend
        """
        return datetime.fromtimestamp(timestamp / 1000).weekday() in self.weekends

    def __generate_red_status(self, order):
        """
        Creates at least 1 status data in red zone.
        Amount depends on order zone/position:
        it may be note only with 'rejected/filled/p_filled'
        or two notes - second with 'to_provider'
        """
        try:
            result = self.__generate_status_data(self.last_status_generator.__next__(), order)
            if order.position > self.one_state_red_finish:
                result.update(self.__generate_status_data(self.statuses[1], order))
        except Exception as ex:
            raise ex
        else:
            return result

    def __generate_green_status(self, order):
        """
        Creates 3 order notes with statuses 'new', 'to_provider' and 'rejected/filled/p_filled'
        """
        try:
            result = dict()
            i = 0
            while i < 3:
                result.update(self.__generate_status_data(self.statuses[i], order))
                i += 1
        except Exception as ex:
            raise ex
        else:
            return result

    def __generate_blue_status(self, order):
        """
        Creates at least 1 order note in blue zone.
        Amount depends on order zone/position:
        it may be note only with 'new'
        or two notes - second with 'to_provider'
        """
        try:
            result = self.__generate_status_data(self.statuses[0], order)
            if order.position <= self.one_state_blue_start:
                result.update(self.__generate_status_data(self.statuses[1], order))
        except Exception as ex:
            raise ex
        else:
            return result

    def __generate_zoned_status(self, order):
        """
        Generate notes from order depending on the order position/zone
        """
        try:
            if order.position <= self.red_zone_finish:
                return self.__generate_red_status(order)
            elif order.position <= self.green_zone_finish:
                return self.__generate_green_status(order)
            elif order.position <= self.blue_zone_finish:
                return self.__generate_blue_status(order)
            return None
        except:
            self.logger.log_error("Cannot generate zone-specified status", include_traceback=True)

    def get_notes_amount(self):
        """
        Returns notes amount depending on the zone colors and 1-state percents
        """
        notes_amount = self.orders_amount * (self.green_percent * 3 +
                                             self.red_percent * (2 - self.one_state_red_percent) +
                                             self.blue_percent * (2 - self.one_state_blue_percent))
        return notes_amount
