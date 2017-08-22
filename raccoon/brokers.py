import multiprocessing as mp
import smtplib
import time
from collections import defaultdict
from datetime import datetime
from email.mime.text import MIMEText
from itertools import chain

from raccoon.models import Job


class Broker(object):
    __slots__ = ('task_queues', 'result_queue', 'tasks', 'mail_config', 'session', 'jobs_limit', '_jobs')

    def __init__(self, task_queues, result_queue, tasks, mail_config, session, jobs_limit):
        self.task_queues = task_queues
        self.result_queue = result_queue
        self.tasks = tasks
        self.mail_config = mail_config
        self.session = session
        self.jobs_limit = jobs_limit
        self._jobs = defaultdict(list)

    def __call__(self):
        self.run()

    def run(self):
        print "Broker is running..."
        while True:
            # ToDo: Maybe run it in threads.
            self._cleanup_finished_jobs()
            self._maybe_start_new_job()
            self._process_results_if_any()
            time.sleep(0.01)

    def _maybe_start_new_job(self):
        total_running = len(list(chain(*self._jobs.values())))
        if total_running >= self.jobs_limit['total']:
            return

        for task_name, task_queue in self.task_queues.items():
            if not task_queue.empty():
                if len(self._jobs[task_name]) < self.jobs_limit[task_name] and total_running < self.jobs_limit['total']:
                    task = self.tasks[task_name]
                    task_data = task_queue.get()
                    process = mp.Process(target=task._run, kwargs=task_data)
                    process.start()
                    self._jobs[task_name].append(process)
                    self._set_job_status(task_data['job_id'], 'in progress')

    def _process_results_if_any(self):
        if not self.result_queue.empty():
            response = self.result_queue.get()
            self._send_email_with_response(**response)

    def _cleanup_finished_jobs(self):
        for task_name, jobs in self._jobs.iteritems():
            for job in list(jobs):
                if not job.is_alive():
                    status = 'success' if job.exitcode == 0 else 'fail'
                    self._set_job_status(job._kwargs['job_id'], status)
                    job.join()
                    jobs.remove(job)

    def _set_job_status(self, job_id, status):
        job = Job.query.get(job_id)
        job.status = status
        if status in ['success', 'fail']:
            job.end_date = datetime.now()
        elif status == 'in progress':
            job.start_date = datetime.now()
        self.session.commit()

    def _send_email_with_response(self, result, email, **kwargs):
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
