class Reporter:
    def __init__(self, data, send_method):
        self.__data = dict()
        self.__send_method= send_method

    # it gonna be similar to send_method(report_text)
    def send(self, report_text):
        pass
