import logging
from datetime import datetime, timedelta
from typing import List, Optional

import requests

from heros.types.noaa import MsgNOAA, RequestsFields, msgsnoaa_list

NOAA_URL = "https://dcs1.noaa.gov/"
LOGIN_URL = NOAA_URL + "ACCOUNT/Login"
FIELD_TEST = NOAA_URL + "Account/FieldTest"


LOGGER = logging.getLogger(__name__)


def login(username: str, password: str) -> Optional[requests.Session]:
    """
    Authenticate with NOAA and return a session if login succeeds.
    
    Note: This function creates a session but does NOT verify that the login
    actually worked. Use verify_login() to confirm authentication.
    """
    session = requests.Session()

    r = session.get(LOGIN_URL)
    payload = {
        "__RequestVerificationToken": r.cookies["__RequestVerificationToken"],
        "UserName": username,
        "Password": password,
    }
    with session.post(LOGIN_URL, data=payload) as r:
        if r.url != "https://dcs1.noaa.gov/ACCOUNT/Login":
            return session
        else:
            LOGGER.error("Failed to login, probably the password has changed")
            return None


def verify_login(username: str, password: str) -> bool:
    """
    Verify that NOAA login credentials are valid by attempting to fetch data.
    
    This performs an actual API call to verify the credentials work.
    
    Args:
        username: NOAA username
        password: NOAA password
    
    Returns:
        True if login is valid and data can be retrieved, False otherwise
    """
    try:
        # Try to fetch data from yesterday to today to verify the credentials work
        today = datetime.today()
        yesterday = today - timedelta(days=1)
        
        result = request_data(username, password, start_date=yesterday, end_date=today)
        
        if result is not None:
            LOGGER.debug("Login verification successful - able to retrieve data")
            return True
        else:
            LOGGER.error("Login verification failed - unable to retrieve data")
            return False
    except Exception as e:
        LOGGER.error(f"Login verification failed with exception: {e}")
        return False


def request_data(
    login: str, password: str, *, start_date: datetime, end_date: Optional[datetime] = None
) -> Optional[List[MsgNOAA]]:
    """
    Request weather data from NOAA API for a given date range.
    
    Args:
        login: NOAA username
        password: NOAA password
        start_date: Start date for data request
        end_date: End date for data request. Defaults to today if not provided.
    
    Returns:
        List of MsgNOAA objects if successful, None if the request fails.
        
    Raises:
        No exceptions are raised; errors are logged and None is returned.
    """
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
