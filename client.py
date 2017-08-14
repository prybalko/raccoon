from raccoon import task


@task(name='make_report')
def make_report(num):
    print "CALLING make_report function with arg {}".format(num)
