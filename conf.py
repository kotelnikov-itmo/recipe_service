import os
from typing import Union

from pydantic import BaseSettings, Field, DirectoryPath, PostgresDsn, AnyUrl
from functools import lru_cache

BASE_DIR = os.path.dirname(__file__)


class _AppSettings(BaseSettings):
    debug: bool = False
    sql_debug: bool = Field(False, description="show queries in console")
    host: str = Field("localhost")
    port: int = Field(8000, le=10000, ge=80)
    secret_key: str = Field("", env="APP_SECRET")
    api_root_url = "/api"
    db_url: Union[PostgresDsn, AnyUrl, str] = "postgresql://user:password@localhost/dand_wine_game_db"
    base_dir: DirectoryPath = BASE_DIR
    # event_strict_mode: bool = Field(False, description="raise error for unsupported game event type")
    # event_log_dir: DirectoryPath = os.path.join(os.path.dirname(BASE_DIR), "game_logs/")


@lru_cache(maxsize=1)
def get_settings(env_file: str = ".env"):
    _settings = _AppSettings(_env_file=env_file)
    assert _settings.secret_key, "App secret key must be set"
    return _settings
