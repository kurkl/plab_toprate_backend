from enum import Enum
from typing import Type
from functools import lru_cache

from pydantic import RedisDsn, BaseSettings, validator

from app.services.redis import RedisPool


class AppEnvironments(Enum):
    prod: str = "prod"
    dev: str = "dev"
    local: str = "local"


class BaseAppConfig(BaseSettings):
    app_env: AppEnvironments = AppEnvironments.dev

    class Config:
        case_sensitive = True
        env_file = ".env.dev"


class AppConfig(BaseAppConfig):
    # Common
    DEBUG: bool
    PROJECT_NAME: str
    API_STR: str = "/api"
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    ALLOWED_HOSTS: list[str] = ["*"]

    # Redis
    REDIS_STORAGE_URI: RedisDsn

    # Plab params
    PLAB_LOGIN: str
    PLAB_PASS: str
    ENCODED_LOGIN: str
    PLAB_AUTH_FORM_DATA: dict | None = None
    PLAB_INDEX_PAGE: str
    PLAB_HEADERS: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46 "
    }

    @validator("PLAB_AUTH_FORM_DATA", pre=True, allow_reuse=True)
    def assemble_auth_form_data(cls, v: dict | None, values: dict) -> dict:
        if isinstance(v, dict):
            return v

        return dict(
            login_username=values.get("PLAB_LOGIN"),
            login_password=values.get("PLAB_PASS"),
            login=values.get("ENCODED_LOGIN"),
        )

    def prepare_logging(self):
        pass


class DevAppConfig(AppConfig):
    debug: bool = True


class LocalAppConfig(AppConfig):
    class Config(AppConfig.Config):
        env_file = "../.env.dev"


class ProdAppConfig(AppConfig):
    class Config(AppConfig.Config):
        env_file = ".env.prod"


environments: dict[AppEnvironments, Type[AppConfig]] = {
    AppEnvironments.dev: DevAppConfig,
    AppEnvironments.prod: ProdAppConfig,
    AppEnvironments.local: LocalAppConfig,
}


@lru_cache()
def get_app_config() -> AppConfig:
    app_env = BaseAppConfig().app_env
    config = environments[app_env]

    return config()


settings = get_app_config()


def create_redis_pool() -> RedisPool:
    return RedisPool(settings.REDIS_STORAGE_URI)


redis_pool = create_redis_pool()
