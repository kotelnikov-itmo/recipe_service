from utils.services import *

from recipes.models import Recipe, Tag, DishTypes
from conf import get_settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = get_settings().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 24 * 36000


class RecipeService(DBModelService):
    def get_list(self,
                 title: Optional[str] = None,
                 dish_type: Optional[int] = None,
                 tag: Optional[str] = None,
                 ):
        q = self._db.query(Recipe).filter(Recipe.is_active is True)
        # filters:
        if title is not None:
            q = q.filter(Recipe.title.like(f"%{title}%"))
        if dish_type is not None:
            q = q.filter(Recipe.dish_type == DishTypes(dish_type))
        if tag is not None:
            q = q.outerjoin(Recipe.tags).filter(Recipe.tags.any(Tag.title == tag))
        return q.all()

    def get_top(self, limit: int):
        return self._db.query(Recipe).order_by(Recipe.likes_count.desc()).limit(limit).all()
