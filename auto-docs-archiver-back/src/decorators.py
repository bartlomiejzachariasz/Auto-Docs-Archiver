import functools
import logging


def log(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        logging.info(f"{f.__name__} invoked")
        return f(*args, **kwargs)

    return wrapped
