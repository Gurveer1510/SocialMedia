import bcrypt
from fastapi import Response
from app.core.config import settings
from jose import jwt, JWTError
import datetime
import time


def create_token(payload : dict):
    data = payload.copy()
    expire = time.time() + datetime.timedelta(minutes=settings.access_token_expire).total_seconds()
    data.update({'exp' : expire})

    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

    return {"access_token": encoded_jwt,  "refresh_token" : create_refresh_token(payload=payload)}

def create_access_token(payload:dict):

     data = payload.copy()
     expire = time.time() + datetime.timedelta(minutes=settings.access_token_expire).total_seconds()
     data.update({'exp' : expire})

     encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

     return {"access_token": encoded_jwt}

def create_refresh_token(payload: dict) :
    
    data = payload.copy()
    expires_delta = time.time() + datetime.timedelta(days=settings.refresh_token_expire).total_seconds()
    data.update({'exp' : expires_delta})

    encoded_jwt = jwt.encode(data, settings.secret_key, settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentialException):
    try:

        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        username: str = payload.get("username")
        if username is None :
            raise credentialException
        
        token_data = payload

    except JWTError:
        raise credentialException
    
    return token_data

def get_password(password : str) -> str:
    return bcrypt.hash(password)


def verify_password(password : str, hashed_password : str) -> bool:
    return bcrypt.verify(password, hashed_password)