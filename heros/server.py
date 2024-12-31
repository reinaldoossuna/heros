from aiohttp import web
import logging
from dotenv import load_dotenv

import heros.api.linigrafos as linigrafos
import heros.api.metereologico as met
from heros.logging import setup_logging
from heros.config import settings

load_dotenv()


LOGGER = logging.getLogger(__name__)


def create_app():
    app = web.Application()

    app.add_routes(
        [
            web.get("/metereologico", met.get_data),
            web.get("/metereologico/update", met.update_sensores),
            web.get("/metereologico/can_login", met.can_login),
            # web.get("/met/updatepassword", met.update_password),
            web.get("/linigrafos", linigrafos.get_data),
            web.get("/linigrafos/update", linigrafos.update_sensores),
            web.get("/linigrafos/sensors/lastupdate", linigrafos.sensors_lastupdate),
            web.get("/linigrafos/update_location", linigrafos.update_location),
        ]
    )

    return app


def main_server():
    setup_logging()
    LOGGER.info("Starting server ...")
    app = create_app()
    web.run_app(app, port=settings.port)


if __name__ == "__main__":
    main_server()
