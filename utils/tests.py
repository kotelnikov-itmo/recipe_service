from datetime import datetime, timedelta
from copy import deepcopy
from fastapi.testclient import TestClient
from fastapi import Depends
from unittest import TestCase, mock
from sqlalchemy.orm import Session
from pprint import pp
from pydantic.json import pydantic_encoder

from main import app
from database import LocalSession, BaseORMModel, db_engine

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy_utils as sa_utils


from conf import get_settings


settings = get_settings()
assert settings.db_url


class DbTestCase(TestCase):
    """
    TestCase with isolated DB session.

    Create database for test (named with prefix 'test_') with current schema on setUp;
    Drop test database on tearDown.
    """
    db_conn: Session
    _db_patcher: mock._patch

    @classmethod
    def setUpClass(cls) -> None:
        # test_db_url = deepcopy(settings.db_url)
        test_db_name = "test_" + settings.db_url.path[1:]
        # print(test_db_url)
        test_db_url = "/".join(settings.db_url.split("/")[:-1] + [test_db_name, ])
        print(test_db_url)
        print(7)
        if sa_utils.database_exists(test_db_url):
            print("Old test database exists")
            sa_utils.drop_database(test_db_url)

        sa_utils.create_database(test_db_url)
        print(f"Test database {test_db_url} created")
        test_db_engine = create_engine(test_db_url, echo=settings.sql_debug)
        _TestDBSession = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
        cls.db_conn = _TestDBSession()
        cls._db_patcher = mock.patch('database.LocalSession')
        get_test_db = cls._db_patcher.start()
        get_test_db.return_value = _TestDBSession()
        BaseORMModel.metadata.create_all(bind=test_db_engine, checkfirst=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db_conn.close()

        _db_url = cls.db_conn.get_bind().url
        sa_utils.drop_database(_db_url)
        print(f"Database {_db_url} dropped")

        cls._db_patcher.stop()
