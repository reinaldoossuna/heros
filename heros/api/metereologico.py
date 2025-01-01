from datetime import datetime
from itertools import chain
from typing import List

from fastapi import APIRouter, HTTPException

import heros.db_access.meterologico as met
import heros.outbound_apis.noaa as noaa
from heros.config import settings
from heros.db_access import pool
from heros.types.db.metereologico import MetereologicoData

router = APIRouter(prefix="/meterologico", tags=["meterologico"])


@router.get("/")
def get_data(start: datetime | None = None, end: datetime | None = None) -> List[MetereologicoData]:
    with pool.connection() as conn:
        data = met.get_data(conn, start, end)
        return data


@router.get("/update")
def update_data():
    config = settings.noaa

    with pool.connection() as conn:
        last_day = met.last_timestamp(conn)
        last_day = last_day if last_day is not None else datetime.fromtimestamp(0)

    noaamsgs = noaa.request_data(config.user, config.password, start_date=last_day)
    if noaamsgs is None:
        return HTTPException(
            status_code=400,
            detail="Failed to get data from NOAA api",
        )

    datas = chain.from_iterable(map(lambda m: m.model_dump(), noaamsgs))

    with pool.connection() as conn:
        met.insert_update_data(conn, datas)


@router.get("/can_login")
def can_login():
    config = settings.noaa
    s = noaa.login(config.user, config.password)

    if s is None:
        return HTTPException(
            status_code=400,
            detail="Failed to login",
        )
    s.close()
