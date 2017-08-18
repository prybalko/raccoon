from raccoon import task, BaseTask
import time


@task(name='make_report')
def make_report(num):
    time.sleep(2)
    return "CALLING make_report function with arg {}".format(num)


class MakeReport(BaseTask):
    name = 'make_class_report'

    def run(self, num):
        time.sleep(3)
        return "Calling MakeReport class run method with arg {}".format(num)
