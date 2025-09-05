import csv
from io import StringIO
from logging import debug
import tempfile
from datetime import datetime
import zipfile
from enum import StrEnum, auto
from pathlib import Path
from typing import Annotated, List, TypeVar
from fastapi import APIRouter, Body, Response
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from heros.db_access import pool

from heros.db_access.meterologico import get_data as weather_data
from heros.db_access.linigrafos import get_local_data as linigrafo_data
from heros.logging import LOGGER

router = APIRouter(prefix="/download", tags=["download"])


class DataType(StrEnum):
    weather = auto()
    linigrafo = auto()
    gauge = auto()


class Period(BaseModel):
    begin: datetime
    end: datetime


BaseModel_t = TypeVar("BaseModel_t", bound=BaseModel)


def basemodel_to_csv(data: List[BaseModel_t]):
    if len(data) == 0:
        return ""
    fieldnames = list(data[0].model_json_schema()["properties"].keys())

    with StringIO() as io:
        writer = csv.DictWriter(io, fieldnames=fieldnames)
        writer.writeheader()
        for row_data in data:
            writer.writerow(row_data.model_dump())
        return io.getvalue()


@router.post("/")
def download_data(
    dataType: Annotated[DataType, Body()],
    period: Annotated[Period, Body()],
    stations: Annotated[List[str], Body()],
):
    LOGGER.info(f"Request for {dataType} {stations} {period}")
    tmp = "data.zip"
    zip = zipfile.ZipFile(tmp, "w")
    LOGGER.info(f"Saving files to {tmp}")

    match dataType:
        case DataType.weather:
            with pool.connection() as conn:
                LOGGER.debug("Preparing data")

                data = weather_data(conn, start=period.begin, end=period.end)
                zip.writestr("weather.csv", basemodel_to_csv(data))

                LOGGER.debug(f"{zip.filelist}")
            LOGGER.debug("Sending data")

        case DataType.linigrafo:
            for station in stations:
                with pool.connection() as conn:
                    LOGGER.debug(f"Preparing data for {station}")
                    data = linigrafo_data(conn, stations, start=period.begin, end=period.end)
                    LOGGER.info(data)
                    if len(data) == 0:
                        LOGGER.info(f"{station} has no data")
                        continue
                    zip.writestr(f"{station}.csv", basemodel_to_csv(data))

        case DataType.gauge:
            response = FileResponse(
                "/home/nardo/projects/heros/backend/data.zip", media_type="application/zip"
            )

    zip.close()
    response = FileResponse(tmp, media_type="application/zip")
    return response
