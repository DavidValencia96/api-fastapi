# Python
from datetime import datetime, date
import json

# Typing
from typing import Optional, List

# Starlette
from starlette import status

# FastAPI
from fastapi import FastAPI, APIRouter, Response, status, HTTPException
from fastapi import Body, Header, Form, Path
from fastapi.responses import JSONResponse

# Pydantic
from pydantic import BaseModel # Permite crear los modelos
from pydantic import EmailStr # Valida emails
from pydantic import Field # Validar los atributos de un modelo

# Cryptography
from cryptography.fernet import Fernet

# Archivos proyecto
from config.db import conn
from models.userModel import users
from schemas.userSchemas import User
# from schemas.userSchemas import UserLogin
from functions_jwt import validate_token, write_token
# from middlewares.verify_toke_routes import VerifyTokenRoute


key = Fernet.generate_key() # generamos una contraseña aleatoria
f = Fernet(key) # tenemos la funcion f


# user = APIRouter(route_class=VerifyTokenRoute)
user = APIRouter()



# class UserLogin(BaseModel):
#     email: EmailStr = Field(...)
#     password: str = Field(...)


# Path Operations

## Login
# @user.post(
#     path = "/login",
#     summary = "Solicitar Token Login",
#     tags = ["Login Data Base"]
# )
# def login(user: UserLogin):
#     result = conn.execute(users.select().where(users.c.email == user.email and users.c.password == user.password)).first()
#     print(result)
#     if (user.email == result.email and user.password == result.password):
#         return write_token(user.dict())
#     else:
#         return JSONResponse(
#             content={
#                 "message": "No existe el usuario"
#             },
#             status_code = status.HTTP_404_NOT_FOUND
#         )

# ### verificador de token
# @user.post(
#     path = "/login/verify_token",
#     status_code = status.HTTP_200_OK,
#     summary = "Verificar Token Login",
#     tags = ["Login Data Base"]
# )
# def verify_token(Authorization: str = Header(None)):
#     print(Authorization)
#     token = Authorization.split(" ")[1]
#     return validate_token(token, output=True)


## Lista Usuarios
@user.get(
    path = "/user", 
    response_model = List[User],
    status_code = status.HTTP_200_OK,
    summary = "Listar usuarios de DB",
    tags = ["User Data Base"]
)
def list_user():
    """
    Listar usuarios
    
    EndPoint podra listar todos los usuarios registrados.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}
    
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
    result = conn.execute(users.select()).fetchall() # Retorna todo los datos de consulta a la db 
    if result:
        return result
    else:
        raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"¡No se encontro información de usuarios!" 
            )


## Crear Usuario
@user.post( 
    path = "/user/create",
    response_model = User, # Respondemos con una lista de los usuarios -- heredada de la class User
    status_code = status.HTTP_200_OK,
    summary = "Crear usuario en DB",
    tags = ["User Data Base"]
)
def create_user(user: User = Body(...)):
    """
    Registro de usuario
    
    EndPoint para registrar usuarios y requerira tener un login con token jwt para continuar con  la creación.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}
        
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


@user.get(
    path = "/user/detail/{id}", 
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Detalle del usuario DB",
    tags = ["User Data Base"]
    
)
def user_detail(id: str):
    """
    Detalle de usuario
    
    EndPoint para ver el detalle de un usuario.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}
    
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
    # print(id)
    return conn.execute(users.select().where(users.c.id == id)).first()


@user.delete(
    path ="/user/delete/{id}", 
    status_code = status.HTTP_200_OK,
    summary = "Borrar usuario DB",
    tags = ["User Data Base"]
)
def delete_user(id: str):
    """
    Eliminar un usuario
    
    EndPoint podra eliminar un usuario que ya se encuentre registrado.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}
    
    - Return:
        - status code: 200 OK
        
    """
    result = conn.execute(users.delete().where(users.c.id == id)) 
    # return "Delete user success"
    return HTTPException(
                status_code = status.HTTP_204_NO_CONTENT,
                detail = f"¡Usuario no encontrado!" 
    )


@user.put(
    path = "/user/edit/{id}", 
    response_model = User,
    status_code = status.HTTP_200_OK,
    summary = "Actualizar usuario DB",
    tags = ["User Data Base"]
)
def update_user(id: str, user: User):
    """
    Editar un usuario
    
    EndPoint podra editar un usuario.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}
        
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
    result = conn.execute(users.update().values(
        name = user.name, 
        country = user.country, 
        phone= user.phone, 
        password = f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()


