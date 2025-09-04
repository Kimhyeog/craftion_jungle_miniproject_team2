from pymongo import MongoClient

client = MongoClient('mongodb://test:test@54.180.142.84',27017)
# client = MongoClient('localhost',27017)

db = client["yournameis"]