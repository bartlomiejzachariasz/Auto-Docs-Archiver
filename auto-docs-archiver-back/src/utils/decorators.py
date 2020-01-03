import functools
import logging

from flask_jwt_extended import verify_jwt_in_request
from flask import abort

from src.errors.errors import UserNotFound

logging.basicConfig(level=logging.DEBUG)

# connector = Connector(DB_CONFIG["host"], DB_CONFIG["port"])
# connector.connect(DB_CONFIG["db_name"])
# authenticator = Authenticator(connector)

def log(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        logging.debug(f"{f.__name__} invoked")
        return f(*args, **kwargs)

    return wrapped


def auth_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        try:
            from src.api.app import authenticator
            authenticator.get_authenticated_user()
            return f(*args, **kwargs)
        except UserNotFound as error:
            logging.error("Authorization failed: %s", error)
            abort(403)
    return wrapper
