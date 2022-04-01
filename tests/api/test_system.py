import httpx
import respx
import pytest
from httpx import Response, AsyncClient
from fastapi import FastAPI, status


@pytest.mark.parametrize("route_name", ("system:health", "system:health-redis"))
async def test_healthcheck_services(app: FastAPI, client: AsyncClient, route_name: str):
    response = await client.get(app.url_path_for(route_name))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "alive"}


@pytest.mark.parametrize("route_name", ("system:health", "system:health-redis"))
async def test_healthcheck_services_unavailable(
    app: FastAPI, client: AsyncClient, mocked_api, route_name: str
):
    route = mocked_api.get(app.url_path_for(route_name)).mock(return_value=Response(500))
    response = await client.get(app.url_path_for(route_name))

    assert route.called
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
