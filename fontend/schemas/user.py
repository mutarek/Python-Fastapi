from typing import Generic, TypeVar
from pydantic import BaseModel, EmailStr

T = TypeVar("T")

class CustomResponse(BaseModel, Generic[T]):
    Issueless: bool
    statusCode: int
    data: T

class UserBase(BaseModel):
    name: str
    email: EmailStr
    profile: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int