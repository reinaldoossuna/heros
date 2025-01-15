from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class LinigrafoData(BaseModel):
    """
    Sensor in the db.
    """

    data_leitura: datetime
    mac: str
    local: Optional[str]
    valor_leitura: float


class LinigrafoLastUpdate(BaseModel):
    """
    Sensor in the db.
    """

    mac: str
    data: datetime
