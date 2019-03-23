import time
import traceback
from datetime import datetime

import config.PathProvider as provider
import config
import root
import utils
import services.file as sf
import generators
import generators.constants as consts
from launcher import threads


def setup():
    provider.load(root.__file__)
    try:
        utils.logger.setup(sf.append, provider.pathes["LOG"].location)

        config.load()

        consts.load()

    except:
        utils.logger.log_level = 1
        utils.logger.log_fatal(traceback.format_exc())
    else:
        utils.logger.log_level = config.settings["log_level"]

        utils.delete_excess_files(provider.pathes["LOG"].location, config.settings["logger_files_max"])
        utils.delete_excess_files(provider.pathes["GEN_OUT"].location, config.settings["out_files_max"])


def close():
    utils.logger.log_info("Closing app...")
    config.save()
    provider.save()
    utils.logger.log_info("App closed")


def single_thread_run():
    global out_path

    start_time = datetime.now()
    generators.setup()

    orders_sequence = generators.get_orders_sequence()
    notes_sequence = generators.get_notes_sequence(orders_sequence)

    threads.setup()

    while threads.portion_iters_amount - threads.portion_iter > 0:
        threads.generate(notes_sequence, single_thread=True)
        threads.to_file(single_thread=True)
        threads.to_mysql()
        threads.to_rabbitmq_queue()

    finish_time = datetime.now() - start_time
    utils.logger.log_debug("Single-thread generation ended after {} sec".format(finish_time))


def run():
    start_time = datetime.now()

    generators.setup()

    orders_sequence = generators.get_orders_sequence()
    notes_sequence = generators.get_notes_sequence(orders_sequence)

    threads.setup()
    generating_thread = threads.GenerationThread(0, "gen", notes_sequence)
    to_file_thread = threads.ToFileThread(1, "to_file")

    generating_thread.start()
    to_file_thread.start()

    while generating_thread.is_alive() or to_file_thread.is_alive():
        time.sleep(0.01)

    generating_thread.join()
    to_file_thread.join()

    finish_time = datetime.now() - start_time
    utils.logger.log_debug("Multi-thread generation ended after {} sec".format(finish_time))


if __name__ == "__main__":
    setup()
    single_thread_run()
    #run()
    close()
