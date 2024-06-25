from pymongo import MongoClient, UpdateOne
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DATABASE_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def get_list(self, limit, offset, sort_field, order):
        # Map friendly sort fields to actual MongoDB fields
        sort_fields_map = {
            "timestamp": "timestamp",
            "overall_reactions": "overall_reactions",
            "author": "author"  # Ensure 'author' is a valid field in your documents
        }

        # Resolve the actual sort field
        sort_field = sort_fields_map.get(sort_field, "timestamp")

        # Find documents where the 'processed_text' field does not exist
        query = {"processed_text": {"$exists": True}}

        # Retrieve documents with pagination and sorting
        return list(self.collection.find(query)
                    .sort(sort_field, order)
                    .skip(offset)
                    .limit(limit))

    def get_by_id(self, id):
        return self.collection.find_one({"_id": id})
