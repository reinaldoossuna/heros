from datetime import datetime
from itertools import chain

from aiohttp import web

import heros.db_access.meterologico as met
import heros.outbound_apis.noaa as noaa
from heros.config import settings
from heros.db_access import pool


async def get_data(request):
    start = request.rel_url.query.get("start", None)
    end = request.rel_url.query.get("end", None)

    start = datetime.strptime(start, "%d%m%Y") if start else None
    end = datetime.strptime(end, "%d%m%Y") if end else None
    with pool.connection() as conn:
        data = met.get_data(conn, start, end)
        dicts = [d.model_dump_json() for d in data]
        return web.json_response(dicts)


async def update_sensores(request):
    config = settings.noaa

    with pool.connection() as conn:
        last_day = met.last_timestamp(conn)
        last_day = last_day if last_day is not None else datetime.fromtimestamp(0)

    noaamsgs = noaa.request_data(config.user, config.password, start_date=last_day)
    if noaamsgs is None:
        return web.Response(status=404, text="Failed to get data from noaa api")

    datas = chain.from_iterable(map(lambda m: m.model_dump(), noaamsgs))

    with pool.connection() as conn:
        met.insert_update_data(conn, datas)

    return web.Response()


async def can_login(request: web.Request) -> web.Response:
    config = settings.noaa
    s = noaa.login(config.user, config.password)

    if s is not None:
        return web.Response(text="Login successful")

    return web.Response(status=403, text="Failed to login")
