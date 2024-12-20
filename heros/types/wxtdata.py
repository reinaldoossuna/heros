from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, TypeAdapter, Field


class ListData(BaseModel):
    fixed_size: list[float] = Field(min_length=7, max_length=7)


class MetDataDB(BaseModel):
    data: datetime = Field(alias="Data")
    pressao_atmosferica: Optional[float] = Field(alias="Pressão atmosférica (bar)")
    temperatura_do_ar: Optional[float] = Field(alias="Temperatura do ar (°C)")
    umidade_relativa_do_ar: Optional[float] = Field(
        alias="Umidade relativa do ar (%)",
    )
    precipitacao: Optional[float] = Field(
        alias="Precipitação (mm)",
    )
    velocidade_do_vento: Optional[float] = Field(
        alias="Velocidade do vento (m/s)",
    )
    direcao_do_vento: Optional[float] = Field(
        alias="Direção do vento (˚)",
    )
    bateria: Optional[float] = Field(
        alias="Bateria (v)",
    )


metdatadb_list = TypeAdapter(List[MetDataDB])
