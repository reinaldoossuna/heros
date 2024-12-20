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
