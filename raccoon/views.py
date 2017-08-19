import json

from flask import render_template, request
from werkzeug.exceptions import abort

from raccoon import app
from raccoon.lib import submit_new_task


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/api/tasks/", methods=['GET', 'POST'])
def tasks():
    if request.method == 'POST':
        response = submit_new_task(request.data)
        return json.dumps(response)
    return "list"
