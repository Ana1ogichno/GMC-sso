from typing import Any

from pydantic import Field, field_validator, PostgresDsn, EmailStr
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )
    # Redis Configuration

    REDIS_HOST: str = Field("0.0.0.0", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
