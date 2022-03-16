import asyncio
from typing import Generator, AsyncGenerator

import pytest
from httpx import AsyncClient
from fastapi import FastAPI


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """
    Create an instance of the default event loop for each test case
    :param request:
    :return:
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def app() -> FastAPI:
    from src.main import app

    return app


@pytest.fixture(scope="module")
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        app=app, base_url="http://test", headers={"Content-Type": "application/json"}
    ) as client:
        yield client
