import json

from jsonschema import validate, ValidationError

from raccoon import TASK_QUEUES, TASKS, db
from raccoon.models import Job

REQUEST_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "request",
    "description": "a request to add new task",
    "type": "object",
    "properties": {
            "type": {
                "description": "The task name (type) to be launched",
                "type": "string"
            },
            "params": {
                "description": "Parameters to run the task with",
                "type": "object"
            },
            "email": {
                "description": "Email to send result to",
                "type": "string"
            }
        },
    "required": ["type", "params"]
}


def validate_request_data(raw_data):
    try:
        data = json.loads(raw_data)
    except ValueError as e:
        raise ValueError("Payload must be a valid JSON")

    try:
        validate(data, REQUEST_SCHEMA)
    except ValidationError as e:
        raise ValueError(e.message)

    task_name, params = data['type'], data['params']
    if task_name not in TASKS:
        raise ValueError("Task name {} not found. Available options are {}".format(task_name, TASKS.keys()))

    task = TASKS[task_name]
    try:
        validate(params, task.json_schema)
    except ValidationError as e:
        raise ValueError(e.message)
    return data


def submit_new_job(raw_data):
    response = {"status": "OK"}
    try:
        data = validate_request_data(raw_data)
    except ValueError as e:
        return {"status": "ERROR", "error_code": 100, "error_msg": e.message}
    task_name, params, email = data['type'], data['params'], data.get('email')

    job = Job(task_name=task_name, params=json.dumps(params), email=email)
    db.session.add(job)
    db.session.commit()

    TASK_QUEUES[task_name].put({'params': params, 'email': email, 'job_id': job.id})
    return response
