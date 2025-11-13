from fastapi import FastAPI 
from pydantic import BaseModel,Field
from typing import Optional

emp = [
    {'id': 101 , 'name' : 'sruthi' , 'place' : 'Chennai'},
    {'id': 102 , 'name' : 'deepa' , 'place' : 't nagar'},
    {'id': 103 , 'name' : 'deepasruthi' , 'place' : 'thiruvanmiyur'}

]
class items(BaseModel):
    name : str = Field(min_length = 3 , max_length = 100, pattern = "^[a-zA-Z]")
    price :float = Field(gt=0 , lt=10000)
    availability : Optional[bool] = None

app = FastAPI()

## Basic ##
@app.get("/home")
def home():
    return ("Heloo worldd")

##Query parameter##
@app.get("/display")
def viewforquery(id:int):
    for e in emp:
        if e['id'] == id:
            return e
        
##path parameter ##
@app.get("/display/{id}")
def viewforpath(id:int):
    for e in emp:
        if e['id'] == id:
            return e


##for checking how basemodel works [ all the values must be filled if you want some 
# columns to be optional mention that in class you are extending from ] ##
@app.post("/display")        
def view(data : items):
    return{"message": "got the data" , "data": data}  



      

            


