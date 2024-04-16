from pydantic import BaseModel


class Post_Schema(BaseModel):
    caption : str

    # owner : Users


