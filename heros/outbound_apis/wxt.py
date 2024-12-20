import json
import logging
import re
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field, asdict

import aiohttp

NOAA_URL = "https://dcs1.noaa.gov/"
LOGIN_URL = NOAA_URL + "ACCOUNT/Login"
LOGOUT_URL = NOAA_URL + "ACCOUNT/SIGNOUT"
FIELD_TEST = NOAA_URL + "Account/FieldTest"
MESSAGES_URL = NOAA_URL + "Messages/"

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8",
}


LOGGER = logging.getLogger(__name__)


class Columns(Enum):
    CAR_TIME = "TblDcpDataDtMsgCar"
    DATA = "TblDcpDataData"


@dataclass
class RequestsFields:
    StartDt: datetime
    EndDt: datetime = field(default_factory=datetime.today)
    DcpAddr: str = "B2F00066"
    HoursDt: int = 0

    def __post_init__(self):
        if isinstance(self.StartDt, str):
            self.StartDt = datetime.strptime(self.StartDt, "%d/%m/%Y")
        self.StartDt = self.StartDt.strftime("%m/%d/%Y")
        self.EndDt = self.EndDt.strftime("%m/%d/%Y")


async def request_data(requests: RequestsFields, login: str, password: str):
    payload = asdict(requests)
    payload.update({"Username": login, "Password": password})

    async with aiohttp.ClientSession() as session:
        async with session.post(FIELD_TEST, data=payload) as r:
            resp = await r.json()
            return resp["msgs"]


async def login(username: str, password: str):
    session = aiohttp.ClientSession()

    r = await session.get(LOGIN_URL)
    payload = {
        "__RequestVerificationToken": r.cookies["__RequestVerificationToken"],
        "UserName": username,
        "Password": password,
    }
    async with session.post(LOGIN_URL, data=payload) as r:
        if r.ok:
            return session
        else:
            r.reason()


def parse_date(date_str: str) -> datetime:
    """
    Parse str to datatime.

    Args:
    date_str: str

    date_str is suppossed to be like "/Date(1734102240307)/"
    and the number inside is suppose to be a posix time
    """
    posix_time = int(re.search(r"\d{10}", date_str).group(0))
    return datetime.utcfromtimestamp(posix_time)


def parse_list(list_str: str):
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


columns = [
    "Data",
    "Pressão atmosférica (bar)",
    "Temperatura do ar (°C)",
    "Umidade relativa do ar (%)",
    "Precipitação (mm)",
    "Velocidade do vento (m/s)",
    "Direção do vento (˚)",
    "Bateria (v)",
]


def parse_one_json(json_resp: dict):
    deltas = [timedelta(hours=-2), timedelta(hours=-1), timedelta(hours=0)]
    date = parse_date(json_resp[Columns.CAR_TIME.value])
    dates = [date + delta for delta in deltas]

    lists_data = parse_list(json_resp[Columns.DATA.value])
    lists_w_date = [[d] + list for d, list in zip(dates, lists_data, strict=False)]
    return list(map(lambda list: tuple(list), lists_w_date))
