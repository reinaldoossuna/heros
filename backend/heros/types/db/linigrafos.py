from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class LinigrafoData(BaseModel):
    """
    Sensor in the db.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

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
