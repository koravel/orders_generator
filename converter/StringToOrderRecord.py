from entity.Order import Order
from entity.OrderRecord import OrderRecord


class StringToOrderRecord:
    @staticmethod
    def convert(string, position=0):
        fields = string.split(',')

        order = Order(
            id=fields[0],
            currency_pair=fields[1],
            direction=fields[2],
            description=fields[3],
            init_price=fields[4],
            init_volume=fields[5],
            tags=fields[6],
            position=position,
            initial_timestamp=None
        )

        order_record = OrderRecord(
            order=order,
            id=fields[11],
            status=fields[9],
            timestamp=fields[10],
            fill_price=fields[7],
            fill_volume=fields[8]
        )

        if order.get_initial_timestamp() is None or order.get_initial_timestamp() > fields[10]:
            order.set_initial_timestamp(fields[10])

        return order_record
