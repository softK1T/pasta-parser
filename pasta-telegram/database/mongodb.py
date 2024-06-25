from pymongo import MongoClient, UpdateOne
from config.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def bulk_update_processed_texts(self, updates):
        # Perform a bulk update of documents
        if updates:
            operations = [
                UpdateOne({'_id': update['_id']}, {"$set": update}, upsert=True)
                for update in updates
            ]
            self.collection.bulk_write(operations)
