from jwt import encode, decode
from jwt import exceptions
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime, timedelta
from os import getenv



def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(
        payload = {
            **data, 
            "exp": expire_date(1)
        }, 
        key=getenv("SECRET"),
        algorithm = "HS256"
    )
    return token


def validate_token(token, output = False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms = ["HS256"])
        decode(token, key=getenv("SECRET"), algorithms = ["HS256"])
    except exceptions.DecodeError:
        return JSONResponse(
            content={"menssage": "Invalid Token"}, 
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    except exceptions.ExpiredSignatureError:
        return JSONResponse(
            content={"menssage": "El token ha sido expirado"}, 
            status_code = status.HTTP_401_UNAUTHORIZED
        )
    except exceptions.InvalidTokenError:
        return JSONResponse(
            content={"menssage": "DecodeError"}, 
            status_code = status.HTTP_401_UNAUTHORIZED
        )