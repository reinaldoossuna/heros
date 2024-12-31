import uvicorn
from fastapi import FastAPI

from heros.api.main import api_router
from heros.config import settings
from heros.logging import LOGGER, setup_logging

setup_logging()

app = FastAPI(title="Heros", openapi_url="/api/openapi.json")

app.include_router(api_router, prefix="/api")


def main_server():
    LOGGER.info("Starting server")
    uvicorn.run(app, port=settings.port, log_level="info")
