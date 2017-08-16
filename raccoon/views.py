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
        try:
            data = json.loads(request.data)
        except ValueError:
            abort(400)
        response = submit_new_task(**data)
        return response
    return "list"
