from typing import Any, List
from datetime import datetime, timedelta
import re

from pydantic import ValidationError


from heros.types.db.metereologico import MetereologicoData


def parse_date(date_str: str) -> datetime:
    """
    Parse str to datatime.

    Args:
    date_str: str

    date_str is suppossed to be like "/Date(1734102240307)/"
    and the number inside is suppose to be a posix time
    """
    match = re.search(r"\d{10}", date_str)
    if match is None:
        raise ValidationError(f"{date_str} cannot be parsed")

    posix_time = int(match.group(0))
    dt = datetime.fromtimestamp(posix_time)
    dt = dt.replace(minute=0, second=0)
    return dt


def parse_clean_data(list_str: str):
    # separate the 3 data list
    lists = list_str.split("\r\n")
    # filter out anything but numbers
    num_re = re.compile(r"(\d+(?:\.\d*)?)")
    dirty_lists = map(lambda l: num_re.findall(l), lists)
    # filter any list with size less than 7
    str_lists = filter(lambda l: len(l) == 7, dirty_lists)
    # cast to float
    data_lists = map(lambda l: list(map(float, l)), str_lists)
    return list(data_lists)


def list2dict(keys, values, strict=True):
    return dict(zip(keys, values, strict=strict))


def ensure_datetime(value: Any):
    if not isinstance(value, datetime):
        return datetime.strptime(value, "%d/%m/%Y")
    else:
        return value


def metdatadb_from(date: datetime, lists_data: List[List[float]]) -> List[MetereologicoData]:
    # keys = [field.alias for _, field in MetereologicoData.__pydantic_fields__.items()]
    keys = [
        "Data",
        "Pressão atmosférica (bar)",
        "Temperatura do ar (°C)",
        "Umidade relativa do ar (%)",
        "Precipitação (mm)",
        "Velocidade do vento (m/s)",
        "Direção do vento (˚)",
        "Bateria (v)",
    ]
    deltas = [timedelta(hours=-2), timedelta(hours=-1), timedelta(hours=0)]

    dates = [date + delta for delta in deltas]
    lists_w_date = [[d] + list for d, list in zip(dates, lists_data, strict=False)]
    list_dicts = [list2dict(keys, l) for l in lists_w_date]
    return [MetereologicoData(**dic) for dic in list_dicts]
