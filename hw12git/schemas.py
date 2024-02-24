from datetime import datetime
from pydantic import BaseModel, Field


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16) 
    email: str  
    password: str = Field(min_length=6, max_length=10)

class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created: datetime
    avatar: str

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactModel(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=30)
    phone: str = Field(max_length=13)  
    birthday: datetime
    inform: str = Field(max_length=150)
    email: str   


class ContactUpdate(BaseModel):
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=30)
    phone: str = Field(max_length=13)
    birthday: datetime
    inform: str = Field(max_length=150)
    email: str   

class ContactUpdateAvatar(BaseModel):
    avatar: str


class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True
