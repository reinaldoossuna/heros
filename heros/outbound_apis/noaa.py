import requests
from datetime import datetime
import logging
from typing import List, Optional

from yarl import URL

import aiohttp
from heros.types.noaa import MsgNOAA, RequestsFields, msgsnoaa_list

NOAA_URL = "https://dcs1.noaa.gov/"
LOGIN_URL = NOAA_URL + "ACCOUNT/Login"
FIELD_TEST = NOAA_URL + "Account/FieldTest"


LOGGER = logging.getLogger(__name__)


def request_data(
    login: str, password: str, *, start_date: datetime, end_date: Optional[datetime] = None
) -> Optional[List[MsgNOAA]]:
    end_date = datetime.today() if end_date is None else end_date
    payload = RequestsFields(
        start_date=start_date, end_date=end_date, user=login, password=password
    )

    with requests.Session() as session:
        with session.post(FIELD_TEST, data=payload.model_dump(by_alias=True)) as r:
            resp = r.json()

            if resp["success"]:
                LOGGER.debug(f"Msgs receveided: {resp['msgs']}")
                validated = msgsnoaa_list.validate_python(resp["msgs"])
                return validated
            else:
                LOGGER.error(f"Failed to get data: {resp['error']}")
                return None


def login(username: str, password: str) -> Optional[requests.Session]:
    session = requests.Session()

    r = session.get(LOGIN_URL)
    payload = {
        "__RequestVerificationToken": r.cookies["__RequestVerificationToken"],
        "UserName": username,
        "Password": password,
    }
    with session.post(LOGIN_URL, data=payload) as r:
        if r.url != URL("https://dcs1.noaa.gov/ACCOUNT/Login"):
            return session
        else:
            LOGGER.error("Failed to login, probably the password has changed")
            return None
