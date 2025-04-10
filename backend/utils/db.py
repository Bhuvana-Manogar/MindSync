
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mindsync_db"]
collection = db["scraped_content"]

def save_to_mongo(data):
    collection.insert_one({"data": data})
