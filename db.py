# from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf import get_settings


settings = get_settings()

db_engine = create_engine(settings.db_url, echo=settings.sql_debug)

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

ModelBase = declarative_base()


# @lru_cache()
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
