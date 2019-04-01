import traceback


def print_log(text):
    print("{}\n{}".format(traceback.format_exc(), text))