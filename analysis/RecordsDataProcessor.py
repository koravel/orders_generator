from analysis.DataProcessor import DataProcessor
from tracking import ReportDataKeys


class RecordsDataProcessor(DataProcessor):
    @staticmethod
    def get_result(data, zone):

        if zone == ReportDataKeys.red:
            data = RecordsDataProcessor.update_zone_data(data, ReportDataKeys.red)
        if zone == ReportDataKeys.green:
            data = RecordsDataProcessor.update_zone_data(data, ReportDataKeys.green)
        if zone == ReportDataKeys.blue:
            data = RecordsDataProcessor.update_zone_data(data, ReportDataKeys.blue)

        return data

    @staticmethod
    def update_zone_data(data, zone):
        data[zone][ReportDataKeys.amount] += 1

        single_gen_time = data[zone][ReportDataKeys.gen_time]

        data[zone][ReportDataKeys.sum] += single_gen_time

        if data[zone][ReportDataKeys.min] > single_gen_time:
            data[zone][ReportDataKeys.min] = single_gen_time
        if data[zone][ReportDataKeys.max] < single_gen_time:
            data[zone][ReportDataKeys.max] = single_gen_time

        data[zone][ReportDataKeys.avg] = data[zone][ReportDataKeys.sum] / data[zone][ReportDataKeys.amount]

        return data

    def __orders_sum(self):
        pass

    def __orders_sum_by_groups(self):
        pass

    def __notes_sum(self):
        pass

    def __notes_sum_by_groups(self):
        pass

    def __generation_time(self):
        pass
