#
#
# def get_mongo_client():
#     return MongoClient(MONGO_URI)
#
#
# def get_collection(client, db_name, collection_name):
#     db = client[db_name]
#     return db[collection_name]
#
# def upsert_message(collection, message):
#     """Upserts a message document into the specified collection."""
#     collection.update_one({'_id': message['_id']}, {'$set': message}, upsert=True)

from pymongo import MongoClient, UpdateOne
from config.config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def get_urls(self):
        query = {"processed_text": {"$exists": True}}
        # query = {"_id": 4034}

        return list(self.collection.find(query, {"_id": 1, "pasta_url": 1}))

    def update_processed_text(self, _id, processed_text):
        # Update the document with the new processed text
        self.collection.update_one(
            {"_id": _id},
            {"$set": {"processed_text": processed_text}}
        )

    def bulk_update_processed_texts(self, updates):
        # Perform a bulk update of documents
        if updates:
            operations = [
                UpdateOne({"_id": _id}, {"$set": {"processed_text": processed_text}})
                for _id, processed_text in updates
            ]
            self.collection.bulk_write(operations)
