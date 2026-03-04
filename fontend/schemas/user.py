from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, ConfigDict, EmailStr, Field

T = TypeVar("T")

class CustomResponse(BaseModel, Generic[T]):
    isSuccess: bool
    statusCode: int
    data: T


class UserBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    profile: Optional[str] = Field(default=None, max_length=500)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    profile: Optional[str] = Field(default=None, max_length=500)
    password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)