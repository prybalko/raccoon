import multiprocessing as mp
import time
import random


def worker(msg, result_queue):
    time.sleep(random.randint(0, 100) / 50.)
    result_queue.put(msg)


class Broker(object):

    def __init__(self, task_queue_list, result_queue):
        self.task_queue_list = task_queue_list
        self.result_queue = result_queue

    def __call__(self, *args, **kwargs):
        self.run()

    def maybe_start_new_worker(self):
        for task_queue in self.task_queue_list:
            if not task_queue.empty():
                msg = task_queue.get()
                worker_p = mp.Process(target=worker, args=(msg, self.result_queue,))
                worker_p.start()

    def proceed_result_if_any(self):
        if not self.result_queue.empty():
            msg = self.result_queue.get()
            print msg
            mp.active_children()

    def run(self):
        print "RUNNING..."
        while True:
            self.maybe_start_new_worker()
            self.proceed_result_if_any()
            time.sleep(0.01)
