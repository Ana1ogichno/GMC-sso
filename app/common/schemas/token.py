from pydantic import BaseModel, Field

from app.common.schemas import CoreSchema


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenData(CoreSchema):
    sid: str = Field(description="Сид пользователя")
    jti: str = Field(description="JWT ID")
    permissions: list[str] = Field(description="Права пользователя")


class LoginToken(RefreshToken, AccessToken):
    pass
