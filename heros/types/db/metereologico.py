from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    model_serializer,
)


class MetereologicoData(BaseModel):
    data: datetime
    pressao_atmosferica: Optional[float]
    temperatura: Optional[float]
    umidade_ar: Optional[float]
    precipitacao: Optional[float]
    velocidade_vento: Optional[float]
    direcao_vento: Optional[float]
    bateria: Optional[float]

    @model_serializer
    def ser_model(self) -> tuple:
        keys = MetereologicoData.__pydantic_fields__.keys()
        values = [self.__getattribute__(key) for key in keys]
        return tuple(values)
