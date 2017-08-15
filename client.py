from raccoon import task
import time


@task(name='make_report')
def make_report(num):
    time.sleep(3)
    return "CALLING make_report function with arg {}".format(num)
