from beanie import Document, Indexed
from uuid import UUID
from typing import Annotated
from pydantic import BaseModel


class LikeModel(BaseModel):
    post_id : UUID
    user_id : UUID

class Likes(Document):
    like : Annotated[LikeModel, Indexed(unique=True)]

    class Settings:
        name = "likes"
       
