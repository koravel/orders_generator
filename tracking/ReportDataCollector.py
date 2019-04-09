from datetime import datetime

from tracking import ReportDataKeys
from tracking.DataCollector import DataCollector


class ReportDataCollector(DataCollector):
    def __setup_zone_params(self, key):
        self.data[key] = {
            ReportDataKeys.amount: 0,
            ReportDataKeys.avg: datetime.now() - datetime.now(),
            ReportDataKeys.min: datetime.now() - datetime.now(),
            ReportDataKeys.max: datetime.now() - datetime.now(),
            ReportDataKeys.sum: datetime.now() - datetime.now()
        }

    def setup(self):
        self.data = dict()

        self.__setup_zone_params(ReportDataKeys.red)
        self.__setup_zone_params(ReportDataKeys.green)
        self.__setup_zone_params(ReportDataKeys.blue)

        self.data[ReportDataKeys.rabbit_consumed] = 0

        self.data[ReportDataKeys.mysql_new] = 0
        self.data[ReportDataKeys.mysql_to_provider] = 0
        self.data[ReportDataKeys.mysql_rejected] = 0
        self.data[ReportDataKeys.mysql_partial_filled] = 0
        self.data[ReportDataKeys.mysql_filled] = 0

    def get_data(self, key, second_key=None):
        try:
            if second_key is None:
                return self.data[key]
            return self.data[key][second_key]
        except:
            return None

    def set_data(self, key, object):
        self.data[key] = object

    def update_zone_data(self, timer, key):
        self.data[key][ReportDataKeys.amount] += 1

        single_gen_time = datetime.now() - timer

        self.data[key][ReportDataKeys.sum] += single_gen_time

        if self.data[key][ReportDataKeys.min] > single_gen_time:
            self.data[key][ReportDataKeys.min] = single_gen_time
        elif self.data[key][ReportDataKeys.max] < single_gen_time:
            self.data[key][ReportDataKeys.max] = single_gen_time

        self.data[key][ReportDataKeys.avg] = self.data[key][ReportDataKeys.sum] / self.data[key][ReportDataKeys.amount]
