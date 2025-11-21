from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from database.db import db
from auth.auth import create_jwt_token
from datetime import datetime
from models.model import OTPVerify

router = APIRouter(prefix="/user", tags=["User OTP Login"])

users_collection = db["users"]
otp_collection = db["otp"]


@router.post("/verify-otp")
def verify_otp(data:OTPVerify, res: Response):
    email = data.email
    otp = data.otp

    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_data = otp_collection.find_one({"email": email})
    if not otp_data:
        raise HTTPException(status_code=400, detail="No OTP found.")
    if otp_data["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired.")

    if str(otp_data["otp"]) != str(otp):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    token_data = {"username": user["username"]} 
    token = create_jwt_token(token_data)

    res.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60
    )
    users_collection.update_one(
        {"email": email},
        {"$set": {"is_verified": True}}
    )

    otp_collection.delete_one({"email": email})

    return {
        "message": "OTP verified successfully!",
        "token": token
    }
