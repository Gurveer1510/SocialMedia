from fastapi import APIRouter, Depends, status, HTTPException,Response, Header
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user_model import Users
from app.services.user_service import UserService
from app.schemas.user_schema import TokenOut
from jose import JWTError, jwt
from app.core.security import create_token, verify_access_token, create_access_token
from app.core.config import settings

auth_router = APIRouter(tags=["users"])


@auth_router.post("/login", description="cookie bases authentication. The access and refresh Token are stored as cookies")
async def login_user( response : Response, formData: OAuth2PasswordRequestForm = Depends()):
    username = formData.username
    password = formData.password

    user = await UserService.authenticate(username, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"invalid credentials"
        )
    
    data = create_token({"username": user.username, "email": user.email})
    response.set_cookie(key='token_data', value=data)
    return data

@auth_router.post("/refresh_token")
async def refresh_token(response : Response, refresh_token : str = Header(convert_underscores=False)):
    credential_exception = f"refresh token expired. login again"
    try:
        payload = verify_access_token(refresh_token, credentialException=credential_exception)
        # print(payload)
        token = create_access_token(payload=payload)
        cookie = {
            'access_token' : token['access_token'],
            'refresh_token' : refresh_token
        }
        response.delete_cookie(key='token_data')
        response.set_cookie(key='token_data', value=cookie)

        return {
            'data' : cookie
        }

    except JWTError:
        raise credential_exception


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, description=f"will remove the token data cookie")
async def logout(response : Response):
    try:
        response.delete_cookie('token_data')

    except:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"authenticate yourself first")

