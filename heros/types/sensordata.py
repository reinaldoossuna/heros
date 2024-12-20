from datetime import datetime
from typing import List

from pydantic import BaseModel, TypeAdapter, model_serializer


class SensorData(BaseModel):
    """
    Sensor data how is send from eng.
    """

    mac: str
    canal: int
    valor_leitura: float
    data_leitura: datetime
    sub_id_disp: str

    @model_serializer
    def ser_model(self) -> tuple:
        return (self.mac, self.canal, self.valor_leitura, self.data_leitura, self.sub_id_disp)


sensors_data_list = TypeAdapter(List[SensorData])

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
