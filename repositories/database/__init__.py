from pymongo import MongoClient
from logger import Logger
from bson.codec_options import CodecOptions
from bson.codec_options import TypeRegistry
from repositories.type_codecs.enum_codecs import Enum_codec
from auxiliaries.enumerations import Position, Order_Type, Order_Status
import os
logger = Logger("Initialize MongoDB", "purple")


class Mongo_DB_service:
    database = None

    def __init__(self, database_url, database_name, codecs):
        self.database_name = database_name
        self.client = MongoClient(database_url,
                                  uuidRepresentation='standard')
        try:
            self.client.server_info()
            logger.info("MongoDB Connected")
            if codecs:
                self.add_codecs(codecs)
            else:
                self.database = self.client[database_name]

        except Exception:
            logger.error("Could not connect to MongoDB")

    def add_codecs(self, codecs):
        type_registry = TypeRegistry(codecs)
        codec_options = CodecOptions(type_registry=type_registry)
        self.database = self.client.get_database(
            self.database_name, codec_options=codec_options)

    def create_collection(self, collection_name, validator):
        self.database.create_collection(collection_name, validator=validator)


position_codec = Enum_codec(Position)
order_type_codec = Enum_codec(Order_Type)
order_status_codec = Enum_codec(Order_Status)
mongo_db = Mongo_DB_service(
    os.getenv("MONGO_DB_URL"),
    os.getenv("MONGO_DB_NAME"),
    [position_codec, order_type_codec, order_status_codec])

# mongo_db.create_collection("backtests")
