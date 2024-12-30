from datetime import datetime
from itertools import chain

from aiohttp import web

import heros.db_access.sql as sql
import heros.outbound_apis.noaa as noaa


async def get_data(request):
    pool = request.app["pool"]
    start = request.rel_url.query.get("start", None)
    end = request.rel_url.query.get("end", None)

    start = datetime.strptime(start, "%d%m%Y") if start else None
    end = datetime.strptime(end, "%d%m%Y") if end else None
    async with pool.acquire() as conn:
        data = await sql.get_met_data(conn, start, end)
        dicts = [d.model_dump_json() for d in data]
        return web.json_response(dicts)


def to_tuple(d: dict):
    return tuple(d.values())


async def update_sensores(request):
    config = request.app["noaa_cfg"]
    pool = request.app["pool"]

    conn = await pool.acquire()
    last_day = await sql.last_day_met(conn)

    noaamsgs = await noaa.request_data(config.user, config.password, start_date=last_day)
    datas = chain.from_iterable(map(lambda m: m.model_dump(), noaamsgs))

    await sql.insert_wxtdata(conn, datas)
    await conn.close()

    return web.Response()


async def can_login(request: web.Request) -> web.Response:
    config = request.app["noaa_cfg"]
    s = await noaa.login(config["user"], config["password"])

    if s is not None:
        return web.Response(text="Login successful")

    return web.Response(status=403, text="Failed to login")
