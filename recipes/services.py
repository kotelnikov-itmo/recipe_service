from utils.services import *

from recipes.models import Recipe, Tag, DishTypes
from auth.models import User
from recipes.api.schemas import RecipeCreateSchema, RecipeUpdateSchema
from conf import get_settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = get_settings().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 24 * 36000


class RecipeService(DBModelService):
    def get(self, id_: int) -> Recipe:
        return self._db.query(Recipe).get(id_)

    def create(self, initial: RecipeCreateSchema, author: User) -> Recipe:
        instance = Recipe(**initial.dict(exclude_unset=True), author_id=author.id)
        instance.is_active = True
        return self._save_obj(instance)

    def update(self, instance: Recipe, data: RecipeUpdateSchema) -> Recipe:
        updated_data = data.dict(exclude_unset=True)
        for field, value in updated_data.items():
            setattr(instance, field, value)
        return self._save_obj(instance)

    def add_to_user_favorites(self, user: User, recipe: Recipe) -> List[Recipe]:
        user.favorites.append(recipe)
        user = self._save_obj(user)
        return user.favorites

    def get_list(self,
                 title: Optional[str] = None,
                 dish_type: Optional[int] = None,
                 tag: Optional[str] = None,
                 author_id: Optional[int] = None
                 ) -> List[Recipe]:
        q = self._db.query(Recipe).filter(Recipe.is_active == True)
        # filters:
        if title is not None:
            q = q.filter(Recipe.title.like(f"%{title}%"))
        if dish_type is not None:
            q = q.filter(Recipe.dish_type == DishTypes(dish_type))
        if tag is not None:
            q = q.outerjoin(Recipe.tags).filter(Recipe.tags.any(Tag.title == tag))
        if author_id is not None:
            q = q.filter(Recipe.author_id == author_id)
        return q.all()

    def get_top(self, limit: int) -> List[Recipe]:
        return self._db.query(Recipe).order_by(Recipe.likes_count.desc()).limit(limit).all()
