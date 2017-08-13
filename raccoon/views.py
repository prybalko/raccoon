from flask import render_template

from raccoon import app, TASK_QUEUE_LIST


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/task/")
def add_task():
    TASK_QUEUE_LIST[0].put("asd")
    print "added"
    return "added"
