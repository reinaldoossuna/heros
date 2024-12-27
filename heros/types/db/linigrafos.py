from typing import List
from datetime import datetime
from pydantic import BaseModel, TypeAdapter

class SensorDataDB(BaseModel):
    """
    Sensor in the db.
    """
    data_leitura: datetime
    mac: str
    valor_leitura: float

sensors_datadb_list = TypeAdapter(List[SensorDataDB])


class SensorLastUpdate(BaseModel):
    """
    Sensor in the db.
    """
    mac: str
    data: datetime

sensors_lastupdate_list = TypeAdapter(List[SensorLastUpdate])
