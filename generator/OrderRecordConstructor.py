from datetime import datetime

from config.provider import GenSettingsKeys
from entity.OrderRecord import OrderRecord
from generator.IdGenerator import IdGenerator
from generator.LastStatusGenerator import LastStatusGenerator
from generator.OrderConstructor import OrderConstructor
from generator.PriceDeviationGenerator import PriceDeviationGenerator
from generator.TimestampGenerator import TimestampGenerator


class OrderRecordConstructor:
    def __init__(self, gen_settings, logger):
        self.__logger = logger
        self.__gen_settings = gen_settings
        self.__orders_amount = gen_settings[GenSettingsKeys.orders_amount]
        self.__id_length = gen_settings[GenSettingsKeys.id_length]
        self.__init_date = gen_settings[GenSettingsKeys.date]

        self.__weekends = gen_settings[GenSettingsKeys.weekends]
        self.__days_amount = gen_settings[GenSettingsKeys.days_amount]
        self.__price_precision = gen_settings[GenSettingsKeys.price_precision]
        self.__volume_precision = gen_settings[GenSettingsKeys.volume_precision]

        self.red_percent = gen_settings[GenSettingsKeys.zones_percents][0]
        self.green_percent = gen_settings[GenSettingsKeys.zones_percents][1]
        self.blue_percent = gen_settings[GenSettingsKeys.zones_percents][2]

        self.one_state_red_percent = gen_settings[GenSettingsKeys.one_state_percent]["Red"]
        self.one_state_blue_percent = gen_settings[GenSettingsKeys.one_state_percent]["Blue"]

        self.red_zone_amount = self.__orders_amount * self.red_percent
        self.green_zone_amount = self.__orders_amount * self.green_percent
        self.blue_zone_amount = self.__orders_amount * self.blue_percent

        self.red_zone_finish = self.red_zone_amount
        self.green_zone_finish = self.red_zone_finish + self.green_zone_amount
        self.blue_zone_finish = self.green_zone_finish + self.blue_zone_amount

        self.one_state_red_finish = self.red_zone_finish * self.one_state_red_percent
        self.one_state_blue_start = self.green_zone_finish + (1 - self.one_state_blue_percent) * self.blue_zone_amount

    def setup_generators(self, x, y, a, c, m, t0):
        """
         Setup order data generator
         'id_generator' - fixed length ids
          'price_deviation_generator' - additive to currency pair value
         'timestamp_add_ms_generator' - generates additive to order.initial_timestamp,
         that depends on orders amount, days amount, weekends
         'last_status_generator' - id of status of set 'rejected/partial_filled/filled'
         All data related to ids etc. can be found in gen-settings-default.json
        """
        try:
            self.order_record_id_generator = IdGenerator(self.__logger, self.__id_length).get_sequence(
                length=self.__orders_amount * 3, x=x, y=y)

            self.timestamp_add_ms_generator = TimestampGenerator(self.__logger, date=self.__init_date,
                                                                 days_amount=self.__days_amount).get_additive_ms_sequence(
                length=self.__orders_amount * 3, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.last_status_generator = LastStatusGenerator(self.__logger).get_sequence(
                length=self.__orders_amount * 3, x=x, y=y, a=a, c=c, m=m, t0=t0)

            self.price_deviation_generator = PriceDeviationGenerator(self.__logger,
                                                                     price_precision=self.__price_precision).get_sequence(
                length=self.__orders_amount * 3, x=x, y=y)


            orders_constructor = OrderConstructor(self.__gen_settings, self.__logger)
            orders_constructor.setup_generators(x, y, a, c, m, t0)
            self.orders_generator = orders_constructor.get_sequence()
        except:
            self.__logger.log_error("OrderRecord construction setup error")
        else:
            self.__logger.log_info("OrderRecord generators initialized successfully")

    def __get_status_timestamp(self, status, initial_timestamp):
        """
        Returns date of order record depending on the note status:
        'New' : initial date - additive
        'To provider' : just initial date
        'Rejected/Partial filled/Filled' : initial date + additive
        """
        date_additive = self.timestamp_add_ms_generator.__next__()
        if status == 0:
            initial_timestamp -= date_additive
        elif status in [2, 3, 4]:
            initial_timestamp += date_additive
        return initial_timestamp

    def __generate_status_data(self, status, order, zone):
        """
        Creates order with status and status date, adds to order data
        """
        try:
            timestamp = round(self.__get_status_timestamp(status, order.get_initial_timestamp()), 3)
            if self.__is_weekend(timestamp):
                if status != 0:
                    old_timestamp = timestamp
                    while self.__is_weekend(timestamp):
                        timestamp += 86400
                    self.__logger.log_trace(
                        "[OrderRecordGen][{}] Add {} sec to timestamp: {}. Previous value {} was a weekend".format
                        (order["id"], timestamp - old_timestamp, timestamp, old_timestamp))
            result = OrderRecord(
                                 order=order,
                                 timestamp=timestamp,
                                 status=status,
                                 zone=zone)
        except Exception as ex:
            raise ex
        else:
            return result

    def __get_fill_values(self, status, order):
        """
        Returns fill price and volume of order note depending on the note status
        'New/To provider/Rejected' : zeros
        'Partial filled' : fill values
        'Filled' : initial values
        """

        price_additive = self.price_deviation_generator.__next__()
        price_diff = 1 - price_additive
        fill_price = order.get_init_price() + price_additive
        fill_volume = order.get_init_volume() * price_diff

        if status == 5:
            return order.get_init_price(), order.get_init_volume()
        elif status == 4:
            fill_price = round(fill_price, self.__price_precision)
            fill_volume = round(fill_volume, self.__volume_precision)

            return fill_price, fill_volume
        else:
            return 0, 0

    def __is_weekend(self, timestamp):
        """
        Checks is timestamp weekend
        """
        return datetime.fromtimestamp(timestamp / 1000).weekday() in self.__weekends

    def __generate_red_status(self, order):
        """
        Creates at least 1 status data in red zone.
        Amount depends on order zone/position:
        it may be note only with 'rejected/filled/p_filled'
        or two notes - second with 'to_provider'
        """
        try:
            result = []
            result.append(self.__generate_status_data(self.last_status_generator.__next__(), order, "red"))
            if order.get_position() > self.one_state_red_finish:
                result.append(self.__generate_status_data(2, order, "red"))
        except Exception as ex:
            raise ex
        else:
            return result

    def __generate_green_status(self, order):
        """
        Creates 3 order notes with statuses 'new', 'to_provider' and 'rejected/filled/p_filled'
        """
        try:
            result = [self.__generate_status_data(1, order, "green"),
                      self.__generate_status_data(2, order, "green"),
                      self.__generate_status_data(self.last_status_generator.__next__(), order, "green")]
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
            result = []
            result.append(self.__generate_status_data(1, order, "blue"))
            if order.get_position() <= self.one_state_blue_start:
                result.append(self.__generate_status_data(2, order, "blue"))
        except Exception as ex:
            raise ex
        else:
            return result

    def __generate_zoned_order_records(self, order):
        """
        Generate notes from order depending on the order position/zone
        """
        try:
            if order.get_position() <= self.red_zone_finish:
                return self.__generate_red_status(order)
            elif order.get_position() <= self.green_zone_finish:
                return self.__generate_green_status(order)
            elif order.get_position() <= self.blue_zone_finish:
                return self.__generate_blue_status(order)
            return None
        except:
            self.__logger.log_error("Cannot generate zone-specified status")

    def get_sequence(self):
        self.__logger.log_info("Generating {} order records...".format(self.get_order_records_amount()))
        i = 0
        try:
            for order in self.orders_generator:
                order_records = self.__generate_zoned_order_records(order)
                for record in order_records:
                    fill_price, fill_volume = self.__get_fill_values(record.get_status(), order)
                    record.set_fill_price(fill_price)
                    record.set_fill_volume(fill_volume)
                    i += 1

                    yield record
        except:
            self.__logger.log_error("Unable to generate order records")
        finally:
            self.__logger.log_info("Generated {} order records.".format(i))

    def get_order_records_amount(self):
        """
        Returns notes amount depending on the zone colors and 1-state percents
        """
        notes_amount = self.__orders_amount * (self.green_percent * 3 +
                                               self.red_percent * (2 - self.one_state_red_percent) +
                                               self.blue_percent * (2 - self.one_state_blue_percent))
        return int(notes_amount)
