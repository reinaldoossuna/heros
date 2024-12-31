from aiohttp import web
from datetime import datetime

from heros.logging import LOGGER
from heros.config import settings
from heros.db_access import pool
import heros.db_access.linigrafos as lini
import heros.outbound_apis.engtec as engtec


async def get_data(request: web.Request):
    start = request.rel_url.query.get("start", None)
    end = request.rel_url.query.get("end", None)

    start = datetime.strptime(start, "%d%m%Y") if start else None
    end = datetime.strptime(end, "%d%m%Y") if end else None
    LOGGER.info("Requesting data from db")
    LOGGER.info(f"start: {start}")
    LOGGER.info(f"end: {end}")

    with pool.connection() as conn:
        data = lini.get_data(conn, start, end)
        dumped = [d.model_dump_json() for d in data]
        return web.json_response(dumped)


async def update_sensores(request) -> web.Response:
    datas = engtec.request_data(settings.engtec)
    if datas is None:
        return web.Response(
            status=400,
            text="Failed to get data from Engtec api",
        )

    with pool.connection() as conn:
        lini.insert_data(conn, datas)
    return web.Response()


async def sensors_lastupdate(request):
    with pool.connection() as conn:
        data = lini.get_sensors_lastupdate(conn)
        dumped = [d.model_dump_json() for d in data]
        return web.json_response(dumped)


async def update_location(request):
    raise NotImplementedError
