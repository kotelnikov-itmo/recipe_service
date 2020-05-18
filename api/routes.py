from typing import List

from fastapi import APIRouter, Depends

from db import get_db
from .schemas import UserCreateSchema, UserProfileSchema, RecipeFilter, RecipeSchema
from services import UserService, RecipeService


router = APIRouter()


@router.post("/users", response_model=UserProfileSchema)
async def create_user(user_data: UserCreateSchema,
                      db=Depends(get_db)):
    """Регистрация нового пользователя;
    """
    user = UserService(db).create_user(**user_data.dict())
    return user


@router.get("/users/{user_id}", response_model=UserProfileSchema)
async def get_user_profile(user_id: int,
                           db=Depends(get_db)):
    """Получение профиля пользователя.
    Передавать все поля модели пользователя плюс ĸоличество рецептов, созданных пользователем;
    """
    user = UserService(db).get_user(id_=user_id)
    return user


@router.get("/recipes", response_model=List[RecipeSchema])
async def get_recipes(filters: RecipeFilter = Depends(), db=Depends(get_db)):
    """Получение списĸа рецептов;
    Фильтрация рецептов по: части названия, типу блюда, хештегу;
    """
    recipes = RecipeService(db).get_list(**filters.dict(exclude_unset=True))
    print(recipes)
    return recipes


@router.get("/recipes/top", response_model=List[RecipeSchema])
async def get_recipes_top(limit: int = 10, db=Depends(get_db)):
    """Получение ТОП-а рецептов (больше лайĸов, выше место в рейтинге).
    Количество рецептов в выдаче передается параметром `limit`.
    """
    recipes = RecipeService(db).get_top(limit)
    return recipes
