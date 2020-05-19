from typing import Optional, List

from pydantic import BaseModel


#  USER

class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserAuthCredentialsSchema(BaseModel):
    username: str
    password: str


class UserProfileSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    favorites: Optional[List[str]]
    owned_recipes_count: int = 0

    class Config:
        orm_mode = True


#  TOKEN

class UserTokenData(BaseModel):
    """User data for JWT token payload"""
    sub: str


class ResponseWithToken(BaseModel):
    """Return JWT Token"""
    token: str

