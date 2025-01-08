from datetime import datetime
from typing import Iterable, List, Optional

from psycopg import Connection
from psycopg.rows import class_row

from heros.types.db.linigrafos import (
    SensorDataDB,
    SensorLastUpdate,
)
from heros.types.engtec import SensorData


def get_data(
    conn: Connection, start: Optional[datetime] = None, end: Optional[datetime] = None
) -> List[SensorDataDB]:
    with conn.cursor(row_factory=class_row(SensorDataDB)) as cur:
        cur.execute(
            """
        SELECT data_leitura, mac, valor_leitura
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


def get_sensors_lastupdate(conn) -> List[SensorLastUpdate]:
    with conn.cursor(row_factory=class_row(SensorLastUpdate)) as cur:
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
               ("mac", "canal", "valor_leitura", "data_leitura", "sub_id_disp")
        VALUES (%s,         %s,              %s,             %s,           NULLIF(%s, 'xxxxxxxxxx'))
        ON CONFLICT ("mac", "data_leitura") DO NOTHING;
        """,
            [data.model_dump() for data in datas],
        )
        conn.commit()
