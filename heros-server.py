#!/usr/bin/env /home/nardo/projects/hydronet/.venv/bin/python3
#
from aiohttp import web
from dotenv import load_dotenv

import heros.api.sensores as sensores
import heros.api.met as met
from heros.db_access.sql import init_db
import heros.config as cfg

load_dotenv()


def create_app():
    app = web.Application()

    app["noaa_cfg"] = cfg.noaa_config()
    app["spi_config"] = cfg.spi_config()
    app.cleanup_ctx.append(init_db)

    app.add_routes(
        [
            web.get("/met", met.get_data),
            web.get("/met/update", met.update_sensores),
            # web.get("/met/canlogin", met.update_sensores),
            # web.get("/met/updatepassword", met.update_password),
            web.get("/sensores", sensores.get_data),
            web.get("/sensores/update", sensores.update_sensores),
            web.get("/sensores/last_update", sensores.last_update),
            web.get("/sensores/update_location", sensores.update_location),
        ]
    )

    return app


if __name__ == "__main__":
    app = create_app()
    web.run_app(app)
