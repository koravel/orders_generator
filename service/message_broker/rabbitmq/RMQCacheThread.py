from thread.TaskThread import TaskThread


class RMQCacheThread(TaskThread):
    def __init__(self, queue, name, thread_pool, logger):
        super().__init__(name, thread_pool, logger)
        self.__queue = queue
