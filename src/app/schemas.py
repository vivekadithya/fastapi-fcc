from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserBase(BaseModel):
    email:EmailStr
    password:str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True # Optional property (sets to default)

class PostCreate(PostBase):
    pass


class Post(PostBase): # inherits the props from PostBase and adds id, created_at
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        orm_mode = True

