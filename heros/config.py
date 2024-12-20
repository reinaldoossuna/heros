from dotenv import load_dotenv
import os

DSN = "postgresql://{user}:{password}@{host}/{database}"

load_dotenv()


def spi_config():
    return {
        "user": os.getenv("SPI_USER"),
        "password": os.getenv("SPI_PASSWORD"),
    }


def noaa_config():
    return {
        "user": os.getenv("NOAA_USER"),
        "password": os.getenv("NOAA_PASSWORD"),
    }


def database_url():
    return DSN.format(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE"),
        host=os.getenv("DB_HOST"),
    )
