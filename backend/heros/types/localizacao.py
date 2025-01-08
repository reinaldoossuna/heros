from pydantic import BaseModel, BeforeValidator
from typing_extensions import Annotated

posicoes = [
    "soter",
    "hemosul",
    "rq30",
    "segredo",
    "segredo2",
    "bandeira",
]


sensores = [
    "94B55517E330",
    "94B55517E358",
    "94B55517E350",
    "94B555196BF8",
    "94B555196D24",
    "94B55536BB20",
    "94B55536BAB0",
    "94B555195254",
]


def is_in(list):
    return lambda val: val if val in list else 0


class SensorLocalizacao(BaseModel):
    p_name: Annotated[str, BeforeValidator(is_in(posicoes))]
    s_mac: Annotated[str, BeforeValidator(is_in(sensores))]
