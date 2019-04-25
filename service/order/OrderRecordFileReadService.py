from converter.StringToOrderRecord import StringToOrderRecord
from service.file.FileReadService import FileReadService


class OrderFileReadService(FileReadService):
    @staticmethod
    def read_all(obj_location):
        result = super(OrderFileReadService, OrderFileReadService).read_all(obj_location).split('\n')

        i = 0
        order_records = []

        while i < len(result) - 1:
            order_record = StringToOrderRecord.convert(result[i])
            order_records.append(order_record)
            i += 1
        return order_records
