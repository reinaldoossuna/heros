import atexit
from psycopg_pool import ConnectionPool
from heros.config import settings

pool = ConnectionPool(settings.pg_dsn.unicode_string())
atexit.register(pool.close)
