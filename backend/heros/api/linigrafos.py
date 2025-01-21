from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException

from heros.db_access import date_lastupdate
import heros.db_access.linigrafos as lini
import heros.outbound_apis.engtec as engtec
from heros.config import settings
from heros.db_access import pool
from heros.logging import LOGGER
from heros.types.db.linigrafos import Interval, LinigrafoAvgData, LinigrafoData, LinigrafoLastUpdate

router = APIRouter(prefix="/linigrafos", tags=["linigrafos"])


@router.get("/")
def get_data(start: datetime | None = None, end: datetime | None = None) -> List[LinigrafoData]:
    LOGGER.info("Requesting data from db")
    LOGGER.info(f"start: {start}")
    LOGGER.info(f"end: {end}")

    with pool.connection() as conn:
        data = lini.get_data(conn, start, end)
        LOGGER.info("Sending data")
        return data


@router.get("/update")
def update_data():
    LOGGER.info("Updating linigrafos data")
    datas = engtec.request_data(settings.engtec)
    if datas is None:
        LOGGER.error("Updated failed")
        return HTTPException(
            status_code=400,
            detail="Failed to get data from Engtec api",
        )

    LOGGER.info("Sending new data to db")
    with pool.connection() as conn:
        lini.insert_data(conn, datas)
    LOGGER.info("Updated done")


@router.get("/update/last")
def last_update() -> Optional[datetime]:
    with pool.connection() as conn:
        return date_lastupdate(conn, "linigrafos")


@router.get("/lastupdate")
def sensors_lastupdate() -> List[LinigrafoLastUpdate]:
    LOGGER.info("Sensors lastupdate requested, getting data in db")
    with pool.connection() as conn:
        data = lini.get_sensors_lastupdate(conn)
        LOGGER.info("Sending data")
        return data

@router.get("/avg/{local}/{interval}")
def get_local_avg_data(local: str, interval: Interval = Interval.hourly, daysago: int = 1) -> List[LinigrafoAvgData]:
    with pool.connection() as conn:
        data = lini.get_avg_local_data(conn, local, interval, daysago)
        return data


@router.get("/{local}")
def get_local_data(
    local: str, start: datetime | None = None, end: datetime | None = None
) -> List[LinigrafoData]:
    LOGGER.info(f"Requesting {local} data from db")
    LOGGER.info(f"start: {start}")
    LOGGER.info(f"end: {end}")

    with pool.connection() as conn:
        data = lini.get_local_data(conn, local, start, end)
        LOGGER.info("Sending data")
        return data
