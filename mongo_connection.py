from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,PyMongoError
from pymongo.collection import Collection
from mongo_abstract import AbstractMongoConnection
from bson.json_util import dumps



from utils import CONNECTION_STRING,DATABASE_NAME


class MongoConnection(AbstractMongoConnection):
    def __init__(self,mongo_conf):
        self.connection_url = mongo_conf[CONNECTION_STRING]
        self.database_name = mongo_conf[DATABASE_NAME]
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.connection_url)
            self.client.admin.command('ping')
            self.db = self.client[self.database_name]
            print(f"Connected to MongoDB database: {self.database_name}")
        except ConnectionFailure as e:
            print(f"Connection failed: {e}")
            raise

    def get_collection(self, collection_name: str):
        if  self.db is None:
            raise RuntimeError("Database connection not established")
        return self.db[collection_name]

    def get_by_filter(self,collection : Collection ,filters):
        return collection.find_one(filters)
    
    def get_by_filter_all(self,collection : Collection ,filters, projection=None):
        return collection.find(filters,projection)

    
    def get_by_filter_all_date_order(self,collection : Collection ,filters):
        return collection.find(filters).sort("date", 1)

    def get_by_aggregation(self,collection : Collection ,pipeline):
        result = list(collection.aggregate(pipeline))
        return result


    
    def insert_doc(self,collection : Collection ,**filters):
        try:
            collection.insert_one(filters)
            print(filters)
            print(f"done--- {filters["action"]}")
        except PyMongoError as e:
            print(f"Error found as {e}")

    
    def delete_doc(self,collection : Collection ,**filters):
            collection.delete_one(filters)

    def get_epoch(self,collection : Collection):
        try:
            return collection.find_one({"epoch":True}) 
        except Exception as e:
            return None
        
    def update_document(self,collection: Collection, filter_query: dict, update_fields: dict,upsert: bool = False,multiple: bool = False):
        update = {"$set": update_fields}
        print(filter_query)

        if multiple:
          result = collection.update_many(filter_query, update, upsert=upsert)
        else:
          result = collection.update_one(filter_query, update, upsert=upsert)
    
        

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")
