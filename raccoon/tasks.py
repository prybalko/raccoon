from collections import defaultdict

from raccoon import RESULTS_QUEUE


class AbstractTask(object):

    @classmethod
    def get_instances(cls):
        raise NotImplementedError

    def _run(self, *args, **kwargs):
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

    def _run(self, *args, **kwargs):
        self.wrapper(*args, **kwargs)

    @classmethod
    def get_instances(cls):
        for instance in cls.__refs__[cls]:
            yield instance


class BaseTask(AbstractTask):
    __slots__ = ('results_queue',)

    def __init__(self, *args, **kwargs):
        self.results_queue = RESULTS_QUEUE

    @classmethod
    def get_instances(cls):
        for subclass in cls.__subclasses__():
            yield subclass()

    def _run(self, *args, **kwargs):
        result = self.run(*args, **kwargs)
        self.results_queue.put(result)
