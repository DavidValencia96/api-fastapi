# Python
from datetime import datetime
from datetime import date

# Typing
from typing import Optional, List

# Starlette
from starlette import status

# FastAPI
from fastapi import APIRouter, Response
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body
from fastapi import Form
from fastapi import Path

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


key = Fernet.generate_key() # generamos una contraseña aleatoria
f = Fernet(key) # tenemos la funcion f


user = APIRouter()

# Path Operations

## Lista Usuarios
@user.get(
    path = "/user", 
    response_model = List[User],
    status_code = status.HTTP_200_OK,
    summary = "Listar usuarios de DB",
    tags = ["User Data Base"]
)
def list_user():
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
    # print(id)
    return conn.execute(users.select().where(users.c.id == id)).first()
    
@user.delete(
    path ="/user/delete/{id}", 
    status_code = status.HTTP_200_OK,
    # status_code = status.HTTP_200_OK,
    summary = "Borrar usuario DB",
    tags = ["User Data Base"]
)
def delete_user(id: str):
    result = conn.execute(users.delete().where(users.c.id == id)) 
    # return "Delete user success"
    return Response(status_code = status.HTTP_200_OK)
    # return HTTPException(
    #             status_code = status.HTTP_204_NO_CONTENT,
    #             detail = f"¡Usuario no encontrado!" 
    # )

@user.put(
    path = "/user/edit/{id}", 
    response_model = User,
    summary = "Actualizar usuario DB",
    tags = ["User Data Base"]
)
def update_user(id: str, user: User):
    result = conn.execute(users.update().values(
        name = user.name, 
        email= user.email, 
        password = f.encrypt(user.password.encode("utf-8"))
    ).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()


## PENDIENTE
@user.post(
    path = "/user/reset_pass",
    status_code = status.HTTP_200_OK,
    summary = "Resetear contraseña del usuario DB",
    tags = ["User Data Base"]
)
def reset_pass():
    pass