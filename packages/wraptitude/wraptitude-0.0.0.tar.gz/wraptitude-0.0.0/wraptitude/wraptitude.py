class Wrapper:
    def __init__(self, fn, *args, **kwargs):
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def __call__(self, fn):
        def wrapper(*args, **kwargs):
            return self._fn(fn(*args, **kwargs), *self._args, **self._kwargs)
        return wrapper
