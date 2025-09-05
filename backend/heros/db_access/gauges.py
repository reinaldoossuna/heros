from datetime import datetime
from typing import Iterable, List, Optional, Tuple

from psycopg import Connection, sql
from psycopg.rows import class_row, scalar_row

from heros.types.db.gauges import GaugeData
from heros.types.db.linigrafos import Interval


def table_exists(conn: Connection, station: str):
    with conn.cursor(row_factory=scalar_row) as cur:
        cur.execute(
            """
            SELECT EXISTS (
   SELECT FROM pg_tables
   WHERE  schemaname = 'public'
   AND    tablename  = %s
   );
            """,
            (station,),
        )
        return cur.fetchone()


def get_station_data(
    conn: Connection, station: str, start: Optional[datetime] = None, end: Optional[datetime] = None
):
    with conn.cursor(row_factory=class_row(GaugeData)) as cur:
        cur.execute(
            sql.SQL(
                """
SELECT time, {column} as data
FROM gauges g
WHERE time BETWEEN
    COALESCE({start}, to_timestamp(0)::date)
    AND COALESCE({end}, CURRENT_TIMESTAMP)
    AND {column} IS NOT NULL;
        """
            ).format(column=sql.Identifier(station), start=start, end=end),
        )
        return cur.fetchall()


def get_acc_station_data(
        conn: Connection, station: str, interval: Interval, start: Optional[datetime] = None, end: Optional[datetime] = None
):
    with conn.cursor(row_factory=class_row(GaugeData)) as cur:
        cur.execute(
            sql.SQL(
                """
WITH temp as (
    SELECT time_bucket({interval}, time) AS bucket,
                    sum({station}) AS data
    FROM gauges g
    WHERE time BETWEEN
        COALESCE({start}, to_timestamp(0)::date)
        AND COALESCE({end}, CURRENT_TIMESTAMP)
        AND {station} IS NOT NULL
    GROUP BY bucket
    ORDER BY bucket ASC)

SELECT bucket as time, data
FROM temp;
        """
            ).format(station=sql.Identifier(station),interval=interval.get(), start=start, end=end),
        )
        return cur.fetchall()
