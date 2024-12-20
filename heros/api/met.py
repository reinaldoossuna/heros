import json
from itertools import chain

from aiohttp import web

import heros.db_access.sql as sql
import heros.outbound_apis.wxt as wxt


async def get_data(request):
    pool = request.app["pool"]
    async with pool.acquire() as conn:
        data = await sql.get_met_data(conn)
        dicts = [d.model_dump_json() for d in data]
        return web.json_response(dicts)


async def update_sensores(request):
    config = request.app["noaa_cfg"]
    pool = request.app["pool"]

    conn = await pool.acquire()
    last_day = await sql.last_day_met(conn)

    req = wxt.RequestsFields(StartDt=last_day)

    raw_jsons = await wxt.request_data(req, config["user"], config["password"])
    clean_json = map(wxt.parse_one_json, raw_jsons)

    await sql.insert_wxtdata(conn, chain.from_iterable(clean_json))
    await conn.close()

    return web.Response()
