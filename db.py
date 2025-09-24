from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Access database
advertisement_management_platform_api = mongo_client["advertisement_management_platform_api"]

# Pick a collection to operate on
adverts_collection = advertisement_management_platform_api["adverts"]

vendors_collection = advertisement_management_platform_api["vendors"]