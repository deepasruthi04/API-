from pydantic import BaseModel , Field

class Register(BaseModel):
    username: str
    password: str
    email: str

class Login(BaseModel):
    username: str
    password: str    

class Mark(BaseModel):
    student: str 
    subject: str 
    score: int 

class MarkResponse(Mark):
    id: str 

class EmailRequest(BaseModel):
    email: str

class OTPVerify(BaseModel):
    email: str
    otp: int    
  