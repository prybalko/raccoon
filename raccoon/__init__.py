from importlib import import_module
from multiprocessing import Queue, Process

from flask import Flask

TASK_QUEUE_LIST = [Queue() for _ in range(3)]
RESULT_QUEUE = Queue()

from raccoon.brokers import Broker
from raccoon.decorators import task



app = Flask(__name__)

app.config.from_object('config')

import views

module_name = 'client'
import_module(module_name)

# broker = Broker(task_queue_list=TASK_QUEUE_LIST, result_queue=RESULT_QUEUE)
# broker_p = Process(target=broker, args=(TASK_QUEUE_LIST, RESULT_QUEUE)).start()


TASKS = {task.name: task for task in task.get_instances()}
print TASKS
TASKS['make_report'].run("jajaja!")
