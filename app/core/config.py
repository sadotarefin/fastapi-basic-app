from typing_extensions import Annotated
from functools import lru_cache 
from pydantic_settings import BaseSettings, SettingsConfigDict

from fastapi import Depends

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ADMIN_USERNAME:str = "admin"
    ADMIN_PASS: str = "admin123"
    ADMIN_EMAIL: str | None = None
    ADMIN_FULL_NAME: str | None = None

    model_config = SettingsConfigDict(
        env_file=str(".env"),
        env_file_encoding="utf-8",
    )

@lru_cache
def get_app_settings():
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_app_settings)]