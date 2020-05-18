from utils.services import *
from passlib.context import CryptContext

from models import User, Recipe, Tag, DishTypes
from utils.db.queries import fast_count
from conf import get_settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = get_settings().secret_key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 24 * 36000


class UserService(DBModelService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user(self, id_: Optional[int] = None, username: Optional[str] = None) -> Union[User, None]:
        if id_ is not None:
            user = self._db.query(User).get(id_)
            user.owned_recipes_count = fast_count(self._db.query(Recipe).filter(Recipe.author_id == user.id))
            return user
        elif username is not None:
            return self._db.query(User).filter(User.username == username).first()
        else:
            return None

    def create_user(self, username: str, password: str):
        instance = User(username=username)
        instance.is_active = True
        instance.hpass = self.pwd_context.hash(password)
        self._db.add(instance)
        self._db.commit()
        self._db.refresh(instance)
        return instance


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
