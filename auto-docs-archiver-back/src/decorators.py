import functools
import logging

logging.basicConfig(level=logging.DEBUG)


def log(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        logging.debug(f"{f.__name__} invoked")
        return f(*args, **kwargs)

    return wrapped
