from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HRMS Lite API"
    app_version: str = "0.1.0"
    debug: bool = True
    database_url: str = "sqlite:///./hrms_lite.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
