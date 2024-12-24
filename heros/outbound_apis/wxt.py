import logging
import re
from typing import Optional
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field, asdict

from yarl import URL

import aiohttp
from heros.types.wxtdata import RequestsFields, MsgNOAA, MsgType, msgsnoaa_list

NOAA_URL = "https://dcs1.noaa.gov/"
LOGIN_URL = NOAA_URL + "ACCOUNT/Login"
FIELD_TEST = NOAA_URL + "Account/FieldTest"


LOGGER = logging.getLogger(__name__)


async def request_data(requests: RequestsFields, login: str, password: str):
    payload = requests.model_dump(by_alias=True)
    LOGGER.info(f"Requesting data from NOAA: {payload}")
    payload.update({"Username": login, "Password": password})

    async with aiohttp.ClientSession() as session:
        async with session.post(FIELD_TEST, data=payload) as r:
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
