from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


# User schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    books: List['BookResponse'] = []

    class Config:
        from_attributes = True


# Book schema
class BookBase(BaseModel):
    title: str
    language: Optional[str] = None
    isbn: str
    pages: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    year: datetime
    user_id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str
    email: str
    is_active: bool
    password: str = None


class BookUpdate(BaseModel):
    title: str
    language: str
    isbn: str
    pages: int


class Book(BookBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
