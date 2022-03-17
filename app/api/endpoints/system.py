import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", name="system:health")
async def healthcheck_service():
    return {"status": "alive"}


@router.get("/health-db", name="system:health-db")
async def healthcheck_service_db():
    return {"skip": "ok"}
