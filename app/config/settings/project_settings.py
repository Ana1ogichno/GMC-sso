from typing import Any

from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    # API
    API_V1_STR: str = "/api/v1"

    # Service Info
    PROJECT_VERSION: str = "0.0.1"  # Изменять вручную
    PROJECT_NAME: str = "GMC SSO Service"

    HOST: str = Field("0.0.0.0")
    PORT: int = Field(8000)

    # JWT Settings
    TOKEN_SECRET_KEY: str = "super_secret_key"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60
    REFRESH_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 30

    OAUTH_SECRET_KEY: str = Field("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")

    # Superuser
    FIRST_SUPERUSER_LOGIN: EmailStr = Field("root@email.com")
    FIRST_SUPERUSER_PASSWORD: str = Field("123123")
