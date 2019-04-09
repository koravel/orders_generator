import threading
import traceback
from datetime import datetime


class TaskThread(threading.Thread):
    def __init__(self, name, thread_pool, logger):
        super().__init__(name=name)
        self.__thread_pool = thread_pool
        self.__logger = logger
        self.task_done = False

    def setup(self, task, data=None, events=None):
        """
        :param task: Task signature: void task(Dictionary<String, Event> events, Dictionary<String, object> data,
                                                                                                 Logger logger)
        :param data: task data Dictionary
        :param events: task events Dictionary
        :return:
        """
        self.__data = data
        self.__events = events
        self._task = task

    def run(self):
        self.start_time = datetime.now().timestamp()
        self.__logger.log_info("Run thread {}".format(self.name))

        events = self.__events
        if events is not None:
            events.update(self.__thread_pool.__global_events)

        data = self.__data
        if data is not None:
            data.update(self.__thread_pool.__global_data)

        self._task(events=events, data=data, logger=self.__logger)

        self.__logger.log_info("Close thread {} after {} sec".format(self.name, datetime.now().timestamp() - self.start_time))

    def set_event(self, name):
        if self.__events[name] is not None:
            try:
                self.__events[name].set()
            except:
                self.__logger.log_info(traceback.format_exc())
                return False
            return True
        return False

    def unset_event(self, name):
        if self.__events[name] is not None:
            try:
                self.__events[name].clear()
            except:
                self.__logger.log_info(traceback.format_exc())
                return False
            return True
        return False

    def on_start(self):
        pass

    def on_stop(self):
        pass
