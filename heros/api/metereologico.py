from itertools import chain
from datetime import datetime

from aiohttp import web

import heros.db_access.sql as sql
import heros.outbound_apis.noaa as noaa
from heros.types.noaa import RequestsFields


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

    req = RequestsFields(start_date=last_day)
    datas = await noaa.request_data(req, config["user"], config["password"])

    tuples = map(to_tuple, filter(lambda d: d is not None, chain.from_iterable(datas)))

    await sql.insert_wxtdata(conn, tuples)
    await conn.close()

    return web.Response()
