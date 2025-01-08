from pydantic import BaseModel, ConfigDict


class LocationData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str
    latitude: float
    longitude: float
