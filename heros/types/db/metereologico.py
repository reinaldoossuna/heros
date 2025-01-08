from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
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
