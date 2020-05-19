from typing import Optional, Union

from passlib.context import CryptContext

from recipes.models import Recipe
from auth.models import User
from utils.db.queries import fast_count
from utils.services import DBModelService


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
