import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    test = "test"
    local = "local"
    preview = "preview"
    production = "production"


environment = Environment(os.getenv("APP_ENV", Environment.local.value))
environment_file = f".env.{environment.value}"


class Settings(BaseSettings):
    ENV: Environment = Environment.local
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    GIT_HOME: str = "/srv/git"

    APP_URL: str = "http://127.0.0.1:8000"

    DEFAULT_GIT_USERNAME: str = "admin"
    DEFAULT_GIT_PASSWORD: str = "admin"

    model_config = SettingsConfigDict(
        env_prefix="app_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=environment_file,
        extra="allow",
    )

    def is_environment(self, environment: Environment) -> bool:
        return self.ENV == environment

    def is_production(self) -> bool:
        return self.is_environment(Environment.production)


settings = Settings()
