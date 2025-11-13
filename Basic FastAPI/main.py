from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI() 

client = MongoClient("mongodb://localhost:27017/")
db = client["book_db"]
collection = db["books"]


@app.post("/add_book/")
def add_book(book: dict):
    result = collection.insert_one(book)
    return {"inserted_id": str(result.inserted_id)}

@app.get("/books/")
def get_books():
    books = list(collection.find({}, {"_id": 0}))
    return books

@app.put("/add_data")
def add_bookkss(book: dict):
    result = collection.insert_one(book)
    return {"inserted_id": str(result.inserted_id)}

@app.delete("/delete")
def delete(book :dict):
    result = collection.delete_one(book)
    return {"deleted_id" : str(result.deleted_count)}