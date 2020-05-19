import sqlalchemy as sa

from db import ModelBase


class User(ModelBase):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True)
    hpass = sa.Column(sa.String)
    username = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean)