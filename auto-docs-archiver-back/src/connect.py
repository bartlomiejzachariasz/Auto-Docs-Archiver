from pymongo import MongoClient


class Connector:

    def __init__(self, host, port):
        self.uri = self.convert_to_uri(host=host, port=port)
        self.connector = None
        self.database = None

    def connect(self, database):
        self.connector = MongoClient(self.uri)
        self.database = self.connector[database]

    def convert_to_uri(self, host, port):
        return f"mongodb://{host}:{port}"

    def find_by_column(self, collection, field, value):
        current_collection = self.database[collection]
        query = {field: value}
        return current_collection.find_one(query)

    def save(self, collection, json_data):
        current_collection = self.database[collection]
        current_collection.insert_one(json_data)
