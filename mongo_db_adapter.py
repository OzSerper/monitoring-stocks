from mongo_connection import MongoConnection
from conf_loader import mongo_conf


mongo = MongoConnection(mongo_conf)
mongo.connect()