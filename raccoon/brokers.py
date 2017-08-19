import multiprocessing as mp
import smtplib
import time
from email.mime.text import MIMEText


class Broker(object):
    __slots__ = ('task_queues', 'result_queue', 'tasks', 'mail_config')

    def __init__(self, task_queues, result_queue, tasks, mail_config):
        self.task_queues = task_queues
        self.result_queue = result_queue
        self.tasks = tasks
        self.mail_config = mail_config

    def __call__(self):
        self.run()

    def run(self):
        print "Broker is running..."
        while True:
            self._maybe_start_new_worker()
            self._proceed_result_if_any()
            time.sleep(0.01)

    def _maybe_start_new_worker(self):
        for task_name, task_queue in self.task_queues.items():
            if not task_queue.empty():
                task = self.tasks[task_name]
                task_data = task_queue.get()
                mp.Process(target=task._run, kwargs=task_data).start()

    def _proceed_result_if_any(self):
        if not self.result_queue.empty():
            response = self.result_queue.get()
            self._send_email_with_response(**response)
            mp.active_children()

    def _send_email_with_response(self, result, email):
        if not email:
            print "No email provided. The result is '{}'".format(result)
            return
        print 'Sending mail to {} with the result "{}"'.format(email, result)

        server, me, password = self.mail_config['server'], self.mail_config['username'], self.mail_config['password']
        msg = MIMEText(result)
        msg['Subject'] = 'Your task has finished'
        msg['From'] = me
        msg['To'] = email

        s = smtplib.SMTP_SSL(server)
        s.ehlo()
        s.login(me, password)
        s.sendmail(me, email, msg.as_string())
        s.quit()
