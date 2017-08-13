from multiprocessing import Process, Queue

from flask import Flask

from raccoon.brokers import Broker

TASK_QUEUE_LIST = [Queue() for _ in range(3)]
RESULT_QUEUE = Queue()

app = Flask(__name__)

app.config.from_object('config')

import views

broker = Broker(task_queue_list=TASK_QUEUE_LIST, result_queue=RESULT_QUEUE)
broker_p = Process(target=broker, args=(TASK_QUEUE_LIST, RESULT_QUEUE)).start()
