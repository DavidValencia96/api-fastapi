# Python native
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel # Permite crear los modelos
from pydantic import EmailStr # Valida emails
from pydantic import Field # Validar los atributos de un modelo


# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body
from fastapi import Form
from fastapi import Path

# Routes
from routes.userRoutes import user

app = FastAPI(
    title="Api Programación Web in FastApi - Python",
    version="1.0.0"
)

app.include_router(user)

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

class LoginOut(BaseModel):
    email: EmailStr = Field(...),
    message: str = Field(default = "Login Successfully")

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        max_length = 255,
        min_length = 1,
    )
    create_at: datetime = Field(default = datetime.now())
    updated_at: Optional[datetime] = Field(default = None)
    by: User = Field(...) # heredo los datos del usuario que estan en la clase User

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
def login(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    """
    Login

    This path operation login a Person in the app

    Parameters:
    - Request body parameters:
        - email: EmailStr
        - password: str

    Returns a LoginOut model with username and message
    """
    
    with open("users.json", "r", encoding="utf-8") as f:
        all_users: list = json.loads(f.read())
        user_found: dict = None
        for user in all_users:
            if user["email"] == email and user["password"] == password:
                user_found = user
                return User(
                    user_id = str(user["user_id"]),
                    email = user["email"],
                    first_name=user["first_name"],
                    last_name=user["last_name"],
                    birth_date=str(user["birth_date"])
                )
        return user_found

### Show all Users
@app.get(
    path = "/users",
    response_model = List[User], # Respondemos con una lista de los usuarios -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Show All User",
    tags = ["User"]
)
def show_all_users():
    """
    Show all Users
    
    This path operation register a user in the app.

    Parameters:
    - 
    
    Return a Json list with all users in the app, with the following keys:
    - user_id: UUID.
    - email: Emailstr.
    - first_name: str.
    - last_name: str.
    - brith_date: datetime.
    """
    
    with open("users.json", "r", encoding = "utf-8") as f:
        results = json.loads(f.read())
        return results

### Show User id
@app.get(
    path = "/users/{user_id}",
    response_model = User, # Traemos la data del usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Show a User",
    tags = ["User"]
)
def show_a_users(user_id: UUID = Path(
    ...,
    title = "User ID",
    description="This is the user ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa7"
)):
    """
    Show a User

    This path operation show if a person exist in the app

    Parameters:
        - user_id: UUID

    Returns a json with user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        id = str(user_id)
        for data in results:
            if data["user_id"] == id:
                return data
            else:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = f"¡This user_id doesn't exist!"
                )

### Delete a User
@app.delete(
    path = "/users/{user_id}/delete",
    response_model = User, # Traemos la data del usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Delete a User",
    tags = ["User"]
)
def delete_a_users(user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
)):
    """
    Delete a User

    This path operation delete a user in the app

    Parameters:
        - user_id: UUID

    Returns a json with deleted user data:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(user_id)
    for data in results:
        if data["user_id"] == id:
            results.remove(data)
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )

### Update a User
@app.put(
    path = "/users/{user_id}/update",
    response_model = User, # Traemos la data del usuario -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Update a User",
    tags = ["User"]
)
def update_a_users(user_id: UUID = Path(
        ...,
        title="User ID",
        description="This is the user ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa3"
    ),
    user: UserRegister = Body(...)
):
    """
    Update User

    This path operation update a user information in the app and save in the database

    Parameters:
    - user_id: UUID
    - Request body parameter:
        - **user: User** -> A user model with user_id, email, first name, last name, birth date and password
    
    Returns a user model with user_id, email, first_name, last_name and birth_date
    """
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])
    with open("users.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
    for user in results:
        if user["user_id"] == user_id:
            results[results.index(user)] = user_dict
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This user_id doesn't exist!"
        )

## Tweet

