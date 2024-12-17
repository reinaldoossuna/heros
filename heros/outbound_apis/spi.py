import logging

import pandas as pd
import aiohttp

from heros.types.sensordata import sensors_data_list

API_URL = "https://leituras.spi.engtecnologia.com/api/"
LOGIN_URL = API_URL + "usuarios/login"
DATA_URL = API_URL + "leituras/listar_leituras_por_idempresa"

LOGGER = logging.getLogger(__name__)


async def login(username: str, password: str):
    LOGGER.info(f"Logging in as {username}")
    session = aiohttp.ClientSession()
    async with session.post(
        LOGIN_URL, json={"email_usuario": username, "senha": password}
    ) as r:
        if r.ok:
            resp = await r.json()
            LOGGER.debug(f"got from the server: {resp}")
            token = resp.get("token")
            session.headers["Authorization"] = f"Bearer {token}"
            return session
        else:
            return r.reason()


async def request_data(session):
    LOGGER.info(f"Requesting data from {API_URL}")
    async with session.get(DATA_URL) as r:
        if r.ok:
            resp = await r.json()
            LOGGER.debug(f"got from the server: {resp}")
            raw = resp["result"]
            return sensors_data_list.validate_python(raw)
        else:
            return r.reason()
