from pymongo import MongoClient
from datetime import datetime
from app.libs.config import Config
from app.libs.logger import Logging

def create(doc: dict):

    # Connect to MongoDB 
    client = MongoClient(Config.DB_CON_STR)

    # set database and collection
    db = client[Config.DB_NAME]   
    collection = db["git_action_logs"]          

    # Insert the document
    result = collection.insert_one(doc)

    Logging.debug(result.inserted_id)
    Logging.debug(doc)


def latest():

     # Connect to MongoDB
    client = MongoClient(Config.DB_CON_STR)

    # set database and collection
    db = client[Config.DB_NAME]    
    collection = db["git_action_logs"]  
   
    # Fetch last 10 inserted documents
    last_10_docs = collection.find().sort("_id", -1).limit(10)

    # Print them
    for doc in last_10_docs:
        print(doc)

