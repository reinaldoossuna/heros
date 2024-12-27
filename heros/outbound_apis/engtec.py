import logging

import aiohttp
from typing import Optional, List
from pydantic import ValidationError

from heros.types.engtec import sensors_data_list, SensorData

API_URL = "https://leituras.spi.engtecnologia.com/api/"
LOGIN_URL = API_URL + "usuarios/login"
DATA_URL = API_URL + "leituras/listar_leituras_por_idempresa"

LOGGER = logging.getLogger(__name__)


async def login(username: str, password: str) -> Optional[aiohttp.ClientSession]:
    LOGGER.info(f"Logging in as {username}")
    session = aiohttp.ClientSession()
    cred = {"email_usuario": username, "senha": password}
    async with session.post(LOGIN_URL, json=cred) as r:
        if r.ok:
            resp = await r.json()
            LOGGER.debug(f"got from the server: {resp}")
            token = resp.get("token")
            session.headers["Authorization"] = f"Bearer {token}"
            return session
        else:
            LOGGER.error(f"Failed to login as {username}, reason: {r.reason}")
            return None


async def request_data(session) -> Optional[List[SensorData]]:
    LOGGER.info(f"Requesting data from {API_URL}")
    async with session.get(DATA_URL) as r:
        if r.ok:
            resp = await r.json()
            LOGGER.debug(f"got from the server: {resp}")
            raw = resp["result"]
            try:
                return sensors_data_list.validate_python(raw)
            except ValidationError as err:
                LOGGER.error(f"Failed to parse data.\n{err}")
                return None

        else:
            LOGGER.error(f"Failed to get data, reason: {r.reason}")
            return None
