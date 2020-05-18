from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, HttpUrl

from models import DishTypes


class UserCreateSchema(BaseModel):
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


class ShortUserProfileSchema(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class RecipeFilter(BaseModel):
    title: Optional[str]
    dish_type: Optional[int]
    tag: Optional[str]


class TagSchema(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class RecipeSchema(BaseModel):
    """Full recipe data
    """
    id: int
    title: str
    description: str
    result_photo: Optional[HttpUrl]
    dish_type: DishTypes
    author: ShortUserProfileSchema
    likes_count: int
    tags: List[TagSchema]
    created_at: datetime
    is_active : bool

    class Config:
        orm_mode = True
