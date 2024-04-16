from beanie import Document

from pydantic import Field
from typing import Optional, List
from uuid import UUID, uuid4
from app.schemas.user_schema import FollowSchema


class Post(Document):
    post_id : UUID = Field(default_factory=uuid4)
    caption : str
    post_image : str
    likes: Optional[int] = 0
    liked_by : Optional[List["FollowSchema"] ] =  []
    owner : FollowSchema
    # comments: 

    class Settings:
        name = "posts"