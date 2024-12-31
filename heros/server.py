from aiohttp import web
import logging
from dotenv import load_dotenv

import heros.api.linigrafos as linigrafos
import heros.api.metereologico as met
from heros.logging import setup_logging
import heros.config as cfg

load_dotenv()


LOGGER = logging.getLogger(__name__)


def create_app():
    app = web.Application()

    settings = cfg.Settings()
    app["settings"] = settings

    app.add_routes(
        [
            web.get("/metereologico", met.get_data),
            web.get("/metereologico/update", met.update_sensores),
            web.get("/metereologico/can_login", met.can_login),
            # web.get("/met/updatepassword", met.update_password),
            web.get("/linigrafos", linigrafos.get_data),
            web.get("/linigrafos/update", linigrafos.update_sensores),
            web.get("/linigrafos/last_update", linigrafos.last_update),
            web.get("/linigrafos/update_location", linigrafos.update_location),
        ]
    )

    return app


def main_server():
    setup_logging()
    LOGGER.info("Starting server ...")
    app = create_app()
    web.run_app(app, port=app["settings"].port)


if __name__ == "__main__":
    main_server()
