from typing import Optional
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

class Info(BaseModel):
    user_id : int
    question_id : int
    bot_id : int

app = FastAPI()

@app.get("/")
def read_root(info : Info):

    status = ""
    
    if info.bot_id==1:
        status = "sent request to bot with id 1"
    elif info.bot_id==2:
        status = "sent request to bot with id 2"
    else:
        status = "sent request to bot with id 3"


    return {
        "status" : status,
        "url" : "url",
        "data" : info
    }
