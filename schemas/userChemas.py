# python
from datetime import date
from datetime import datetime
# Pydantic
from pydantic import BaseModel # Permite crear los modelos
from pydantic import EmailStr # Valida emails
from pydantic import Field # Validar los atributos de un modelo

# Typing
from typing import Optional

class User(BaseModel):
    id: Optional[str]
    name: str =  Field(
        ..., 
        min_length = 1,
        max_length = 50,
        example = "juan David Valencia"
    )
    country: str =  Field(
        ..., 
        min_length = 1,
        max_length = 20,
        example = "Colombia"
    )
    phone: str =  Field(
        ..., 
        min_length = 7,
        max_length = 10,
        example = "3123456789"
    )
    user_create: Optional[date] = Field(default=None)
    email: EmailStr = Field(...)
    password: str = Field(
        ..., 
        min_length = 1,
        max_length = 50,
    )
    tipo_user: int = 0