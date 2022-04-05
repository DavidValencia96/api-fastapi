# Python native
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field 


# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

# Models

# Contiene la info basica cuando el usuario se va a registrar
class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class Userlogin(UserBase): # Heredada de la clase userBase para tener la info completa, para aprovechar el user y email
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

class UserRegister(User):
    password: str = Field(
        ..., 
        min_length = 8,
        max_length = 64,
    )

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

## User

### Signup user
@app.post(
    path = "/signup",
    response_model = User, # Respondemos con la información de un usuario -- heredada de la class User
    status_code = status.HTTP_201_CREATED,
    summary = "Register a User",
    tags = ["User"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup User
    
    This path operation register a user in the app.

    Parameters:
        - Request body parameter.
            - user: UserRegister.
    
    Return a Json with basic user information:
        - user_id: UUID.
        - email: Emailstr.
        - first_name: str.
        - last_name: str.
        - brith_date: datetime.
    """
    
    with open("users.json", "r+", encoding = "utf-8") as f:
        results = json.loads(f.read()) # almacenamos los datos y los convertimos a JSON
        user_dict = user.dict() # Transformamos el JSON En diccionario que contiene la info del usuario
        user_dict["user_id"] = str(user_dict["user_id"]) # Convertimos el datos UUID a STRING
        user_dict["birth_date"] = str(user_dict["birth_date"]) # Convertimos el datos datetime a STRING
        results.append(user_dict)
        f.seek(0) # nos aseguramos que tener todo como se tiene en la lista del JSON "[]"
        f.write(json.dumps(results)) # seguir escribiendo en la mismos listado del JSON "[]" y evitar que se genere otra "[][]"
        return user
    
### Login user
@app.post(
    path = "/login",
    response_model = User, # Respondemos con la información de un usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Login User Success",
    tags = ["User"]
)
def login():
    pass

### Show all Users
@app.get(
    path = "/users",
    response_model = List[User], # Respondemos con una lista de los usuarios -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Show All User",
    tags = ["User"]
)
def show_all_users():
    pass

### Show User id
@app.get(
    path = "/users/{user_id}",
    response_model = User, # Traemos la data del usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Show a User",
    tags = ["User"]
)
def show_a_users():
    pass

### Delete a User
@app.delete(
    path = "/users/{user_id}/delete",
    response_model = User, # Traemos la data del usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Delete a User",
    tags = ["User"]
)
def delete_a_users():
    pass

### Update a User
@app.put(
    path = "/users/{user_id}/update",
    response_model = User, # Traemos la data del usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Update a User",
    tags = ["User"]
)
def update_a_users():
    pass


## Tweet

### Show al Tweets
@app.get(
    path = "/",
    response_model = List[Tweet], # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Show all Tweets",
    tags = ["Tweets"]
)
def home():
    return {"Twitter API": "Working"}

## User

### Post a Tweet
@app.post(
    path = "/post",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_201_CREATED,
    summary = "Post a Tweet",
    tags = ["Tweets"]
)
def post():
    pass

### Show a Tweet
@app.get(
    path = "/tweets/{tweet_id}",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Show a Tweet",
    tags = ["Tweets"]
)
def show_a_tweet():
    pass

### Show a Tweet
@app.delete(
    path = "/tweets/{tweet_id}/delete",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Delete a Tweet",
    tags = ["Tweets"]
)
def delete_a_tweet():
    pass


### Show a Tweet
@app.put(
    path = "/tweets/{tweet_id}/update",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Update a Tweet",
    tags = ["Tweets"]
)
def update_a_tweet():
    pass