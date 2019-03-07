import math
import time
import threading
import traceback
from datetime import datetime
from os import path

import config.PathProvider as provider
import config
import generators
import services.file as sf
import services.mysql as mysql
import services.rabbitmq as rabbit
import utils

notes = []
is_generating = threading.Event()
is_throwing = threading.Event()
notes_count = 0
portion_iter = 0
notes_amount = 0
portion_iters_amount = 0
out_path = ""


def setup():
    global notes_amount, portion_iters_amount, out_path
    notes_amount = generators.get_notes_amount()
    portion_iters_amount = math.ceil(notes_amount / config.settings["portion_amount"])
    out_path = path.join(provider.pathes["GEN_OUT"].location, utils.get_date_file_name("txt"))
    open(out_path, 'x+').close()


class GenerationThread(threading.Thread):
    def __init__(self, threadID, name, notes_sequence):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.notes_sequence = notes_sequence

    def run(self):
        while portion_iters_amount - portion_iter > 0:
            generate(self.notes_sequence)


class ToFileThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        while portion_iters_amount - portion_iter > 0:
            to_file()


def generate(notes_sequence, single_thread=False):
    global notes, is_generating, is_throwing

    is_generating.set()

    start_time = datetime.now()

    utils.logger.log_debug("Start 'generate' operation at {}".format(start_time))

    local_notes = []

    try:
        while len(local_notes) < config.settings["portion_amount"]:
            local_notes.append(notes_sequence.__next__())
    except:
        utils.logger.log_warn(traceback.format_exc())
        utils.logger.log_debug("Portion count lesser than portion amount")

    if not single_thread:
        is_throwing.wait()

    notes = local_notes

    finish_time = datetime.now() - start_time
    utils.logger.log_debug("Finish 'generate' operation after {} sec".format(finish_time))
    is_generating.clear()


def to_file(single_thread=False):
    global portion_iter, out_path, notes, is_throwing, is_generating

    start_time = datetime.now()

    utils.logger.log_debug("Start 'to_file' operation at {}".format(start_time))

    if not single_thread:
        is_generating.wait()

    is_throwing.set()

    sf.append_array(notes, out_path)

    finish_time = datetime.now() - start_time
    utils.logger.log_debug("Finish 'to_file' operation after {} sec".format(finish_time))
    portion_iter += 1
    is_throwing.clear()


def to_mysql():
    global out_path, portion_iter, portion_iters_amount
    start_time = datetime.now()
    connector = mysql.default_connect()

    mysql.execute_queries_yield(sf.read_all_yield(out_path), connector)

    mysql.close(connector)

    finish_time = datetime.now() - start_time
    utils.logger.log_debug("Finish 'to_mysql' thread after {} sec".format(finish_time))


def to_rabbitmq_queue():
    global out_path

    start_time = datetime.now()

    queries_generator = sf.read_all_yield(out_path)

    rabbit_connection = rabbit.open_connection(config.settings["rabbit"]["host"])
    rabbit.declare_queue(rabbit_connection.channel(), config.settings["rabbit"]["routing_key"])

    rabbit.send_messages(rabbit_connection,
                         config.settings["rabbit"]["exchange"],
                         config.settings["rabbit"]["routing_key"],
                         queries_generator)

    rabbit.close_connection(rabbit_connection)

    finish_time = datetime.now() - start_time
    utils.logger.log_debug("Finish 'to_rabbitmq_queue' thread after {} sec".format(finish_time))
