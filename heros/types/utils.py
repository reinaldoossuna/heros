from typing import Any
from datetime import datetime
import re


def parse_date(date_str: str) -> datetime:
    """
    Parse str to datatime.

    Args:
    date_str: str

    date_str is suppossed to be like "/Date(1734102240307)/"
    and the number inside is suppose to be a posix time
    """
    posix_time = int(re.search(r"\d{10}", date_str).group(0))
    dt = datetime.utcfromtimestamp(posix_time)
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