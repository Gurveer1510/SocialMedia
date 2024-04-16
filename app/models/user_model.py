from beanie import Document, Indexed
from pydantic import Field, EmailStr
from typing import Annotated
from typing import Optional, List, Set
from uuid import UUID, uuid4
from app.schemas.user_schema import FollowSchema


class Users(Document):
    user_id : UUID = Field(default_factory=uuid4)
    username: Annotated[str, Indexed(unique = True)]
    email : Annotated[EmailStr, Indexed(unique = True)]
    hashed_password : str 
    followers: Optional[List['FollowSchema']] = []
    following: Optional[List['FollowSchema']] = []
    profile_pic: Optional[str] = None


    class Settings:
        name = "users"




