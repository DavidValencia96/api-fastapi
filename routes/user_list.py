from fastapi import APIRouter
from pydantic import BaseModel
from requests import get
# from middlewares.verify_toke_routes import VerifyTokenRoute

# userToken = APIRouter(route_class=VerifyTokenRoute)
userToken = APIRouter() 

class UserJTW(BaseModel):
    email: str
    password: str
    
    
    country: str
    page: str


# @userToken.post("/usersjtw/user")
# def user_ist_token(github: UserJTW):
#     return get(f'https://api.github.com/search/users?q=location:"{github.country}"&page={github.page}').json()

# @userToken.post("/usersjtw/userdb")
# def user_ist_token(userdb: UserJTW):
#     return get(f'https://api.github.com/search/users?q=location:"{userdb.email}"&page={github.page}').json()
#     # return get(f'http://127.0.0.1:8000/user').json()