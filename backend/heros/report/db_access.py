from datetime import datetime
from dateutil.relativedelta import relativedelta
from psycopg.connection import Connection

import heros.db_access.meterologico as met
from heros.report.period import Period
from heros.db_access import pool
from heros.report.period import start_of_month


def month_stats(conn: Connection, month: datetime):
    values = dict(begin=start_of_month(month), end=start_of_month(month) + relativedelta(months=1))
    with conn.cursor() as cur:
        cur.execute(
            """
            with period AS (
                SELECT *
                FROM met_daily
                WHERE day >= %(begin)s AND day < %(end)s
            )
            SELECT min(temp_min),
                max(temp_max),
                sum(precip_total),
                (SELECT count(*)
                FROM period
                WHERE precip_total = 0) as days_wo_rain
            FROM period;
            """,
            values,
        )
        return cur.fetchone()


def month_precipitation(conn: Connection, month: datetime):
    values = dict(begin=start_of_month(month), end=start_of_month(month) + relativedelta(months=1))

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT precip_total
            FROM met_daily
            WHERE day >= %(begin)s AND day < %(end)s;
            """,
            values,
        )
        return cur.fetchall()


def period_temp(conn: Connection, month: datetime, period_months: int = 5):
    values = dict(
        begin=start_of_month(month) + relativedelta(months=-period_months),
        end=start_of_month(month) + relativedelta(months=-1),
    )

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT temp_min, temp_avg, temp_max
            FROM met_daily
            WHERE day >= %(begin)s AND day < %(end)s;
            """,
            values,
        )
        return cur.fetchall()
