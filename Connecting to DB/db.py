from pymongo import MongoClient 

client = MongoClient("mongodb://localhost:27017/")
db = client["student"]
collection = db["student_record"]
