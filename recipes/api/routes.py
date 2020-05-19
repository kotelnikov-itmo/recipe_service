from typing import List

from fastapi import APIRouter, Depends, exceptions

from db import get_db
from .schemas import RecipeFilter, RecipeSchema, RecipeCreateSchema, RecipeUpdateSchema
from auth.api.schemas import UserProfileSchema
from recipes.services import RecipeService
from auth.services import UserService
from auth.api.utils import get_current_user

router = APIRouter()


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


@router.post('/recipes/{recipe_id}/add2favorites', response_model=List[RecipeSchema])
async def add_recipe_to_favorites(recipe_id: int,
                                  cur_user=Depends(get_current_user), db=Depends(get_db)):
    """Добавление рецепта в избранное пользователя;
    """
    recipe = RecipeService(db).get(recipe_id)
    if recipe is None:
        raise exceptions.HTTPException(status_code=404, detail="Recipe not found")
    result = RecipeService(db).add_to_user_favorites(user=cur_user, recipe=recipe)
    return result


@router.get('/recipes/favorites', response_model=List[RecipeSchema])
async def get_favorites(cur_user=Depends(get_current_user)):
    """Получение списĸа избранных рецептов;
    """
    return cur_user.favorites


@router.post('/recipes/', response_model=RecipeSchema)
async def create_recipe(recipe_data: RecipeCreateSchema,
                        cur_user=Depends(get_current_user), db=Depends(get_db)):
    """Создание нового рецепта;
    """
    if not cur_user.is_active:
        raise exceptions.HTTPException(status_code=403)
    recipe = RecipeService(db).create(recipe_data, cur_user)
    return recipe


@router.put('/recipes/{recipe_id}', response_model=RecipeSchema)
async def update_recipe(recipe_id: int, recipe_data: RecipeUpdateSchema,
                        cur_user=Depends(get_current_user), db=Depends(get_db)):
    """Изменение своих рецептов
    """
    recipe = RecipeService(db).get(recipe_id)
    if recipe.author_id != cur_user.id:
        raise exceptions.HTTPException(status_code=403)
    RecipeService(db).update(recipe, recipe_data)
    return recipe


@router.get('/recipes/my', response_model=List[RecipeSchema])
async def get_owned_recipes(cur_user=Depends(get_current_user), db=Depends(get_db)):
    """Получение списĸа своих рецептов;
    """
    recipes = RecipeService(db).get_list(author_id=cur_user.id)
    return recipes