### Show al Tweets
@app.get(
    path = "/",
    response_model = List[Tweet], # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "HOME -- Show all Tweets",
    tags = ["Tweets"]
)
def home():
    """
    Show all Tweets
    
    This path operation shows all tweets in the app

    Parameters:
    - 
    
    Return a Json with basic tweet information:
    - tweet_id: UUID 
    - content: str 
    - create_at: datetime 
    - updated_at: Optional[datetime] 
    - By: User  
    """
    
    with open("tweets.json", "r", encoding = "utf-8") as f:
        results = json.loads(f.read())
        return results
    # return {"Twitter API": "Working"}

## User

### Post a Tweet
@app.post(
    path = "/post",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_201_CREATED,
    summary = "Post a Tweet",
    tags = ["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a Tweet
    
    This path operation post a tweet in the app
    Parameters:
    - Request body parameter.
        - tweet: Tweet.
    
    Return a Json with basic tweet information:
    - tweet_id: UUID 
    - content: str 
    - create_at: datetime 
    - updated_at: Optional[datetime] 
    - by: User  
    """
    
    with open("tweets.json", "r+", encoding = "utf-8") as f:
        results = json.loads(f.read()) # almacenamos los datos y los convertimos a JSON
        tweet_dict = tweet.dict() # Transformamos el JSON En diccionario que contiene la info del usuario
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"]) # Convertimos el datos UUID a STRING
        tweet_dict["create_at"] = str(tweet_dict["create_at"]) # Convertimos el datos datetime a STRING
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        
        results.append(tweet_dict)
        f.seek(0) # nos aseguramos que tener todo como se tiene en la lista del JSON "[]"
        f.write(json.dumps(results)) # seguir escribiendo en la mismos listado del JSON "[]" y evitar que se genere otra "[][]"
        return tweet

### Show a Tweet
@app.get(
    path = "/tweets/{tweet_id}",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Show a Tweet",
    tags = ["Tweets"]
)
def show_a_tweet(tweet_id: UUID = Path(
    ...,
    title="Tweet ID",
    description="This is the tweet ID",
    example="3fa85f64-5717-4562-b3fc-2c963f66afa6"
)):
    """
    Show a Tweet

    This path operation show if a tweet exist in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"¡This tweet_id doesn't exist!"
        )

### Delete a Tweet
@app.delete(
    path = "/tweets/{tweet_id}/delete",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Delete a Tweet",
    tags = ["Tweets"]
)
def delete_a_tweet(tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa2"
)):
    """
    Delete a Tweet

    This path operation delete a tweet in the app

    Parameters:
        - tweet_id: UUID

    Returns a json with deleted tweet data:
        - tweet_id: UUID
        - content: str
        - created_at: datetime
        - updated_at: Optional[datetime]
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
        id = str(tweet_id)
    for data in results:
        if data["tweet_id"] == id:
            results.remove(data)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return data
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )


### Update a Tweet
@app.put(
    path = "/tweets/{tweet_id}/update",
    response_model = Tweet, # Respondemos con la información de los tweets -- heredada de la class Tweet
    status_code = status.HTTP_200_OK,
    summary = "Update a Tweet",
    tags = ["Tweets"]
)
def update_a_tweet(tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa8"
    ),
     content: str = Form(
        ..., 
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",
    )):
    
    """
    Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    - tweet_id: UUID
    - contet:str
    
    Returns a json with:
        - tweet_id: UUID
        - content: str 
        - created_at: datetime 
        - updated_at: datetime
        - by: user: User
    """
    
    tweet_id = str(tweet_id)
    # tweet_dict = tweet.dict()
    # tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
    # tweet_dict["birth_date"] = str(tweet_dict["birth_date"])
    with open("tweets.json", "r+", encoding="utf-8") as f: 
        results = json.loads(f.read())
    for tweet in results:
        if tweet["tweet_id"] == tweet_id:
            tweet['content'] = content
            tweet['updated_at'] = str(datetime.now())
            print(tweet)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(results))
            return tweet
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This tweet_id doesn't exist!"
        )