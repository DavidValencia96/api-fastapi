from pydantic import BaseModel, EmailStr # Permite crear los modelos
from pydantic import Field
from fastapi import APIRouter, Header, Body
from fastapi import status
from fastapi.responses import JSONResponse
from cryptography.fernet import Fernet

from functions_jwt import validate_token, write_token
from config.db import conn
from models.userModel import users
from schemas.userSchemas import User

auth_routes = APIRouter()

key = Fernet.generate_key() # generamos una contraseña aleatoria
f = Fernet(key) # tenemos la funcion f

class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)


# Path Operations

## Login
@auth_routes.post(
    path = "/login",
    summary = "Login con Token JWT",
    tags = ["Login/sign-up Data Base"]
)
def login(user: UserLogin):
    """
    Login JTW
    
    EndPoint para solicitar al sistema un login JWT el cual el mismo le va a retornar un TOKEN y este va a ser requerido para
    todas las funcionalidades de la API, en caso de no enviar el TOKEN o enviar uno incorrecto, el sistema le retornara un mensaje de error.

    Parameters:
    - Request BODY (raw -> (JSON)):
        - "email" : email del usuario
        - "password" : contraseña del usuario
    
    - Return:
        - token jwt
    """
    result = conn.execute(users.select().where(users.c.email == user.email and users.c.password == user.password)).first()
    # print(result)
    if (user.email == result.email and user.password == result.password):
        return write_token(user.dict())
    else:
        return JSONResponse(
            content={
                "message": "No existe el usuario"
            },
            status_code = status.HTTP_404_NOT_FOUND
        )

### verificador de token
@auth_routes.post(
    path = "/login/verify_token",
    status_code = status.HTTP_200_OK,
    summary = "Verificar Token JWT",
    tags = ["Login/sign-up Data Base"]
)
def verify_token(Authorization: str = Header(None)):
    """
    Verificar token JTW
    
    EndPoint para validar el token JWT que retorno la API al momento de hacer el login.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    
    - Return:
        - "email"
        - "password"
        - "exp"
        
    """
    token = Authorization.split(" ")[1]
    print(token)
    # return "Success TOKEN JWT"
    return validate_token(token, output=True)


## Crear Usuario
@auth_routes.post( 
    path = "/register",
    response_model = User, # Respondemos con una lista de los usuarios -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Registrar usuario en DB",
    tags = ["Login/sign-up Data Base"]
)
def create_user(user: User = Body(...)):
    """
    Registro de usuario
    
    EndPoint para registrar usuarios.

    Parameters:
    - Request BODY (raw -> (JSON)):
        - "name" : nombre del usuario - (String(50))
        - "country" : pais del usuario - (String(30))
        - "phone" : telefono o celular del usuario - (String(10))
        - "user_create" : fecha en la que se crea el usuario - (String(20))
        - "email" : email del usuario - (String(50))
        - "password" : contraseña usuario - (String(50))
        - "tipo_user" : tipo usuario - (Integer)
    
    - Return:
        - "id"
        - "name"
        - "country"
        - "phone"
        - "user_create"
        - "email"
        - "password"
        - "tipo_user"
        
    """
    #diccionaro que contiene los datos solciitados
    new_user = { 
        "name": user.name, 
        "country": user.country, 
        "phone": user.phone, 
        "email": user.email, 
        "user_create": user.user_create,
        "tipo_user": user.user_create
    } 
    new_user["password"] = f.encrypt(user.password.encode("utf-8")) # encriptamos la contraseña y en utf-8
    result = conn.execute(users.insert().values(new_user)) # ejecutamos la inserción de datoa
    # el sistema consulta en la tabla users, y consultara con la validación del where el ultimo resultado insertado where tabla - c=columna .id
    # y solo devolvera el primer elemento
    
    return conn.execute(users.select().where(users.c.id == result.lastrowid)).first() # first solo cuando es un select

## PENDIENTE
@auth_routes.post(
    path = "/user/reset_pass",
    status_code = status.HTTP_200_OK,
    summary = "Recuperar contraseña del usuario DB",
    tags = ["Login/sign-up Data Base"]
)
def reset_pass():
    pass









#--------------------------------Login jwt simple test----------------------------------------------------#
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


# @auth_routes.post("/login")
# def login(user: UserLogin):
#     print(user)
#     if user.email == "user@example.com":
#         return write_token(user.dict())
#     else:
#         return JSONResponse(
#             content={
#                 "message": "No existe el usuario"
#             },
#             status_code = status.HTTP_404_NOT_FOUND
#         )

# @auth_routes.post("/verify/token")
# def verify_token(Authorization: str = Header(None)):
#     print(Authorization)
#     token = Authorization.split(" ")[1]
#     return validate_token(token, output=True)


