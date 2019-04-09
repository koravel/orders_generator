from serializer.proto.OrderRecord_pb2 import OrderRecord


class OrderRecordToProto:
    @staticmethod
    def convert(record):
        proto = OrderRecord()

        proto.id = int(record.get_id())
        proto.order_id = int(record.order.get_id())
        proto.timestamp = int(record.get_timestamp())
        proto.status = record.get_status()
        proto.currency_pair = record.order.get_currency_pair()
        proto.direction = record.order.get_direction()
        proto.init_price = float(record.order.get_init_price())
        proto.init_volume = float(record.order.get_init_volume())
        proto.fill_price = float(record.get_fill_price())
        proto.fill_volume = float(record.get_fill_volume())
        proto.description = record.order.get_description()
        proto.tags = record.order.get_tags()
        proto.zone = record.get_zone()

        return proto
