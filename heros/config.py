from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Account(BaseModel):
    user: str
    password: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", extra="ignore", cli_parse_args=True
    )

    port: int
    pg_dsn: PostgresDsn
    engtec: Account
    noaa: Account


settings = Settings()  # pyright: ignore[reportCallIssue]
