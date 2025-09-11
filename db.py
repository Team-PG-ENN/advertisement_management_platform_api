from pymongo import MongoClient
import os
from dotenv import load_dotenv 

load_dotenv()

#connect to mongo atlas cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

#assess database

adverts_collection_db = mongo_client["adverts_collection_db"]

#pick collection to operate on 
adverts_collection = adverts_collection_db["advert"]