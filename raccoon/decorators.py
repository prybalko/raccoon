from collections import defaultdict

from raccoon import RESULT_QUEUE


class KeepRefs(object):
    __refs__ = defaultdict(list)

    def __init__(self):
        self.__refs__[self.__class__].append(self)

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            yield inst_ref


class task(KeepRefs):

    def __init__(self, *args, **kwargs):
        super(task, self).__init__()
        self.name = kwargs.get('name')

    def __call__(self, fn):
        def call_fn(*args, **kwargs):
            print "BEFORE!"
            result = fn(*args, **kwargs)
            RESULT_QUEUE.put(result)
            print "AFTER!"
    
        self.run = call_fn
        # return call_fn
