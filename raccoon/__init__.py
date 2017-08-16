from importlib import import_module
from itertools import chain
from multiprocessing import Queue, Process

from flask import Flask

RESULTS_QUEUE = Queue()

from raccoon.brokers import Broker
from raccoon.tasks import task, BaseTask

app = Flask(__name__)

app.config.from_object('config')

module_name = 'client'
import_module(module_name)

tasks_instances = map(lambda x: x.get_instances(), [task, BaseTask])
TASKS = {task.name: task for task in chain(*tasks_instances)}
TASK_QUEUES = {task_name: Queue() for task_name in TASKS.keys()}

print TASKS

import views

broker = Broker(task_queue_list=TASK_QUEUES, result_queue=RESULTS_QUEUE, tasks=TASKS)
Process(target=broker).start()
