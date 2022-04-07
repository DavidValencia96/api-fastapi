# python
from datetime import date
from datetime import datetime
# Pydantic
from pydantic import BaseModel # Permite crear los modelos
from pydantic import Field # Validar los atributos de un modelo

# Typing
from typing import Optional


class TweetSchema(BaseModel):
    tweet_id: Optional[str]
    content:  str =  Field(
        ..., 
        min_length = 1,
        max_length = 255,
        example = "contenido del tweet"
    )
    create_tw_date: Optional[date] = Field(default=None)
    update_tw_date: Optional[date] = Field(default=None)
    user_id_create: int = 0