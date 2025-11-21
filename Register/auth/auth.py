from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from fastapi import Cookie, HTTPException

SECRET_KEY = "Bairav@2020"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def verify_token(request: Request):
     token = request.cookies.get("access_token")
     if not token:
         raise HTTPException(status_code=401, detail="Token missing")

     try:
         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
         username = payload.get("username")
         if not username:
             raise HTTPException(status_code=401, detail="Invalid token payload")
         return username
     except JWTError:
         raise HTTPException(status_code=401, detail="Invalid or expired token")

