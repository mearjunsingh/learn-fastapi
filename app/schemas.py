from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    published: bool = False


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True