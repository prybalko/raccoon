from raccoon import TASK_QUEUES


def submit_new_task(type=None, params=None, email=None, **kwagrs):
    TASK_QUEUES[type].put(params)
    return "added", 201