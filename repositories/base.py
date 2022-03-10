from repositories.database import mongo_db
from bson import ObjectId


class Base_repository:

    def convert_object_id_to_string(func):
        def wrapper(self):
            #result_func = func(self)
            #result_list = list(result_func)
            # result_converted = [
            #    {**x, "_id": str(x["_id"])} for x in result_list]
            # return result_converted
            return [{**x, "_id": str(x["_id"])} for x in list(func(self))]
        return wrapper

    def __init__(self, table_name):
        self.table_name = table_name
        self.collection = mongo_db.database[table_name]

    @convert_object_id_to_string
    def get_all(self):
        return self.collection.find()

    def get_by_id(self, id):
        return self.collection.find_one({"_id": ObjectId(id)})

    def get_one(self, query):
        return self.collection.find_one(query)

    def create_one(self, document):
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def update_one_by_id(self, id, update):
        return self.update_one({"_id": ObjectId(id)}, update)

    def update_one(self, query, update):
        return self.collection.update_one(query, update)

    def delete_one(self, query):
        return self.collection.delete_one(query)

    def delete_one_by_id(self, id):
        return self.delete_one({"_id": ObjectId(id)})
