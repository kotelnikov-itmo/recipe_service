import sqlalchemy as sa
from sqlalchemy.orm import relationship

from db import ModelBase


recipe2user_table = sa.Table(
    'recipes2users', ModelBase.metadata,
    sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.id')),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
)


class User(ModelBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    hpass = sa.Column(sa.String)
    username = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean)

    favorites = relationship(
        "Recipe", secondary=recipe2user_table
    )