import logging
from typing import List, Optional

import requests
from pydantic import ValidationError

from heros.config import Account
from heros.types.engtec import SensorData, sensors_data_list

API_URL = "https://leituras.spi.engtecnologia.com/api/"
LOGIN_URL = API_URL + "usuarios/login"
DATA_URL = API_URL + "leituras/listar_leituras_por_idempresa"

LOGGER = logging.getLogger(__name__)


def _login(username: str, password: str) -> Optional[requests.Session]:
    LOGGER.info(f"Logging in as {username}")
    session = requests.Session()
    cred = {"email_usuario": username, "senha": password}
    with session.post(LOGIN_URL, json=cred) as r:
        if r.ok:
            resp = r.json()
            LOGGER.debug(f"got from the server: {resp}")
            token = resp.get("token")
            session.headers["Authorization"] = f"Bearer {token}"
            return session
        else:
            LOGGER.error(f"Failed to login as {username}, reason: {r.reason}")
            return None


def _request_data(session: requests.Session) -> Optional[List[SensorData]]:
    LOGGER.info(f"Requesting data from {API_URL}")
    with session.get(DATA_URL) as r:
        if r.ok:
            resp = r.json()
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


def request_data(account: Account) -> Optional[List[SensorData]]:
    session = _login(account.user, account.password)
    if session is None:
        return None

    data = _request_data(session)
    session.close()
    return data
