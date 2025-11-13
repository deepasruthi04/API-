from fastapi import FastAPI
from auth import create_access
from routes import students

app = FastAPI()

app.include_router(students.router)

@app.post("/login/")
def login(username: str, password: str):
    if username == "Deepasruthi" and password == "1234567890":
        token = create_access(username)
        return {"access_token": token}
    return {"error": "Invalid username or password"}
