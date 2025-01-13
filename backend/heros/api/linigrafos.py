from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

from heros.db_access import date_lastupdate
import heros.db_access.linigrafos as lini
import heros.outbound_apis.engtec as engtec
from heros.config import settings
from heros.db_access import pool
from heros.logging import LOGGER
from heros.types.db.linigrafos import SensorDataDB, SensorLastUpdate

router = APIRouter(prefix="/linigrafos", tags=["linigrafos"])


@router.get("/")
def get_data(start: datetime | None = None, end: datetime | None = None) -> List[SensorDataDB]:
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
def last_update() -> datetime:
    with pool.connection() as conn:
        return date_lastupdate(conn, 'linigrafos')

@router.get("/lastupdate")
def sensors_lastupdate() -> List[SensorLastUpdate]:
    LOGGER.info("Sensors lastupdate requested, getting data in db")
    with pool.connection() as conn:
        data = lini.get_sensors_lastupdate(conn)
        LOGGER.info("Sending data")
        return data
