from bson import ObjectId
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

    def find_by_column(self, collection, field, value, single=False, exclude=None):
        if exclude is None:
            exclude = []
        current_collection = self.database[collection]
        query = {field: value}
        excluded_fields = {}
        for field in exclude:
            excluded_fields[field] = 0

        if single:
            return current_collection.find_one(query)
        else:
            if exclude:
                return current_collection.find(query, {'fields': exclude})
            else:
                return current_collection.find(query)

    def save(self, collection, json_data):
        current_collection = self.database[collection]
        return current_collection.insert_one(json_data).inserted_id

    def delete(self, collection, field, value):
        current_collection = self.database[collection]
        query = {field: value}
        return current_collection.delete_one(query)

    def update(self, collection, field, value, update_field, update_value):
        current_collection = self.database[collection]
        current_collection.update({field: value}, {'$set': {update_field: update_value}})
