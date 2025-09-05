import heros.db_access.meterologico as met
from heros.report.period import Period
from heros.db_access import pool


def get_data(period: Period):
    with pool.connection() as conn:
        data = met.get_data(conn, period.begin, period.end)

    df = pd.DataFrame(data)

    # set data columns as datetime
    df.data = pd.to_datetime(df.data, utc=True)
    df = df.set_index("data")
    return df
