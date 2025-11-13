from fastapi import FastAPI, HTTPException, Cookie, Response
import uuid
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()

username = "Deepasruthi"
password = "1234567890"
sessions = {}
SESSION_DURATION = 30 


@app.post("/login")
def login(uname: str, passwd: str, res: Response):
    if username == uname and password == passwd:
        sid = str(uuid.uuid4())
        curr_time = datetime.now()
        exp_time = curr_time + timedelta(seconds=SESSION_DURATION)

        print("Current time:", curr_time)
        print("Expiry time:", exp_time)

        sessions[sid] = {
            "username": uname,
            "expires_at": exp_time
        }

        res.set_cookie(key="sid", value=sid, httponly=True)
        return {"message": "LOGIN SUCCESSFUL"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/home")
def home(sid: Optional[str] = Cookie(None)):
    if sid is None or sid not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session_data = sessions[sid]
    if datetime.now() > session_data["expires_at"]:
        del sessions[sid]
        raise HTTPException(status_code=401, detail="Session expired")

    return {"user": session_data["username"], "expires_at": session_data["expires_at"]}
