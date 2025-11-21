from fastapi import FastAPI
from routes import register, login, marks, email_utils, verify

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(marks.router)
app.include_router(email_utils.router)
app.include_router(verify.router)
