#!/usr/bin/env /home/nardo/projects/hydronet/.venv/bin/python3
#
from aiohttp import web
import logging
from dotenv import load_dotenv

import heros.api.linigrafos as linigrafos
import heros.api.metereologico as met
from heros.db_access.sql import init_db
from heros.logging import setup_logging
import heros.config as cfg

load_dotenv()


LOGGER = logging.getLogger(__name__)


def create_app():
    app = web.Application()

    app["noaa_cfg"] = cfg.noaa_config()
    app["spi_config"] = cfg.spi_config()
    app.cleanup_ctx.append(init_db)

    app.add_routes(
        [
            web.get("/metereologico", met.get_data),
            web.get("/metereologico/update", met.update_sensores),
            # web.get("/met/canlogin", met.update_sensores),
            # web.get("/met/updatepassword", met.update_password),
            web.get("/linigrafos", linigrafos.get_data),
            web.get("/linigrafos/update", linigrafos.update_sensores),
            web.get("/linigrafos/last_update", linigrafos.last_update),
            web.get("/linigrafos/update_location", linigrafos.update_location),
        ]
    )

    return app


if __name__ == "__main__":
    setup_logging()
    LOGGER.info("Starting server ...")
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8000)
