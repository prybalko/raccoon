import multiprocessing as mp
import time


class Broker(object):
    __slots__ = ('task_queues', 'result_queue', 'tasks')

    def __init__(self, task_queue_list, result_queue, tasks):
        self.task_queues = task_queue_list
        self.result_queue = result_queue
        self.tasks = tasks

    def __call__(self, *args, **kwargs):
        self.run()

    def run(self):
        print "RUNNING..."
        while True:
            self._maybe_start_new_worker()
            self._proceed_result_if_any()
            time.sleep(0.01)

    def _maybe_start_new_worker(self):
        for task_name, task_queue in self.task_queues.items():
            if not task_queue.empty():
                task = self.tasks[task_name]
                kwargs = task_queue.get()
                mp.Process(target=task._run, kwargs=kwargs).start()

    def _proceed_result_if_any(self):
        if not self.result_queue.empty():
            msg = self.result_queue.get()
            print msg
            mp.active_children()
