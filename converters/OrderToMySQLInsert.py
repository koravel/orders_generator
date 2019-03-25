class OrderToMySQLInsert:
    __query_text = "insert into order_notes values({},'{}',{},'{}','{}',{},{},{},{},'{}','{}');"

    @staticmethod
    def convert(note):
        """
        Converts note into sql insert command and returns formatted string
        """
        return OrderToMySQLInsert.__query_text.format(
            note["id"], note["status"], note["date"], note["currency_pair"], note["direction"],
            note["init_price"], note["fill_price"], note["init_volume"], note["fill_volume"],
            note["description"], note["tags"])
