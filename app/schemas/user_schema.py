from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from uuid import UUID


class FollowSchema(BaseModel):
    user_id : UUID
    username : str
    email : EmailStr
    profile_pic : Optional[str] = None



class UserAuth(BaseModel):
    email : EmailStr = Field(..., description="user email")
    username : str = Field(..., max_length=20)
    hashed_password: str = Field(..., max_length=20)


class UserOut(BaseModel):
    user_id : UUID
    username: str
    email: str
    followers: Optional[List['FollowSchema']] = []
    following: Optional[List['FollowSchema']] = []
    profile_pic: Optional[str] = None
  

class TokenOut(BaseModel):
    data: dict
