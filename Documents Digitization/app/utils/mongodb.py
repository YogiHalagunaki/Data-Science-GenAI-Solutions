from pymongo import MongoClient
from urllib import parse

from utils.config import logger

class MongoDB:
    def __init__(self, db_name, mdb_conn_str):
        logger.info("Starting MongoDB Connection...")

        try:
            self.client = MongoClient(mdb_conn_str)
            self.db = self.client[db_name]
        except Exception as e:
            logger.error(f"Exception: Failed to connect to MongoDB!, {e}")
            return None

    def create_collection(self, collection_name):
        try:
            return self.db[collection_name]
        except Exception as e:
            logger.error(f"Exception: create_collection, {e}")
            return None
    
    def insert_row(self, collection_name, data):
        try:
            collection = self.create_collection(collection_name)
            return collection.insert_one(data)
        except Exception as e:
            logger.error(f"Exception: insert_row, {e}")
            return False

    def insert_rows(self, collection_name, data):
        try:
            collection = self.create_collection(collection_name)
            return collection.insert_many(data)
        except Exception as e:
            logger.error(f"Exception: insert_rows, {e}")
            return False

    def get_document(self, collection_name, query={}, projection={}):
        try:
            collection = self.create_collection(collection_name)
            return collection.find_one(query, projection)
        except Exception as e:
            logger.error(f"Exception: get_document, {e}")
            return None

    def get_documents(self, collection_name, query={}, projection={}):
        try:
            collection = self.create_collection(collection_name)
            return list(collection.find(query, projection))
            # return list(collection.find(query))
        except Exception as e:
            logger.error(f"Exception: get_documents, {e}")
            return None
        
    def update_document(self, collection_name, query, new_values):
        try:
            collection = self.create_collection(collection_name)
            return collection.update_one(query, {"$set":new_values}, upsert=True)
        except Exception as e:
            logger.error(f"Exception: update_document, {e}")
            return False

    def update_documents(self, collection_name, query, new_values):
        try:
            collection = self.create_collection(collection_name)
            return collection.update_many(query, {"$set":new_values}, upsert=True)
        except Exception as e:
            logger.error(f"Exception: update_documents, {e}")
            return False
    
    def delete_document(self, collection_name, query):
        try:
            collection = self.create_collection(collection_name)
            return collection.delete_one(query)
        except Exception as e:
            logger.error(f"Exception: delete_document, {e}")
            return False

    def count_documents(self, collection_name):
        try:
            collection = self.create_collection(collection_name)
            return collection.count_documents({})
        except Exception as e:
            logger.error(f"Exception: count_documents, {e}")
            return None
        
    def is_alive(self):
        try:
            logger.info("Checking if MongoDB connection is alive")
            # info = self.client.server_info() # Forces a call.
            # logger.info(f"MongoClient INFO: {info}")
            ping = self.client.admin.command('ping')
            logger.info(f"Ping: {ping}")
            return True
        except Exception as e:
            logger.error(f"MongoDB not alive: {e}")
            return False
        
    def close_connection(self):
        try:
            logger.info(f"Closing MongoDB Connections...")
            self.client.close()
            return True
        except Exception as e:
            logger.error(f"Error while closing MongoDB Connection: {e}")
            return False
