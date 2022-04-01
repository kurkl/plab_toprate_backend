from fastapi import Path, Depends
from aioredis import Redis

from app.core.config import settings, redis_pool
from app.services.site_parser import PLabParser, PlabParserConfig


def get_redis() -> Redis:
    return redis_pool.redis


def get_parser_config() -> PlabParserConfig:
    return PlabParserConfig(
        headers=settings.PLAB_HEADERS,
        auth_form_data=settings.PLAB_AUTH_FORM_DATA,
        index_page=settings.PLAB_INDEX_PAGE,
    )


def get_site_parser(config: PlabParserConfig = Depends(get_parser_config)) -> PLabParser:
    return PLabParser(config)


async def get_current_categories_from_path(
    slug: str = Path(..., min_length=1),
    site_parser: PLabParser = Depends(get_site_parser),
    redis: Redis = Depends(get_redis),
):
    raise NotImplementedError
