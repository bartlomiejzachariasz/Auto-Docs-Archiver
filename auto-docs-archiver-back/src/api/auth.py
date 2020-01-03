from flask_jwt_extended import get_jwt_identity, create_access_token

from src.utils.connect import Connector
from src.errors.errors import UserNotFound, InvalidCredentials


class Authenticator:

    def __init__(self, db_connector: Connector):
        self.db_connector = db_connector

    def get_authenticated_user(self):
        jwt_identity = get_jwt_identity()
        user = self.db_connector.find_by_column("users", "username", jwt_identity, single=True)
        if user is not None:
            return user
        else:
            raise UserNotFound()

    def authenticate_user(self, username, password):
        user = self.db_connector.find_by_column("users", "username", username, single=True)
        if user['password'] == password:
            return create_access_token(identity=username)
        else:
            raise InvalidCredentials()

