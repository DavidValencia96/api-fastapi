# Python native
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field 
from fastapi import status

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
    By: User = Field(...) # heredo los datos del usuario que estan en la clase User

# Path Operations

@app.get(path = "/")
def home():
    return {"Twitter API": "Working"}

## User

### Signup
@app.post(
    path = "/signup",
    response_model = User, # Respondemos con la información de un usuario -- hereda de la class User
    status_code = status.HTTP_201_CREATED,
    summary = "Register a User",
    tags = ["User"]
)
def signup():
    pass

### Login
@app.post(
    path = "/login",
    response_model = User, # Respondemos con la información de un usuario -- hereda de la class User
    status_code = status.HTTP_200_OK,
    summary = "Login User Success",
    tags = ["User"]
)
def login():
    pass

### Users
@app.get(
    path = "/users",
    response_model = List[User], # Respondemos con una lista de los usuarios -- hereda de la class User
    status_code = status.HTTP_200_OK,
    summary = "Show All User",
    tags = ["User"]
)
def show_all_users():
    pass

### User id
@app.get(
    path = "/users/{user_id}",
    response_model = User, # Traemos la data del usuario -- hereda de la class User
    status_code = status.HTTP_200_OK,
    summary = "Show a User",
    tags = ["User"]
)
def show_a_users():
    pass

### Delete User
@app.delete(
    path = "/users/{user_id}/delete",
    response_model = User, # Traemos la data del usuario -- hereda de la class User
    status_code = status.HTTP_200_OK,
    summary = "Delete a User",
    tags = ["User"]
)
def delete_a_users():
    pass

### update User
@app.put(
    path = "/users/{user_id}/update",
    response_model = User, # Traemos la data del usuario -- hereda de la class User
    status_code = status.HTTP_200_OK,
    summary = "Update a User",
    tags = ["User"]
)
def update_a_users():
    pass




## Tweet
