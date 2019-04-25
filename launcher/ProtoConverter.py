from converter.OrderRecordToProto import OrderRecordToProto


class ProtoConverter:
    @staticmethod
    def convert_batch(batch):
        protos = []
        for order_record in batch:
            protos.append(OrderRecordToProto.convert(order_record))
        return protos
