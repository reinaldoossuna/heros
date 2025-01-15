from datetime import datetime
import atexit
from typing import Optional

from psycopg import Connection
from psycopg.rows import scalar_row
from psycopg_pool import ConnectionPool

from heros.config import settings

pool = ConnectionPool(settings.pg_dsn.unicode_string())
atexit.register(pool.close)


def create_tables():
    with pool.connection() as con:
        con.execute(open("./migrations/create_tables.sql", "r").read())  # pyright: ignore
        con.commit()


def date_lastupdate(conn: Connection, table_name: str) -> Optional[datetime]:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            SELECT last_update
            FROM tables_infos
            WHERE table_name = %s
            """,
            (table_name,),
        )
        return cur.fetchone()
