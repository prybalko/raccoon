from collections import defaultdict

from raccoon import RESULTS_QUEUE


class AbstractTask(object):
    """
    An abstract class for any client tasks. It defines the methods, which `Broker` relies on.
    """

    @classmethod
    def get_instances(cls):
        """Returns a *list* of task instances. Must be reimplemented"""
        raise NotImplementedError

    def _run(self, *args, **kwargs):
        """This method is called by `Broker` in order to execute the task. Must be reimplemented"""
        raise NotImplementedError


class task(AbstractTask):
    """
    A decorator to define a task. Example:

    @task(name='make_report', json_schema={...})
    def make_report(params):
        pass

    """
    __slots__ = ('name', 'wrapper', 'results_queue', 'json_schema')
    __refs__ = defaultdict(list)

    def __init__(self, *args, **kwargs):
        self.__refs__[self.__class__].append(self)
        self.name = kwargs.get('name')
        self.json_schema = kwargs.get('json_schema')
        self.results_queue = RESULTS_QUEUE

    def __call__(self, fn):
        def call_fn(params, email, job_id):
            result = fn(**params)
            self.results_queue.put({'result': result, 'email': email, 'job_id': job_id})
        self.wrapper = call_fn

    def _run(self, *args, **kwargs):
        self.wrapper(*args, **kwargs)

    @classmethod
    def get_instances(cls):
        for instance in cls.__refs__[cls]:
            yield instance


class BaseTask(AbstractTask):
    """
    A superclass to define a task. Example:

    class MakeReport(BaseTask):
        name = 'make_report'
        json_schema = {...}

        def run(self, params):
            pass

    """
    __slots__ = ('results_queue',)

    def __init__(self, *args, **kwargs):
        self.results_queue = RESULTS_QUEUE

    @classmethod
    def get_instances(cls):
        for subclass in cls.__subclasses__():
            yield subclass()

    def _run(self, params, email, job_id):
        result = self.run(**params)
        self.results_queue.put({'result': result, 'email': email, 'job_id': job_id})

    def run(self, **kwargs):
        raise NotImplementedError
