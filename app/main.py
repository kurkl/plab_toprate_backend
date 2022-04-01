import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import settings, redis_pool
from app.core.events import connect_to_redis, disconnect_from_redis

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_STR}/openapi.json",
    )
    settings.prepare_logging()
    app.state.redis_pool = redis_pool
    app.add_event_handler("startup", connect_to_redis)
    app.add_event_handler("shutdown", disconnect_from_redis)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_STR)

    return app


if __name__ == "__main__":
    from uvicorn import run  # noqa

    run("main:get_app", host="127.0.0.1", port=5001, log_level="info", reload=True, factory=True)
