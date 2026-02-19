from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HRMS Lite API"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "mongodb://localhost:27017"
    database_name: str = "hrms_lite"
    api_v1_prefix: str = ""
    cors_origins: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in {"1", "true", "yes", "on", "debug"}
        return False

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("database_name", mode="before")
    @classmethod
    def parse_database_name(cls, value):
        if isinstance(value, str) and value.strip():
            return value.strip()
        return "hrms_lite"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
