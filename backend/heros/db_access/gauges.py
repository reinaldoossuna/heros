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


query_station_data = sql.SQL(
    """
WITH shifted_table AS (
    SELECT
        "time",
        {station} as raw,
        LAG({station}, 1, 0) OVER (ORDER BY "time") AS shifted
    FROM {table}
    WHERE
    time >= COALESCE({start}, to_timestamp(0)::date) AND
    time < COALESCE({end}, CURRENT_TIMESTAMP)
)
SELECT
    "time",
    CASE WHEN raw >= shifted THEN raw - shifted ELSE raw END AS data
FROM shifted_table
ORDER BY "time";
                """
)


def get_station_data(
    conn: Connection, station: str, start: Optional[datetime] = None, end: Optional[datetime] = None
):
    with conn.cursor(row_factory=class_row(GaugeData)) as cur:
        cur.execute(
            query_station_data.format(
                table=sql.Identifier("pluviometros_processados"),
                station=sql.Identifier(station),
                start=start,
                end=end,
            ),
        )
        return cur.fetchall()


def get_acc_station_data(
    conn: Connection,
    station: str,
    interval: Interval,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
):
    with conn.cursor(row_factory=class_row(GaugeData)) as cur:
        cur.execute(
            sql.SQL(
                """
WITH shifted_table AS (
    SELECT
        "time",
        {station} as raw,
        LAG({station}, 1, 0) OVER (ORDER BY "time") AS shifted
    FROM {table}
    WHERE
    time >= COALESCE({start}, to_timestamp(0)::date) AND
    time < COALESCE({end}, CURRENT_TIMESTAMP)
),
                discrete_table AS (
SELECT
    "time",
    CASE WHEN raw >= shifted THEN raw - shifted ELSE raw END AS discrete
FROM shifted_table
ORDER BY "time"
),
                temp as (
    SELECT time_bucket({interval}, time) AS bucket,
                    sum(discrete) AS data
    FROM discrete_table
    GROUP BY bucket
    ORDER BY bucket ASC)

SELECT bucket as time, data
FROM temp;
        """
            ).format(
                table=sql.Identifier("pluviometros_processados"),
                station=sql.Identifier(station),
                interval=interval.get(),
                start=start,
                end=end,
            ),
        )
        return cur.fetchall()
