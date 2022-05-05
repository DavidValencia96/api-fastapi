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

# Archivos proyecto
from config.db import conn
from models.tweetModel import tweetsModel
from schemas.tweetSchemas import TweetSchema

from middlewares.verify_toke_routes import VerifyTokenRoute

# tweet = APIRouter(route_class=VerifyTokenRoute)
tweet = APIRouter() 

# Path Operations

## Tweet's

### Mostrar todos los  Tweet's
@tweet.get(
   path = "/tweet",
   response_model = List[TweetSchema], # Respondemos con la información de los tweets -- heredada de la class Tweet
   status_code = status.HTTP_200_OK,
   summary = "Home App",
   tags = ["Tweets Data Base"]
)
async def list_tweet():
   """
    Listar Tweets publicados
    
    EndPoint para ver los tweets que ya se encuentra publicados.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    - Return:
        - "tweet_id"
        - "content"
        - "create_tw_date"
        - "update_tw_date"
        - "user_id_create"
        
    """
   result = conn.execute(tweetsModel.select()).fetchall() # Retorna todo los datos de consulta a la db 
   if result:
       return result
   else:
       raise HTTPException(
               status_code = status.HTTP_404_NOT_FOUND,
               detail = f"¡No hay Tweet's publicados aún!" 
        )


### Crear un Tweet
@tweet.post(
   path = "/tweet/create",
   response_model = TweetSchema, # Respondemos con una lista de los usuarios -- heredada de la class User
   status_code = status.HTTP_200_OK,
   summary = "Crear Tweet en DB",
   tags = ["Tweets Data Base"]
)
async def create_tweet(tweet: TweetSchema = Body(...)):
   """
    Crear Tweet
    
    EndPoint para crear un tweet.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    - Request BODY (raw -> (JSON)):
        - "content" : contenido del tweet - (String(250))
        - "create_tw_date" : fecha de creación del twwet - (String(30))
        - "update_tw_date" : actualización del tweet -(String(30))
        - "user_id_create" : usuario que lo creo - (Integer)
    
    - Return:
        - "tweet_id"
        - "content"
        - "create_tw_date"
        - "update_tw_date"
        - "user_id_create"
        
   """
   new_tweet = {
      "content": tweet.content,
      "create_tw_date": tweet.create_tw_date,
      "update_tw_date": tweet.update_tw_date,
      "user_id_create": tweet.user_id_create
   }
   result = conn.execute(tweetsModel.insert().values(new_tweet))
   return conn.execute(tweetsModel.select().where(tweetsModel.c.tweet_id == result.lastrowid)).first()

### Detalle del tweet
@tweet.get(
   path = "/tweet/detail/{tweet_id}",
   response_model = TweetSchema,
   status_code = status.HTTP_200_OK,
   summary = "Detalle del Tweet en DB",
   tags = ["Tweets Data Base"]
)
async def detail_tweet(tweet_id: str):   
   """
    Detalle del Tweet
    
    EndPoint para ver el detalle de un tweet.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    - Return:
        - "tweet_id"
        - "content"
        - "create_tw_date"
        - "update_tw_date"
        - "user_id_create"
        
    """
   result = conn.execute(tweetsModel.select().where(tweetsModel.c.tweet_id == tweet_id)).first()
   if result:
        return result
   else:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = f"¡No se encontro información Tweet!" 
      )
      

### Eliminar un Tweet
@tweet.delete(
   path = "/tweet/delete/{tweet_id}",
   status_code = status.HTTP_200_OK,
   summary = "Detalle del Tweet en DB",
   tags = ["Tweets Data Base"]
)
def delete_tweet(tweet_id: str = Path(
   ...,
   description = "Escriba el ID del Tweet a eliminar",
)):
   """
    Eliminar un Tweet
    
    EndPoint para eliminar un tweet.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    - Return:
        - status code: 200 OK
        
   """
   conn.execute(tweetsModel.delete().where(tweetsModel.c.tweet_id == tweet_id))
   return HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = f"¡No se encontro el Tweet, intente nuevamente!" 
      )


## Editar Tweet
@tweet.put(
   path = "/tweet/edit/{tweet_id}",
   response_model = TweetSchema,
   status_code = status.HTTP_200_OK,
   summary = "Editar Tweet en DB",
   tags = ["Tweets Data Base"]
)
async def update_tweet(
   tweet_id: str,
   tweet: TweetSchema
):
   """
    Crear Tweet
    
    EndPoint para editar un tweet.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    - Request BODY (raw -> (JSON)):
        - "content" : contenido del tweet - (String(250))
        - "update_tw_date" : actualización del tweet -(String(30))
    
    - Return:
        - "tweet_id"
        - "content"
        - "create_tw_date"
        - "update_tw_date"
        - "user_id_create"
        
    """
   conn.execute(tweetsModel.update().values(
      content = tweet.content,
      update_tw_date = tweet.update_tw_date,
   ).where(tweetsModel.c.tweet_id == tweet_id))
   result = conn.execute(tweetsModel.select().where(tweetsModel.c.tweet_id == tweet_id)).first()
   if result:
      return result
   else:
      raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="¡No se pudo actualizar el Tweet, intente nuevamente!"
      )
   