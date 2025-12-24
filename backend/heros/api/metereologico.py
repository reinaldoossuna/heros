from datetime import date, datetime
from itertools import chain
from typing import List, Optional

from fastapi import APIRouter, HTTPException

import heros.db_access.meterologico as met
import heros.outbound_apis.noaa as noaa
from heros.config import settings
from heros.db_access import pool, date_lastupdate
from heros.db_access.credentials import get_credential
from heros.logging import LOGGER
from heros.types.db.metereologico import MetereologicoData

router = APIRouter(prefix="/metereologico", tags=["metereologico"])


@router.get("/")
def get_data(
    start: datetime | None = None, end: datetime | None = None
) -> List[MetereologicoData]:
    LOGGER.info("Requesting metereologico data from db")
    LOGGER.info(f"start: {start}")
    LOGGER.info(f"end: {end}")
    with pool.connection() as conn:
        data = met.get_data(conn, start, end)
        LOGGER.debug(f"Data: {data}")
        LOGGER.info("Sending data")
        return data


@router.get("/update")
def update_data():
    # Try to get credentials from database first, fallback to config
    db_config = get_credential("noaa")
    config = db_config if db_config is not None else settings.noaa

    with pool.connection() as conn:
        last_day = met.last_timestamp(conn)
        last_day = last_day if last_day is not None else datetime.fromtimestamp(0)

    noaamsgs = noaa.request_data(config.user, config.password, start_date=last_day)
    if noaamsgs is None:
        return HTTPException(
            status_code=400,
            detail="Failed to get data from NOAA api",
        )
    listlistdata = [msg.data for msg in noaamsgs]
    chained = chain.from_iterable(listlistdata)

    with pool.connection() as conn:
        met.insert_update_data(conn, chained)


@router.get("/update/last")
def last_update() -> Optional[datetime]:
    with pool.connection() as conn:
        return date_lastupdate(conn, "wxt530")


@router.get("/can_login")
def can_login() -> bool:
    # Try to get credentials from database first, fallback to config
    db_config = get_credential("noaa")
    config = db_config if db_config is not None else settings.noaa
    
    s = noaa.login(config.user, config.password)
    result = s is not None
    s.close() if result else None

    return result


@router.get("/days")
def get_data_days() -> List[date]:
    LOGGER.info("Requesting days with metereologico data")
    with pool.connection() as conn:
        days = met.get_data_days(conn)
        LOGGER.debug(f"Days: {days}")
        LOGGER.info("Sending days")
        return days
