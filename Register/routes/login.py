from fastapi import APIRouter, HTTPException, Response
import hashlib

from database.db import db
from auth.auth import create_jwt_token
from models.model import Login

router = APIRouter(prefix="/user", tags=["User Login"])

users_collection = db["users"]

def hash_password(password: str) -> str:
    """Hash the password with SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/login")
def login_user(data: Login, res: Response):
    username = data.username
    password = data.password

    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    hashed_pass = hash_password(password)
    if user["password"] != hashed_pass:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_jwt_token({"username": username})

    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,      
        samesite="lax",     
        max_age=60 
    )

    users_collection.update_one(
        {"username": username},
        {"$set": {"is_verified": True}}
    )
    return {"message": "Login successful", "token": token}
