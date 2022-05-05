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
from models.commentsModel import commentsModel
from schemas.commentsSchemas import CommentsSchemas
from middlewares.verify_toke_routes import VerifyTokenRoute


# comment = APIRouter(route_class=VerifyTokenRoute)
comment = APIRouter()

# Path Operations

## Comments

### Mostrar todos los comentarios
@comment.get(
    path = "/comment",
    response_model = List[CommentsSchemas],
    status_code = status.HTTP_200_OK,
    summary = "Commentarios en los Tweet's",
    tags = ["Comments Data Base"]
)
def  list_comment():
   """
    Listar comentarios
    
    EndPoint para listar todos los comentarios de los tweets.

    Parameters:
    - Headers
        - Content-Type: application/json
        - Authorization: Bearer Token {jwt_token}

    - Return:
        - "comment_id"
        - "tweet_id"
        - "comment_content"
        - "cm_create_date"
        - "cm_update_date"
        - "user_id_comment"
        
    """
   result = conn.execute(commentsModel.select()).fetchall() # Retorna todo los datos de consulta a la db 
   if result:
       return result
   else:
      raise HTTPException(
              status_code = status.HTTP_404_NOT_FOUND,
              detail = f"¡No hay comentarios publicados!" 
       )


### Crear comentario
@comment.post(
    path = "/comment/create",
    response_model = CommentsSchemas,
    status_code = status.HTTP_200_OK,
    summary = "Crear comentario",
    tags = ["Comments Data Base"]
)
def create_comment(comment: CommentsSchemas = Body(...)):
   """
   Crear comentario de un tweet
   
   EndPoint para crear un un comentario de un tweet.

   Parameters:
   - Headers
       - Content-Type: application/json
       - Authorization: Bearer Token {jwt_token}

   - Request BODY (raw -> (JSON)):
      - "tweet_id" : ID del tweet el cual estara asociado el twwet - (Integer)
      - "comment_content" : Detalle comentario - (Strgin(255))
      - "cm_create_date" : fecha de creación de comentario - (Strgin(30))
      - "cm_update_date" : fecha de modificación de comentario - (Strgin(30))
      - "user_id_comment" : usuario que creo el comentario -  - (Integer)
      
   - Return:
      - "comment_id"
      - "tweet_id"
      - "comment_content"
      - "cm_create_date"
      - "cm_update_date"
      - "user_id_comment"
       
   """
   new_comment = {
       "tweet_id": comment.tweet_id,
       "comment_content": comment.comment_content,
       "cm_create_date": comment.cm_create_date,
       "cm_update_date": comment.cm_update_date,
       "user_id_comment": comment.user_id_comment
   }
   result = conn.execute(commentsModel.insert().values(new_comment))
   return conn.execute(commentsModel.select().where(commentsModel.c.comment_id == result.lastrowid)).first()

### Detalle comentario
@comment.get(
   path = "/comment/detail/{comment_id}",
   response_model = CommentsSchemas,
   status_code = status.HTTP_200_OK,
   summary = "Detalle comentario en DB",
   tags = ["Comments Data Base"]
)
def detail_comment(comment_id: str):
   """
   Detalle de un comentario
   
   EndPoint para ver el detalle de un comentario.

   Parameters:
   - Headers
       - Content-Type: application/json
       - Authorization: Bearer Token {jwt_token}
      
   - Return:
      - "comment_id"
      - "tweet_id"
      - "comment_content"
      - "cm_create_date"
      - "cm_update_date"
      - "user_id_comment"
       
   """
   result = conn.execute(commentsModel.select().where(commentsModel.c.comment_id == comment_id)).first()
   print(result)
   if result:
        return result
   else:
      raise HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = f"¡No se encontro información del comentario!" 
      )

### Eliminar un commentario
@comment.delete(
   path = "/comment/delete/{comment_id}",
   status_code = status.HTTP_200_OK,
   summary = "Eliminar comentario en DB",
   tags = ["Comments Data Base"]
)
def delete_comment(comment_id: str = Path(
   ...,
   description = "Escriba el ID del comentario a eliminar",
)):
   """
   Detalle de un comentario
   
   EndPoint para ver el detalle de un comentario.

   Parameters:
   - Headers
       - Content-Type: application/json
       - Authorization: Bearer Token {jwt_token}
      
   - Return:
      - status code: 200 OK
       
   """
   conn.execute(commentsModel.delete().where(commentsModel.c.comment_id == comment_id))
   return HTTPException(
         status_code = status.HTTP_404_NOT_FOUND,
         detail = f"¡No se elimino el comentarios, intente nuevamente!" 
      )

### Editar un commentario
@comment.put(
   path = "/comment/edit/{comment_id}",
   response_model = CommentsSchemas,
   status_code = status.HTTP_200_OK,
   summary = "Editar un comentario en DB",
   tags = ["Comments Data Base"]
)
def update_comment(
   comment_id: str,
   comment: CommentsSchemas
):
   """
   Crear comentario de un tweet
   
   EndPoint para crear un un comentario de un tweet.

   Parameters:
   - Headers
       - Content-Type: application/json
       - Authorization: Bearer Token {jwt_token}

   - Request BODY (raw -> (JSON)):
      - "comment_content" : detalle comentario - (Strgin(255))
      - "update_tw_date" :  fecha de modificación - (Strgin(30))
      
   - Return:
      - "comment_id"
      - "tweet_id"
      - "comment_content"
      - "cm_create_date"
      - "cm_update_date"
      - "user_id_comment"
       
   """
   conn.execute(commentsModel.update().values(
      comment_content = comment.comment_content,
      cm_update_date = comment.cm_update_date,
   ).where(commentsModel.c.comment_id == comment_id))
   result = conn.execute(commentsModel.select().where(commentsModel.c.comment_id == comment_id)).first()
   if result:
      return result
   else:
      raise HTTPException(
            status_code=status.HTTP_304_NOT_MODIFIED,
            detail="¡No se pudo actualizar el comentario, intente nuevamente!"
      )