from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, EmailStr

T = TypeVar("T")

class CustomResponse(BaseModel, Generic[T]):
    isSuccess: bool
    statusCode: int
    data: T

class UserBase(BaseModel):
    name: str
    email: EmailStr
    profile: str

class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    profile: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True