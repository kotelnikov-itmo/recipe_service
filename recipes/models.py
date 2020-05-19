from datetime import datetime
from enum import IntEnum

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from db import ModelBase


class DishTypes(IntEnum):
    __tablename__ = "recipes"

    salad = 1
    first = 2
    second = 3
    soup = 4
    desert = 5
    drink = 6


though_table = sa.Table(
    'recipes2tags', ModelBase.metadata,
    sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.id')),
    sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id'))
)


class Tag(ModelBase):
    __tablename__ = "tags"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)


class Recipe(ModelBase):
    __tablename__ = "recipes"

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String)
    description = sa.Column(sa.Text)
    result_photo = sa.Column(sa.String)
    dish_type = sa.Column(sa.Enum(DishTypes))
    author_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    likes_count = sa.Column(sa.Integer, default=0)

    tags = relationship("Tag", secondary=though_table)
    is_active = sa.Column(sa.Boolean)
    created_at = sa.Column(sa.DateTime, default=datetime.now)

    author = relationship('User', backref="own_recipes")
