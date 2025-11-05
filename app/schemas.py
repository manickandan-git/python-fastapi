from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserBase(BaseModel):
    email: EmailStr
    phone_number: Optional[str]
    
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class config:
        orm_mode = True
    
class UserCreate(UserBase):
    password: str  
    

class UserLogin(UserBase):
    password: str

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    



