from collections import defaultdict

from raccoon import RESULTS_QUEUE


class BaseTask(object):

    @classmethod
    def get_instances(cls):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


class KeepRefs(object):
    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(self)

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            yield inst_ref


class task(KeepRefs, BaseTask):
    __slots__ = ('name', 'wrapper', 'results_queue')

    def __init__(self, *args, **kwargs):
        super(task, self).__init__()
        self.name = kwargs.get('name')
        self.results_queue = RESULTS_QUEUE

    def __call__(self, fn):
        def call_fn(*args, **kwargs):
            result = fn(*args, **kwargs)
            self.results_queue.put(result)
        self.wrapper = call_fn

    def run(self, *args, **kwargs):
        self.wrapper(*args, **kwargs)
