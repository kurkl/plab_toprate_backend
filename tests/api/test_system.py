from httpx import AsyncClient
from fastapi import FastAPI, status
import pytest


async def test_healthcheck_service(app: FastAPI, client: AsyncClient):
    response = await client.get(app.url_path_for("system:health"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "alive"}


@pytest.mark.skip
async def test_healthcheck_service_db(app: FastAPI, client: AsyncClient):
    response = await client.get(app.url_path_for("system:health-db"))

    assert response.status_code == status.HTTP_200_OK
    assert "alive" in response.json().keys()
