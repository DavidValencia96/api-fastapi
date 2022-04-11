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
from fastapi.responses import RedirectResponse


from dotenv import load_dotenv

# Routes
from routes.userRoutes import user
from routes.tweetRoutes import tweet
from routes.commentsRoutes import comment
from routes.auth import auth_routes
from routes.user_list import userToken

import os
SECRET_KEY = os.getenv('ApiJwtPROGweb')

app = FastAPI(
    title="Api Programación Web in FastApi - Python",
    # version="1.0.0" # se crea la base del proyecto
    version="1.0.1" #Se incluye documentación y conexión a base de datos heroku
)


async def redirect_docs():
    
    """ Nullo """
    
    return RedirectResponse("https://fastapi-jd.herokuapp.com/docs")


app.include_router(user, prefix="/api")
app.include_router(tweet, prefix="/api")
app.include_router(comment, prefix="/api")
app.include_router(auth_routes, prefix="/api")
app.include_router(userToken, prefix="/api")

load_dotenv()


