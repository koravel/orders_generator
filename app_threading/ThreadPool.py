from collections import deque
from threading import Event


class ThreadPool:
    def __init__(self, logger):
        self.__global_events = dict()
        self.__global_data = dict()
        self.__threads = dict()
        self.__logger = logger
        self.__queue = deque()

    def is_event_set(self, name):
        try:
            return self.__global_events[name].is_set()
        except:
            pass

    def get_data(self, name):
        try:
            return self.__global_data[name]
        except:
            return None

    def set_event(self, name):
        try:
            self.__global_events[name].set()
        except:
            self.__global_events[name] = Event()

    def unset_event(self, name):
        try:
            self.__global_events[name].unset()
        except:
            pass

    def add_data(self, name, data):
        try:
            self.__global_data[name] = data
        except:
            pass

    def update_data(self, name, data):
        try:
            self.__global_data[name] = data
        except:
            pass

    def delete_data(self, name):
        try:
            self.__global_data[name] = None
        except:
            pass

    def setup(self, threads_max):
        self.__threads_max = threads_max

    def add_thead(self, thread):
        if len(self.__threads) > self.__threads_max:
            self.__logger.log_warn("Reached max number of threads.")
            self.__queue.append(thread)
            self.__logger.log_info("Added thread {} to queue".format(thread.name))
        else:
            if len(self.__queue) > 0:
                self.__threads[thread.name] = self.__queue.popleft()
                self.__queue.append(thread)
            else:
                self.__threads[thread.name] = thread

    def start_thread(self, name):
        if self.__threads[name] is not None:
            if not self.__threads[name].isAlive():
                self.__threads[name].start()

    def stop_thread(self, name):
        if self.__threads[name] is not None:
            if not self.__threads[name].isAlive():
                self.__threads[name].stop()

    def join_thread(self, name):
        if self.__threads[name] is not None:
            if not self.__threads[name].isAlive():
                self.__threads[name].join()
