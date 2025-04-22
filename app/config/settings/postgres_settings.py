from typing import Any

from pydantic import Field, field_validator, PostgresDsn, EmailStr
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    # PostgresSQL Configuration
    POSTGRES_HOST: str = Field("0.0.0.0")
    POSTGRES_PORT: int = Field(5432)
    POSTGRES_USER: str = Field("referral")
    POSTGRES_PASSWORD: str = Field("referral")
    POSTGRES_DB: str = Field("referral")

    POSTGRES_DATABASE_URL: PostgresDsn | None = None

    @field_validator("POSTGRES_DATABASE_URL", mode="before")
    def assemble_db_connection(cls, v: str | None, values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        options = {
            "scheme": "postgresql+asyncpg",
            "username": values.data.get("POSTGRES_USER"),
            "password": values.data.get("POSTGRES_PASSWORD"),
            "host": values.data.get("POSTGRES_HOST"),
            "port": values.data.get("POSTGRES_PORT"),
            "path": f'{values.data.get("POSTGRES_DB") or ""}',
        }
        return PostgresDsn.build(**options)

    DB_POOL_SIZE: int = Field(20, env="DB_POOL_SIZE")
    WEB_CONCURRENCY: int = Field(1, env="WEB_CONCURRENCY")
    POOL_SIZE: int | None = None

    @field_validator("POOL_SIZE", mode="before")
    def assemble_poll_size(cls, v: int | None, values: ValidationInfo) -> int:
        if isinstance(v, int):
            return v
        return max(
            values.data.get("DB_POOL_SIZE") // values.data.get("WEB_CONCURRENCY"), 5
        )

    TZ: str = Field("Europe/Moscow")
