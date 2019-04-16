from tracking import ReportDataKeys


class Reporter:
    def __init__(self, data):
        self.__data = data

    def get_report(self):
        generation_text = self.get_generation_text()
        rabbit_consuming_text = self.get_rabbit_consuming_text()
        mysql_saving_text = self.get_mysql_saving_text()

        return self._get_report(generation_text, rabbit_consuming_text, mysql_saving_text)

    def _get_report(self, generation_text, rabbit_consuming_text, mysql_saving_text):
        return "===============================REPORT===============================" \
               "\n{}\n--------------------------------------------------------------------"\
               "\n{}\n--------------------------------------------------------------------" \
               "\n{}\n=============================REPORT_END=============================".format(
                generation_text, rabbit_consuming_text, mysql_saving_text)

    def get_generation_text(self):
        return self._get_generation_text(
            red_zone_text=self.__get_time_text(
                "red zone",
                self.__data[ReportDataKeys.red][ReportDataKeys.amount],
                self.__data[ReportDataKeys.red][ReportDataKeys.avg],
                self.__data[ReportDataKeys.red][ReportDataKeys.min],
                self.__data[ReportDataKeys.red][ReportDataKeys.max],
                self.__data[ReportDataKeys.red][ReportDataKeys.sum]
        ),
           green_zone_text=self.__get_time_text(
               "green zone",
               self.__data[ReportDataKeys.green][ReportDataKeys.amount],
               self.__data[ReportDataKeys.green][ReportDataKeys.avg],
               self.__data[ReportDataKeys.green][ReportDataKeys.min],
               self.__data[ReportDataKeys.green][ReportDataKeys.max],
               self.__data[ReportDataKeys.green][ReportDataKeys.sum]
           ),
           blue_zone_text=self.__get_time_text(
               "blue zone",
               self.__data[ReportDataKeys.blue][ReportDataKeys.amount],
               self.__data[ReportDataKeys.blue][ReportDataKeys.avg],
               self.__data[ReportDataKeys.blue][ReportDataKeys.min],
               self.__data[ReportDataKeys.blue][ReportDataKeys.max],
               self.__data[ReportDataKeys.blue][ReportDataKeys.sum]
           ),
            total_amount=self.__data[ReportDataKeys.red][ReportDataKeys.amount] +
                         self.__data[ReportDataKeys.green][ReportDataKeys.amount] +
                         self.__data[ReportDataKeys.blue][ReportDataKeys.amount]
        )

    def _get_generation_text(self, red_zone_text, green_zone_text, blue_zone_text, total_amount):
        return "Generation:" \
                "\n{}\n{}\n{}"\
                "\nTotal amount: {}".format(
                    red_zone_text, green_zone_text, blue_zone_text, total_amount)

    def get_rabbit_consuming_text(self):
        return self._get_rabbit_consuming_text(consumed=self.__data[ReportDataKeys.rabbit_consumed])

    def _get_rabbit_consuming_text(self, consumed):
        return "RabbitMQ Consumer:\nconsumed: {}".format(consumed)

    def get_mysql_saving_text(self):
        sum = self.__data[ReportDataKeys.mysql_red] + \
              self.__data[ReportDataKeys.mysql_green] + \
              self.__data[ReportDataKeys.mysql_blue]

        return self._get_mysql_saving_text(
            red=self.__data[ReportDataKeys.mysql_red],
            green=self.__data[ReportDataKeys.mysql_green],
            blue=self.__data[ReportDataKeys.mysql_blue],
            total_saved=sum
        )

    def _get_mysql_saving_text(self, red, green, blue, total_saved):
        return "MySQL saving:\nRed: {}\nGreen: {}\nBlue: {}\nTotal saved: {}\n".\
            format(red, green, blue, total_saved)

    def __get_time_text(self, title, amount, avg, min, max, total):
        return "-{}: {}\navg: {} ms\nmin: {} ms\nmax: {} ms\nTotal: {} ms\n".format(title, amount, avg, min, max, total)
