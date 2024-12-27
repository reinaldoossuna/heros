from aiohttp import web

import heros.outbound_apis.engtec as engtec
import heros.db_access.sql as sql
from heros.types.localizacao import SensorLocalizacao


# TODO: filter by date
async def get_data(request):
    pool = request.app["pool"]
    async with pool.acquire() as conn:
        data = await sql.get_sensor_data(conn)
        dicts = [d.model_dump_json() for d in data]
        return web.json_response(dicts)


async def update_sensores(request) -> web.Response:
    config = request.app["spi_config"]

    session = await engtec.login(config["user"], config["password"])
    if session is None:
        return web.Response(
            status=400,
            text="Failed to login",
        )

    data = await engtec.request_data(session)
    await session.close()

    pool = request.app["pool"]
    async with pool.acquire() as conn:
        await sql.insert_sensordata(conn, data)
    return web.Response()


async def last_update(request):
    pool = request.app["pool"]
    async with pool.acquire() as conn:
        data = await sql.get_lastupdate_sensors(conn)
        dumped = [d.model_dump_json() for d in data]
        return web.json_response(dumped)


async def update_location(request):
    pool = request.app["pool"]
    data = SensorLocalizacao(
        p_name=request.rel_url.query["local"], s_mac=request.rel_url.query["mac"]
    )
    async with pool.acquire() as conn:
        async with conn.transaction():
            # TODO: query
            await conn.execute(
                """
            INSERT INTO localizacao_sensores (p_name, s_mac)
            VALUES ($1, $2);
            """,
                data.p_name,
                data.s_mac,
            )
    return web.Response()
