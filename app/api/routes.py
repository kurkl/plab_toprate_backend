from fastapi import APIRouter

from app.api.endpoints import system, topics

api_router = APIRouter()


api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(topics.router, prefix="/plab", tags=["plab"])
