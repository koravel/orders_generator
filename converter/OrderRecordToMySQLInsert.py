class OrderRecordToMySQLInsert:
    __query_text = "insert into order_notes values({},'{}',{},'{}','{}',{},{},{},{},'{}','{}');"

    @staticmethod
    def convert(record):
        """
        Converts order record into sql insert command and returns formatted string
        """
        return OrderRecordToMySQLInsert.__query_text.format(
            record["id"], record["status"], record["date"], record["currency_pair"], record["direction"],
            record["init_price"], record["fill_price"], record["init_volume"], record["fill_volume"],
            record["description"], record["tags"])
