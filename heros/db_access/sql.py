import asyncio
import asyncpg

DSN = "postgresql://{user}:{password}@{host}/{database}"


def get_url(config):
    return DSN.format(
        user=config["DB_USER"],
        password=config["DB_PASSWORD"],
        database=config["DB_DATABASE"],
        host=config["DB_HOST"],
    )


async def init_db(app):
    config = app["config"]
    dsn = get_url(config)
    app["pool"] = await asyncpg.create_pool(dsn)
    yield
    await app["pool"].close()


async def copy_sensordata_to_table(conn, data):
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
