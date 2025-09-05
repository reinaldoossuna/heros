from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException

import heros.db_access.gauges as gauges
from heros.db_access import pool
from heros.logging import LOGGER
from heros.types.db.gauges import GaugeData
from heros.types.db.linigrafos import Interval

router = APIRouter(prefix="/gauges", tags=["gauges"])


@router.get("/{station}")
def get_station_data(
    station: str, start: datetime | None = None, end: datetime | None = None
) -> List[GaugeData]:
    LOGGER.info(f"Requesting {station} data from db")
    LOGGER.info(f"start: {start}")
    LOGGER.info(f"end: {end}")

    with pool.connection() as conn:
        if not gauges.table_exists(conn, station):
            raise HTTPException(status_code=404, detail=f"table for {station} does not exists.")
        data = gauges.get_station_data(conn, station, start, end)
        LOGGER.info("Sending data")
        return data


@router.get("/daily/{station}")
def get_daily_station_data(
    station: str, start: datetime | None = None, end: datetime | None = None
) -> List[GaugeData]:
    LOGGER.info(f"Requesting {station} DAILY data from db")
    LOGGER.info(f"start: {start}")
    LOGGER.info(f"end: {end}")

    with pool.connection() as conn:
        if not gauges.table_exists(conn, station):
            raise HTTPException(status_code=404, detail=f"table for {station} does not exists.")
        data = gauges.get_acc_station_data(conn, station, Interval.daily, start, end)
        LOGGER.info("Sending data")
        return data
