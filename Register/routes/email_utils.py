import random
import smtplib
from email.mime.text import MIMEText
from fastapi import APIRouter, HTTPException
from database.db import db
from models.model import EmailRequest
from datetime import datetime, timedelta

router = APIRouter(prefix="/user", tags=["OTP Login"])

users_collection = db["users"]
otp_collection = db["otp"]

SENDER_EMAIL = "deepasruthi04@gmail.com"
APP_PASSWORD = "gowotaxvwwtoxowe"


def send_email(to_email, otp):
    msg = MIMEText(f"Your OTP is: {otp}")
    msg["Subject"] = "Your Login OTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())


@router.post("/send-otp")
def send_otp(data: EmailRequest):
    email = data.email

    user = users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")

    otp = random.randint(100000, 999999)
    expire_time = datetime.utcnow() + timedelta(minutes=5)

    otp_collection.update_one(
        {"email": email},
        {"$set": {"otp": otp, "expires_at": expire_time}},
        upsert=True
    )

    send_email(email, otp)

    return {"message": "OTP sent successfully"}
