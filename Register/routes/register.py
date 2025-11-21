from fastapi import APIRouter, HTTPException
from database.db import db
from models.model import Register
import hashlib

router = APIRouter(prefix="/user", tags=["User"])
users_collection = db["users"]

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/register")
def register_user(data: Register):

    username = data.username
    email = data.email
    password = data.password

    if users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    if users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pass = hash_password(password)

    user_doc = {
        "username": username,
        "email": email,
        "password": hashed_pass
    }

    result = users_collection.insert_one(user_doc)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }
