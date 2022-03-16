from pydantic import BaseSettings
from functools import lru_cache
from environs import Env


class Config(BaseSettings):
    PROJECT_NAME: str = "PornoLabApi"
    API_STR: str = "/api"


@lru_cache()
def get_config() -> Config:
    env = Env
    env.read_env()

    return Config()


settings = get_config()
