from fastapi import FastAPI
import uvicorn

from heros.logging import setup_logging, LOGGER
from heros.api.main import api_router
from heros.config import settings

setup_logging()

app = FastAPI(title="Heros", openapi_url="/api/openapi.json")

app.include_router(api_router, prefix="/api")

def main_server():
    LOGGER.info("Starting server")
    uvicorn.run(app, port=settings.port, log_level="info")
