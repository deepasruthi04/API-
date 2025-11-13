from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt

# JWT = JSON Web Token
# Structure: header.payload.signature
# header -> type:JWT, algorithm (RSA/HS256)
# payload -> user data
# signature -> encoded info

# Config
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 1  
SECRET_KEY = "MYSECRETKEY"

app = FastAPI()

username = "deepasruthi"
password = "12345"  


def create_token(uname: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    payload = {"username": uname, "expire": expire.isoformat()}  
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        return payload["username"]
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")  

@app.post("/login")
def login(uname: str, passwd: str):
    if uname == username and passwd == password:
        token = create_token(uname)
        return {"access_token": token}
    raise HTTPException(status_code=400, detail="Invalid credentials")  

@app.get("/secure_data")
def sec_data(token: str):
    uname = verify_token(token)
    return {"message": f"Hello {uname}, this is a secured endpoint"}
