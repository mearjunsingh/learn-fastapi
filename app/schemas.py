from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    published: bool = False


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True