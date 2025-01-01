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
        FROM hydronet.public.dados_met ds
        WHERE
        ds."DATA" BETWEEN
                    COALESCE(%s, to_timestamp(0)::date)
                    AND COALESCE(%s, CURRENT_TIMESTAMP);
        """,
            (start, end),
        )
        return cur.fetchall()


def last_timestamp(conn: Connection) -> Optional[datetime]:
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute("""
        SELECT dm."Data"
        FROM hydronet.public.dados_met dm
        ORDER BY dm."Data" DESC
        LIMIT 1;
        """)
        return cur.fetchone()


# TODO: Should recieve MetereologicoData
def insert_update_data(conn: Connection, datas: Iterable[tuple]):
    with conn.cursor() as cur:
        cur.executemany(
            """
        INSERT
        INTO
        hydronet.public.dados_met as t
       (
            "Data",
            "Pressão atmosférica (bar)",
            "Temperatura do ar (°C)",
            "Umidade relativa do ar (%%)",
            "Precipitação (mm)",
            "Velocidade do vento (m/s)",
            "Direção do vento (˚)",
            "Bateria (v)"
       )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON
        CONFLICT ("Data")
        DO
        UPDATE
        SET
            (
                "Pressão atmosférica (bar)",
                "Temperatura do ar (°C)",
                "Umidade relativa do ar (%%)",
                "Precipitação (mm)",
                "Velocidade do vento (m/s)",
                "Direção do vento (˚)",
                "Bateria (v)"
            ) =
        (COALESCE(EXCLUDED."Pressão atmosférica (bar)",
        t."Pressão atmosférica (bar)"),
        COALESCE(EXCLUDED."Temperatura do ar (°C)",
        t."Temperatura do ar (°C)"),
        COALESCE(EXCLUDED."Umidade relativa do ar (%%)",
        t."Umidade relativa do ar (%%)"),
        COALESCE(EXCLUDED."Precipitação (mm)",
        t."Precipitação (mm)"),
        COALESCE(EXCLUDED."Velocidade do vento (m/s)",
        t."Velocidade do vento (m/s)"),
        COALESCE(EXCLUDED."Direção do vento (˚)",
        t."Direção do vento (˚)"),
        COALESCE(EXCLUDED."Bateria (v)",
        t."Bateria (v)"));
        """,
            datas,
        )
        conn.commit()
