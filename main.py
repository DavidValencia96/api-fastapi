# Python native
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field 

# FastAPI
from fastapi import FastAPI

app = FastAPI()

# Models

# Contiene la info basica cuando el usuario se va a registrar
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class Userlogin(UserBase): # Hereda de la clase userBase para tener la info completa, para aprovechar el user y email
    password: str = Field(
        ..., 
        min_length = 8,
        max_length = 64,
    )

class User(UserBase):
   
    first_name: str = Field(
        ..., 
        min_length = 1,
        max_length = 50,
        example = "juan"
    )
    last_name: str = Field(
        ..., 
        min_length = 1,
        max_length = 50,
        example = "valencia"
    )
    birth_date: Optional[date] = Field(default=None)

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        max_length = 255,
        min_length = 1,
    )
    create_at: datetime = Field(default = datetime.now())
    update_at: Optional[datetime] = Field(default = None)
    By: User = Field(...)



@app.get(path = "/")
def home():
    return {"Twitter API": "Working"}