import getopt
import sys
from collections import defaultdict
from importlib import import_module
from itertools import chain
from multiprocessing import Queue, Process

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

# ToDo: take the module_name form command line args
module_name = 'client'
import_module(module_name)

tasks_instances = map(lambda x: x.get_instances(), [task, BaseTask])
TASKS = {task.name: task for task in chain(*tasks_instances)}
TASK_QUEUES = {task_name: Queue() for task_name in TASKS.keys()}

print "Found {} tasks: {}".format(len(TASKS), TASKS.keys())

possible_cl_options = ['{}='.format(task_name) for task_name in chain(TASKS, ['total'])]
opts, _ = getopt.getopt(sys.argv[1:], '', possible_cl_options)

JOBS_LIMIT = defaultdict(lambda: float('Inf'))

for task_name, limit in opts:
    JOBS_LIMIT[task_name[2:]] = int(limit)

import views

mail_config = dict(username=MAIL_USERNAME, password=MAIL_PASSWORD, server=MAIL_SERVER)
broker = Broker(task_queues=TASK_QUEUES, result_queue=RESULTS_QUEUE, tasks=TASKS, mail_config=mail_config,
                session=db.session, jobs_limit=JOBS_LIMIT)
Process(target=broker).start()
