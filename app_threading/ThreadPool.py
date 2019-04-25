from collections import deque
from threading import Event

from app_threading.TaskThread import TaskThread


class ThreadPool:
    def __init__(self, logger):
        self.__global_events = dict()
        self.__global_data = dict()
        self.__threads = dict()
        self.__logger = logger
        self.__queue = deque()
        self.__names_counter = dict()

    def get_events(self):
        return self.__global_events

    def get_datas(self):
        return self.__global_data

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

    def setup(self, threads_max=10, queue_max=10, allow_duplicate_names_process=False):
        self.__threads_max = threads_max
        self.__queue_max = queue_max
        self.__allow_duplicate_names_process = allow_duplicate_names_process

    def add_thread(self, thread):
        if thread.name in self.__threads.keys():
            if thread.name not in self.__names_counter.keys():
                self.__names_counter[thread.name] = 1

            if self.__names_counter[thread.name] > 0:
                if not self.__allow_duplicate_names_process:
                    raise NameError("Thread already exists")
                self.__names_counter[thread.name] += 1
                thread.name = "{}_{}".format(thread.name, self.__names_counter[thread.name])

        if len(self.__threads) > self.__threads_max:
            self.__logger.log_warn("Reached max number of threads. Try to add thread {} to queue...".format(thread.name))
            if len(self.__queue) > self.__queue_max:
                self.__logger.log_warn("Reached max number of threads in queue. Thread {} cannot be attached to thread pool.".format(thread.name))
                return False
            else:
                self.__queue.append(thread)
                self.__logger.log_info("Added thread {} to queue".format(thread.name))
        else:
            if len(self.__queue) > 0:
                queue_thread = self.__queue.popleft()
                self.__threads[queue_thread.name] = queue_thread
                self.__logger.log_info("Thread {} has been moved from queue.".format(queue_thread.name))

                self.__queue.append(thread)
                self.__logger.log_info("Added thread {} to queue".format(thread.name))
            else:
                self.__threads[thread.name] = thread
                self.__logger.log_info("Thread {} attached to thread pool.".format(thread.name))
            return True

    def start_thread(self, obj):
        if obj.__class__ is TaskThread:
            if obj in self.__threads.values():
                if not obj.isAlive():
                    obj.start()
                    return True
            return False

        elif obj in self.__threads.keys():
            if not self.__threads[obj].isAlive():
                self.__threads[obj].start()
                return True
        return False

    def stop_thread(self, obj):
        if obj.__class__ is TaskThread:
            if obj in self.__threads.values():
                if obj.isAlive():
                    obj.stop()
                    return True
            return False
        elif obj in self.__threads.keys():
            if self.__threads[obj].isAlive():
                self.__threads[obj].stop()
                return True
        return False

    def join_thread(self, obj):
        if obj.__class__ is TaskThread:
            if obj in self.__threads.values():
                if obj.isAlive():
                    obj.join()
                    return True
            return False
        elif obj in self.__threads.keys():
            if not self.__threads[obj].isAlive():
                self.__threads[obj].join()
                return True
        return False

    def get_threads(self):
        return self.__threads
