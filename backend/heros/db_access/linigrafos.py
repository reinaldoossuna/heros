from datetime import datetime
from typing import Iterable, List, Optional

from psycopg import Connection
from psycopg.rows import class_row

from heros.types.db.linigrafos import (
    LinigrafoData,
    LinigrafoLastUpdate,
)
from heros.types.engtec import SensorData


def get_data(
    conn: Connection, start: Optional[datetime] = None, end: Optional[datetime] = None
) -> List[LinigrafoData]:
    with conn.cursor(row_factory=class_row(LinigrafoData)) as cur:
        cur.execute(
            """
        SELECT data_leitura, mac, valor_leitura, sub_id_disp as local
        FROM linigrafos ds
        WHERE
        ds.data_leitura BETWEEN
                    COALESCE(%s, to_timestamp(0)::date)
                    AND COALESCE(%s, CURRENT_TIMESTAMP)
        ORDER BY ds.mac, ds.data_leitura ASC;
        """,
            (start, end),
        )
        return cur.fetchall()


def get_local_data(
    conn: Connection,
    local: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> List[LinigrafoData]:
    with conn.cursor(row_factory=class_row(LinigrafoData)) as cur:
        cur.execute(
            """
        SELECT data_leitura, mac, valor_leitura, sub_id_disp as local
        FROM linigrafos ds
        WHERE
        sub_id_disp = %s AND
        ds.data_leitura BETWEEN
                    COALESCE(%s, to_timestamp(0)::date)
                    AND COALESCE(%s, CURRENT_TIMESTAMP)
        ORDER BY ds.data_leitura ASC;
        """,
            (local, start, end),
        )
        return cur.fetchall()


def get_sensors_lastupdate(conn) -> List[LinigrafoLastUpdate]:
    with conn.cursor(row_factory=class_row(LinigrafoLastUpdate)) as cur:
        cur.execute("""
        SELECT mac,  max(data_leitura) AS data
        FROM linigrafos
        GROUP BY mac;
        """)
        return cur.fetchall()


def insert_data(conn: Connection, datas: Iterable[SensorData]):
    with conn.cursor() as cur:
        cur.executemany(
            """
        INSERT INTO linigrafos
               ( "mac",    "canal",  "valor_leitura",   "data_leitura",   "sub_id_disp")
        VALUES (%(mac)s, %(canal)s, %(valor_leitura)s, %(data_leitura)s, %(sub_id_disp)s)
        ON CONFLICT ("mac", "data_leitura") DO NOTHING;
        """,
            map(lambda d: d.model_dump(), datas),
        )
        conn.commit()
