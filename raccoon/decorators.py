

class task(object):

    def call(*argv, **kwargs):
        def call_fn(fn):
            return fn(*argv, **kwargs)
        return call_fn
