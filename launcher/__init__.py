import time
import traceback
from datetime import datetime

import config.PathProvider as provider
import config
import root
import util
import service.file as sf
import generator
import generator.constant as consts
import thread


def setup():
    provider.load(root.__file__)
    try:
        util.logger.setup(sf.append, provider.pathes["LOG"].location)

        config.load()

        consts.load()

    except:
        util.logger.log_level = 1
        util.logger.log_fatal(traceback.format_exc())
    else:
        util.logger.log_level = config.settings["log_level"]

        util.delete_excess_files(provider.pathes["LOG"].location, config.settings["logger_files_max"])
        util.delete_excess_files(provider.pathes["GEN_OUT"].location, config.settings["out_files_max"])


def close():
    util.logger.log_info("Closing app...")
    config.save()
    provider.save()
    util.logger.log_info("App closed")


def single_thread_run():
    global out_path

    start_time = datetime.now()
    generator.setup()

    orders_sequence = generator.get_orders_sequence()
    notes_sequence = generator.get_notes_sequence(orders_sequence)

    thread.setup()

    while thread.portion_iters_amount - thread.portion_iter > 0:
        thread.generate(notes_sequence, single_thread=True)
        thread.to_file(single_thread=True)
        thread.to_mysql()
        thread.to_rabbitmq_queue()

    finish_time = datetime.now() - start_time
    util.logger.log_debug("Single-thread generation ended after {} sec".format(finish_time))


def run():
    start_time = datetime.now()

    generator.setup()

    orders_sequence = generator.get_orders_sequence()
    notes_sequence = generator.get_notes_sequence(orders_sequence)

    thread.setup()
    generating_thread = thread.GenerationThread(0, "gen", notes_sequence)
    to_file_thread = thread.ToFileThread(1, "to_file")

    generating_thread.start()
    to_file_thread.start()

    while generating_thread.is_alive() or to_file_thread.is_alive():
        time.sleep(0.01)

    generating_thread.join()
    to_file_thread.join()

    finish_time = datetime.now() - start_time
    util.logger.log_debug("Multi-thread generation ended after {} sec".format(finish_time))


if __name__ == "__main__":
    setup()
    single_thread_run()
    #run()
    close()
