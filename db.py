from pymongo import MongoClient
import os
from dotenv import load_dotenv 

load_dotenv()

#connect to mongo atlas cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

#assess database

advertisement_management_platform_api = mongo_client["advertisement_management_platform_api"]

# Pick a collection to operate on
adverts_collection = advertisement_management_platform_api["adverts"]

users_collection = advertisement_management_platform_api["users"]