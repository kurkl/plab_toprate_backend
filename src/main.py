from fastapi import FastAPI
from src.core.config import settings
from src.core.logging import prepare_logging
from src.api.routes import api_router

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json")

app.include_router(api_router, prefix=settings.API_STR)

if __name__ == "__main__":
    from uvicorn import run # noqa

    run("main:app", host="127.0.0.1", port=5001, log_level="info", reload=True)
