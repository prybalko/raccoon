from collections import defaultdict

from raccoon import RESULTS_QUEUE


class AbstractTask(object):

    @classmethod
    def get_instances(cls):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class task(AbstractTask):
    __slots__ = ('name', 'wrapper', 'results_queue')
    __refs__ = defaultdict(list)

    def __init__(self, *args, **kwargs):
        self.__refs__[self.__class__].append(self)
        self.name = kwargs.get('name')
        self.results_queue = RESULTS_QUEUE

    def __call__(self, fn):
        def call_fn(*args, **kwargs):
            result = fn(*args, **kwargs)
            self.results_queue.put(result)
        self.wrapper = call_fn

    def run(self, *args, **kwargs):
        self.wrapper(*args, **kwargs)

    @classmethod
    def get_instances(cls):
        return cls.__refs__[cls]


class BaseTask(AbstractTask):

    @classmethod
    def get_instances(cls):
        return cls.__subclasses__()
