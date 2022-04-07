# python
from datetime import date
from datetime import datetime

# Pydantic
from pydantic import BaseModel # Permite crear los modelos
from pydantic import Field # Validar los atributos de un modelo

# Typing
from typing import Optional


class CommentsSchemas(BaseModel):
    comment_id: Optional[str]
    tweet_id: Optional[str]
    comment_content:  str =  Field(
        ..., 
        min_length = 1,
        max_length = 255,
        example = "Comentario"
    )
    cm_create_date: Optional[date] = Field(default=None)
    cm_update_date: Optional[date] = Field(default=None)
    user_id_comment: int = 0