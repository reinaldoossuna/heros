import asyncpg

from heros.types.sensordata import sensors_datadb_list, sensors_lastupdate_list
from heros.types.wxtdata import metdatadb_list
from heros.config import database_url


async def init_db(app):
    dsn = database_url()
    app["pool"] = await asyncpg.create_pool(dsn)
    yield
    await app["pool"].close()


async def insert_sensordata(conn, data):
    tuples = [d.model_dump() for d in data]

    await conn.executemany(
        """
        INSERT INTO dados_sensores
               ("mac", "canal", "valor_leitura", "data_leitura", "sub_id_disp")
        VALUES ($1,         $2,              $3,             $4,           $5)
        ON CONFLICT ("mac", "data_leitura") DO NOTHING;
        """,
        tuples,
    )


# TODO: this is almost the same code as above
async def insert_wxtdata(conn, data):
    await conn.executemany(
        """
        INSERT INTO dados_met
               (
            "Data",
            "Pressão atmosférica (bar)",
            "Temperatura do ar (°C)",
            "Umidade relativa do ar (%)",
            "Precipitação (mm)",
            "Velocidade do vento (m/s)",
            "Direção do vento (˚)",
            "Bateria (v)"
        )
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8)
        ON CONFLICT ("Data") DO NOTHING;
        """,
        data,
    )


async def last_day_met(conn):
    r = await conn.fetchval(
        """
        select dm."Data"
        from hydronet.public.dados_met dm
        order by dm."Data" desc
        limit 1;
        """
    )
    return r


async def get_sensor_data(conn):
    async with conn.transaction():
        records = await conn.fetch("""
        SELECT data_leitura, mac, valor_leitura
        FROM hydronet.public.dados_sensores ds;
        """)
        data = sensors_datadb_list.validate_python(records)
        return data


async def get_lastupdate_sensors(conn):
    async with conn.transaction():
        records = await conn.fetch("""
        SELECT mac, data
        FROM hydronet.public.sensores_last_use;
        """)
        data = sensors_lastupdate_list.validate_python(records)
        return data


async def get_met_data(conn):
    async with conn.transaction():
        records = await conn.fetch("""
        SELECT *
        FROM hydronet.public.dados_met;
        """)
        data = metdatadb_list.validate_python(records)
        return data
