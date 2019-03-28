from collections import deque


class ThreadPool:
    def __init__(self, logger):
        self.__global_events = dict()
        self.__global_data = dict()
        self.__threads = dict()
        self.__logger = logger
        self.__queue = deque()

    def setup(self, threads_max):
        self.__threads_max = threads_max

    def add_thead(self, thread):
        if len(self.__threads) > self.__threads_max:
            self.__logger.log_warn("Reached max number of thread.")
            self.__queue.append(thread)
            self.__logger.log_info("Added thread {} to queue".format(thread.name))
        else:
            if len(self.__queue) > 0:
                self.__threads[thread.name] = self.__queue.popleft()
                self.__queue.append(thread)
            else:
                self.__threads[thread.name] = thread

    def start_thread(self, name):
        for thread in self.__threads:
            if thread.name == name and not thread.isAlive():
                thread.start()

    def stop_thread(self, name):
        for thread in self.__threads:
            if thread.name == name and thread.isAlive():
                thread.stop()

    def join_thread(self, name):
        for thread in self.__threads:
            if thread.name == name and thread.isAlive():
                thread.join()
