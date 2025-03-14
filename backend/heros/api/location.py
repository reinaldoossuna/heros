from typing import List
from fastapi import APIRouter
from psycopg.rows import class_row

from heros.db_access import pool
from heros.types.db.location import LocationData

router = APIRouter(prefix="/location", tags=["locations"])


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
