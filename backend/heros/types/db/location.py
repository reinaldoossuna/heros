from pydantic import BaseModel, ConfigDict
from typing_extensions import Annotated
from pydantic import (
    BeforeValidator,
)

from enum import StrEnum, auto
from typing import List


class LocationData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str
    latitude: float
    longitude: float


class SensorType(StrEnum):
    linigrafo = auto()
    weather = auto()
    gauge = auto()


class SensorStatus(StrEnum):
    ok = auto()
    missing = auto()
    faulty = auto()
    no_signal = auto()
    maintenance = auto()
    error = auto()
    unknown = auto()

def aliaslist_to_str(v: List[str]) -> str:
        return v[0]

class Location(BaseModel):
    alias: Annotated[str, BeforeValidator(aliaslist_to_str)]
    sensor: SensorType
    status: SensorStatus
    latitude: float
    longitude: float
