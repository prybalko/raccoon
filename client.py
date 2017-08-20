from raccoon import task, BaseTask
import time

task_schema = {
    "type": "object",
    "properties": {
        "num": {"type": "number"},
    },
    "required": ["num"],
    "additionalProperties": False
}


@task(name='make_report', json_schema=task_schema)
def make_report(num):
    time.sleep(num)
    return "CALLING make_report function with arg {}".format(num)


class MakeReport(BaseTask):
    name = 'make_class_report'
    json_schema = task_schema

    def run(self, num):
        time.sleep(num)
        return "Calling MakeReport class run method with arg {}".format(num)
