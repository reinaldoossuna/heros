from fastapi import APIRouter

from heros.api import linigrafos, metereologico, location

api_router = APIRouter()
api_router.include_router(linigrafos.router)
api_router.include_router(metereologico.router)
api_router.include_router(location.router)


@api_router.get("/healty", status_code=200)
def healty():
    return "Ok"
