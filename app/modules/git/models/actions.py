from datetime import datetime
from pymongo import MongoClient
from app.libs.config import Config
from app.libs.logger import Logging
from bson import ObjectId

def create(doc: dict) -> ObjectId:

    # Connect to MongoDB 
    client = MongoClient(Config.DB_CON_STR)

    # set database and collection
    db = client[Config.DB_NAME]   
    collection = db["git_action_logs"]          

    # Insert the document
    result = collection.insert_one(doc)

    return result.inserted_id


from datetime import datetime

def latest(limit: int) -> list:
    # Connect to MongoDB
    client = MongoClient(Config.DB_CON_STR)

    # set database and collection
    db = client[Config.DB_NAME]    
    collection = db["git_action_logs"]  
   
    # Fetch last 10 inserted documents
    last_10_docs = collection.find().sort("_id", -1).limit(limit)

    # Format documents into strings based on action
    # ################################################################
    # ## For PULL_REQUEST action:
    #   Format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
    #   Sample: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
    #
    # ## For PUSH action:
    #   Format: {author} pushed to {to_branch} on {timestamp}
    #   Sample: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
    #
    # ## For PULL_REQUEST action:
    #   Format: {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
    #   Sample: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
    # #####################################################
    formatted_logs = []
    for doc in last_10_docs:
        # Parse timestamp if it's a string
        if isinstance(doc['timestamp'], str):
            timestamp = datetime.fromisoformat(doc['timestamp'].replace('Z', '+00:00'))
        else:
            timestamp = doc['timestamp']
        
        # Format timestamp
        formatted_time = timestamp.strftime("%d %B %Y - %I:%M %p UTC")
        
        # Create formatted string based on action
        if doc['action'] == 'PULL':
            message = f"'{doc["author"]}' submitted a pull request from '{doc["from_branch"]}' to '{doc["to_branch"]}' on {formatted_time}"
        elif doc['action'] == 'PUSH':
            message = f"'{doc["author"]}' pushed to '{doc["to_branch"]}' on {formatted_time}"
        elif doc['action'] == 'MERGE':
            message = f"'{doc["author"]}' merged from '{doc["from_branch"]}' to '{doc["to_branch"]}' on {formatted_time}"
        
        formatted_logs.append(message)
    
    return formatted_logs
