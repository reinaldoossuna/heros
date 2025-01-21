from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, ConfigDict

class Interval(StrEnum):
    hourly= 'hourly'
    daily= 'daily'

    def get(self):
        match self:
            case Interval.hourly:
                return '1 hour'
            case Interval.daily:
                return '1 day'

class LinigrafoData(BaseModel):
    """
    Sensor in the db.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    data_leitura: datetime
    mac: str
    local: Optional[str]
    valor_leitura: float


class LinigrafoAvgData(BaseModel):
    """
    Avg Sensor in the db.
    """

    date: datetime
    avg_height: float


class LinigrafoLastUpdate(BaseModel):
    """
    Sensor in the db.
    """

    mac: str
    data: datetime
