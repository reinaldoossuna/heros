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


async def insert_wxtdata(conn, data):
    await conn.executemany(
        """
insert
    into
    hydronet.public.dados_met as t
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
values ($1,$2,$3,$4,$5,$6,$7,$8)
on
conflict ("Data")
do
update
set
    (
    "Pressão atmosférica (bar)",
    "Temperatura do ar (°C)",
    "Umidade relativa do ar (%)",
    "Precipitação (mm)",
    "Velocidade do vento (m/s)",
    "Direção do vento (˚)",
    "Bateria (v)"
) =
    (coalesce(EXCLUDED."Pressão atmosférica (bar)",
    t."Pressão atmosférica (bar)"),
    coalesce(EXCLUDED."Temperatura do ar (°C)",
    t."Temperatura do ar (°C)"),
    coalesce(EXCLUDED."Umidade relativa do ar (%)",
    t."Umidade relativa do ar (%)"),
    coalesce(EXCLUDED."Precipitação (mm)",
    t."Precipitação (mm)"),
    coalesce(EXCLUDED."Velocidade do vento (m/s)",
    t."Velocidade do vento (m/s)"),
    coalesce(EXCLUDED."Direção do vento (˚)",
    t."Direção do vento (˚)"),
    coalesce(EXCLUDED."Bateria (v)",
    t."Bateria (v)"));
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
