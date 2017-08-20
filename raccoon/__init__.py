from importlib import import_module
from itertools import chain
from multiprocessing import Queue, Process
from flask_sqlalchemy import SQLAlchemy

from flask import Flask

from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER

RESULTS_QUEUE = Queue()

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

import models
db.drop_all()
db.create_all()

from raccoon.brokers import Broker
from raccoon.tasks import task, BaseTask

module_name = 'client'
import_module(module_name)

tasks_instances = map(lambda x: x.get_instances(), [task, BaseTask])
TASKS = {task.name: task for task in chain(*tasks_instances)}
TASK_QUEUES = {task_name: Queue() for task_name in TASKS.keys()}

print "Found {} tasks: {}".format(len(TASKS), TASKS.keys())

import views

mail_config = dict(username=MAIL_USERNAME, password=MAIL_PASSWORD, server=MAIL_SERVER)
broker = Broker(task_queues=TASK_QUEUES, result_queue=RESULTS_QUEUE, tasks=TASKS, mail_config=mail_config,
                session=db.session)
Process(target=broker).start()
