import json

from flask import render_template, request

from raccoon import app
from raccoon.lib import submit_new_job
from raccoon.models import Job


@app.route("/")
def home():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)


@app.route("/api/tasks/", methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        response = submit_new_job(request.data)
        return json.dumps(response)
    print Job.query.all()
    return "list"
