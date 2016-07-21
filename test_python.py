
from pymongo import MongoClient
CLIENT = MongoClient("mongodb://localhost:27017/")
DB = CLIENT['dota']

collection = DB.key.find_one()['steam']
print(collection)