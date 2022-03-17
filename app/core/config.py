from enum import Enum
from typing import Type
from functools import lru_cache

from pydantic import BaseSettings


class AppEnvironments(Enum):
    prod: str = "prod"
    dev: str = "dev"


class BaseAppConfig(BaseSettings):
    app_env: AppEnvironments = AppEnvironments.dev

    class Config:
        case_sensitive = True
        env_file = ".env.dev"


class AppConfig(BaseAppConfig):
    DEBUG: bool = False
    PROJECT_NAME: str = "PornoLabApi"
    API_STR: str = "/api"
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    ALLOWED_HOSTS: list[str] = ["*"]

    def prepare_logging(self):
        pass


class DevAppConfig(AppConfig):
    debug: bool = True


class ProdAppConfig(AppConfig):
    class Config(AppConfig.Config):
        env_file = ".env.dev.prod"


environments: dict[AppEnvironments, Type[AppConfig]] = {
    AppEnvironments.dev: DevAppConfig,
    AppEnvironments.prod: ProdAppConfig,
}


@lru_cache()
def get_app_config() -> AppConfig:
    app_env = BaseAppConfig().app_env
    config = environments[app_env]

    return config()


settings = get_app_config()
