from datetime import datetime
from typing import Iterable, List, Optional

from psycopg import Connection
from psycopg.rows import class_row, scalar_row

from heros.types.db.metereologico import MetereologicoData


def get_data(
    conn: Connection, start: Optional[datetime] = None, end: Optional[datetime] = None
) -> List[MetereologicoData]:
    with conn.cursor(row_factory=class_row(MetereologicoData)) as cur:
        cur.execute(
            """
        SELECT *
        FROM wxt530 ds
        WHERE
        ds.data BETWEEN
                    COALESCE(%s, to_timestamp(0)::date)
                    AND COALESCE(%s, CURRENT_TIMESTAMP)
        ORDER BY ds.data DESC;
        """,
            (start, end),
        )
        return cur.fetchall()


def last_timestamp(conn: Connection) -> Optional[datetime]:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute("""
        SELECT ds.data
        FROM wxt530 ds
        ORDER BY ds.data DESC
        LIMIT 1;
        """)
        return cur.fetchone()


def insert_update_data(conn: Connection, datas: Iterable[MetereologicoData]):
    with conn.cursor() as cur:
        cur.executemany(
            """
        INSERT INTO wxt530 as t
       (
            "data",
            "pressao_atmosferica",
            "temperatura",
            "umidade_ar",
            "precipitacao",
            "velocidade_vento",
            "direcao_vento",
            "bateria" 
       )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT ("data") DO UPDATE
        SET (
            "pressao_atmosferica",
            "temperatura",
            "umidade_ar",
            "precipitacao",
            "velocidade_vento",
            "direcao_vento",
            "bateria"
            ) =
        (
            COALESCE(EXCLUDED.pressao_atmosferica, t.pressao_atmosferica),
            COALESCE(EXCLUDED.temperatura, t.temperatura),
            COALESCE(EXCLUDED.umidade_ar, t.umidade_ar),
            COALESCE(EXCLUDED.precipitacao, t.precipitacao),
            COALESCE(EXCLUDED.velocidade_vento, t.velocidade_vento),
            COALESCE(EXCLUDED.direcao_vento, t.direcao_vento),
            COALESCE(EXCLUDED.bateria, t.bateria)
            );
        """,
            map(lambda d: d.model_dump(), datas),
        )
        conn.commit()
