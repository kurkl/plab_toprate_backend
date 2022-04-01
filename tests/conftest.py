import asyncio
from typing import Generator, AsyncGenerator

import respx
import pytest
from httpx import AsyncClient
from fastapi import FastAPI

from app.core.events import connect_to_redis, disconnect_from_redis


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


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_app

    app = get_app()
    return app


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    await connect_to_redis()
    yield app
    await disconnect_from_redis()


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
async def mocked_api(client: AsyncGenerator):
    async with respx.mock(base_url="http://test") as respx_mock:
        yield respx_mock
