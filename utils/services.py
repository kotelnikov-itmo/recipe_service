from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import ModelBase

ModelType = TypeVar("ModelType", bound=ModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class DBModelService(object):
    def __init__(self, db: Session):
        self._db = db

    def _save_obj(self, obj: ModelBase):
        """add + commit + refresh
        """
        self._db.add(obj)
        self._db.commit()
        self._db.refresh(obj)
        return obj
