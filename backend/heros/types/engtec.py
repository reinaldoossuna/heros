from datetime import datetime
from typing import List

from pydantic import BaseModel, TypeAdapter


class SensorData(BaseModel):
    """
    Sensor data how is send from eng.
    """

    mac: str
    canal: int
    valor_leitura: float
    data_leitura: datetime
    sub_id_disp: str



sensors_data_list = TypeAdapter(List[SensorData])
