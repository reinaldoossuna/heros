from typing import List
from fastapi import APIRouter
from psycopg.rows import class_row

from heros.db_access import pool
from heros.db_access import locations
from heros.types.db.location import LocationData, Location

router = APIRouter(prefix="/location", tags=["locations"])


@router.get("/v2")
def get_locationsv2() -> List[Location]:
    with pool.connection() as conn:
        return locations(conn)


@router.get("/")
def get_locations() -> List[LocationData]:
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(LocationData)) as cur:
            cur.execute(
                """
                SELECT nome , latitude, longitude
                FROM posicoes;
                """
            )
            return cur.fetchall()
