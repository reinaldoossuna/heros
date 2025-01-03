from fastapi import APIRouter

from heros.api import linigrafos, metereologico

api_router = APIRouter()
api_router.include_router(linigrafos.router)
api_router.include_router(metereologico.router)
