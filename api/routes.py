from typing import List

from fastapi import APIRouter, Depends

from db import get_db
from .schemas import UserCreateSchema, UserProfileSchema, RecipeFilter, RecipeSchema
from services import UserService, RecipeService


router = APIRouter()


@router.post("/users", response_model=UserProfileSchema)
async def create_user(user_data: UserCreateSchema,
                      db=Depends(get_db)):
    user = UserService(db).create_user(**user_data.dict())
    return user


@router.get("/users/{user_id}", response_model=UserProfileSchema)
async def get_user_profile(user_id: int,
                           db=Depends(get_db)):
    user = UserService(db).get_user(id_=user_id)
    return user


@router.get("/recipes", response_model=List[RecipeSchema])
async def get_recipes(filters: RecipeFilter = Depends(), db=Depends(get_db)):
    recipes = RecipeService(db).get_list(**filters.dict(exclude_unset=True))
    print(recipes)
    return recipes


@router.get("/recipes/top", response_model=List[RecipeSchema])
async def get_recipes_top(limit: int = 10, db=Depends(get_db)):
    recipes = RecipeService(db).get_top(limit)
    return recipes
