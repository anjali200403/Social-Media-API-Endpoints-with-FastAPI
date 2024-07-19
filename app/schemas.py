from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserOut(BaseModel):
    id:int
    email:EmailStr

    class Config:
        orm_mode=True
        
class PostIn(BaseModel):
    title: str
    content: str
    published: bool =True
    rating: Optional[int] =None


class Post(BaseModel):
    title: str
    content: str
    published: bool =True
    rating: Optional[int] =None
    owner: UserOut

class PostOut(BaseModel):
    Post:Post
    votes:int

class UserCreate(BaseModel):
    email:EmailStr
    password: str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
