from enum import StrEnum, auto
from logging import DEBUG, ERROR, INFO, WARNING
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Account(BaseModel):
    user: str
    password: str


class Level(StrEnum):
    info = auto()
    warning = auto()
    error = auto()
    debug = auto()

    def to_logging(self):
        match self.value:
            case Level.info:
                return INFO
            case Level.warning:
                return WARNING
            case Level.error:
                return ERROR
            case Level.debug:
                return DEBUG

    def is_debug(self):
        return self.value == DEBUG


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", extra="ignore", cli_parse_args=True
    )

    port: int
    pg_dsn: PostgresDsn
    engtec: Account
    noaa: Account
    log_level: Level
    report_template: str


settings = Settings()  # pyright: ignore[reportCallIssue]
