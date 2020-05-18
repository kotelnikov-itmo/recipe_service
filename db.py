# from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf import get_settings


settings = get_settings()

db_engine = create_engine(settings.db_url, echo=settings.sql_debug)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

ModelBase = declarative_base()


# class DataBase(object):
#     def __init__(self):
#         pass
#
#
# class FakeDatabase(DataBase):
#     def __init__(self):
#         from initial_data import users, rooms, games
#         self.__data = {
#             "users": users,
#             "rooms": rooms,
#             "room_sessions": lambda: {r["session_key"]: r for r in rooms.values()},
#             "games": games
#         }
#         super().__init__()
#
#     def get_player_by_key(self, key: str) -> dict:
#         for room in self.__data["rooms"].values():
#             for m in room["members"]:
#                 if m["session_key"] == key:
#                     return m
#
#     def __getattr__(self, item):
#         if item in self.__data.keys():
#             return self.__data.get(item)
#         else:
#             return getattr(self, item)


# @lru_cache()
def get_db():
    # if fake:
    #     return FakeDatabase()
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
