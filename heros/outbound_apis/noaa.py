from datetime import datetime
import logging
from typing import Optional

from yarl import URL

import aiohttp
from heros.types.noaa import RequestsFields, msgsnoaa_list

NOAA_URL = "https://dcs1.noaa.gov/"
LOGIN_URL = NOAA_URL + "ACCOUNT/Login"
FIELD_TEST = NOAA_URL + "Account/FieldTest"


LOGGER = logging.getLogger(__name__)


async def request_data(
    login: str, password: str, *, start_date: datetime, end_date: datetime = datetime.today()
):
    payload = RequestsFields(
        start_date=start_date, end_date=end_date, user=login, password=password
    )

    async with aiohttp.ClientSession() as session:
        async with session.post(FIELD_TEST, data=payload.model_dump(by_alias=True)) as r:
            resp = await r.json()

            if resp["success"]:
                LOGGER.debug(f"Msgs receveided: {resp['msgs']}")
                validated = msgsnoaa_list.validate_python(resp["msgs"])
                datas = [m.model_dump() for m in validated]
                return datas
            else:
                LOGGER.error(f"Failed to get data: {resp['error']}")
                return None


async def login(username: str, password: str) -> Optional[aiohttp.ClientSession]:
    session = aiohttp.ClientSession()

    r = await session.get(LOGIN_URL)
    payload = {
        "__RequestVerificationToken": r.cookies["__RequestVerificationToken"],
        "UserName": username,
        "Password": password,
    }
    async with session.post(LOGIN_URL, data=payload) as r:
        if r.url != URL("https://dcs1.noaa.gov/ACCOUNT/Login"):
            return session
        else:
            LOGGER.error("Failed to login, probably the password has changed")
            return None
