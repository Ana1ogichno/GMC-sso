import logging
import uuid
from datetime import timedelta
from uuid import UUID

from fastapi import Depends
from jose import jwt
from redis import Redis

from app.common.consts import ErrorCodesEnums
from app.common.contracts.utils import ITokenHelper, ICustomDateTime
from app.common.decorators.logger import LoggingFunctionInfo
from app.common.logger.dependencies import get_base_logger
from app.common.schemas import TokenData, LoginToken
from app.config.exception import BackendException
from app.config.settings import settings


class TokenHelper(ITokenHelper):
    """
    A helper class for handling JWT token creation, decoding, and validation.

    Responsibilities:
    - Generate access and refresh tokens with expiration and unique JTI.
    - Decode and validate JWT payloads based on token type (access/refresh).
    - Store token JTIs in Redis for blacklisting or tracking.
    """

    def __init__(
        self,
        redis: Redis,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        custom_datetime: ICustomDateTime
    ):
        """
        Initialize the TokenHelper.

        :param redis: Redis client used for storing and verifying token JTIs.
        :param errors: Enum provider containing error codes.
        :param logger: Logger instance for recording token-related operations and debugging.
        :param custom_datetime: ICustomDateTime instance for working with the current time.
        """

        self._redis = redis
        self._errors = errors
        self._logger = logger
        self._custom_datetime = custom_datetime

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Create JWT token with custom payload, expiration, and type (access/refresh)"
    )
    def create_token(
        self,
        data: dict,
        expires_delta: timedelta,
        jti: UUID,
        refresh: bool = False,
    ) -> str:
        """
        Generate a JWT token with expiration and JTI.

        :param data: Payload to encode into token.
        :param expires_delta: Token lifetime duration.
        :param jti: Unique JWT ID.
        :param refresh: Flag to indicate if this is a refresh token.
        :return: Encoded JWT token string.
        """

        self._logger.debug("Creating token. Refresh: %s, JTI: %s", refresh, jti)
        to_encode = data.copy()

        expire = self._custom_datetime.get_datetime_w_timezone() + expires_delta
        to_encode.update({"exp": expire, "jti": str(jti)})

        token_type = "refresh" if refresh else "access"
        to_encode.update({"token": token_type})

        encoded_jwt = jwt.encode(
            to_encode, settings.project.TOKEN_SECRET_KEY, algorithm=settings.project.ALGORITHM
        )

        self._logger.debug("Token created successfully. Payload: %s", to_encode)

        return encoded_jwt

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Decode and validate JWT token, ensuring type and blacklist checks"
    )
    def token_payload(self, token: str, refresh: bool) -> TokenData:
        """
        Decode a JWT token and validate its contents.

        :param token: Encoded JWT string.
        :param refresh: Flag to indicate expected token type.
        :return: TokenData containing user SID, JTI, and permissions.
        """

        self._logger.debug("Validating token. Refresh expected: %s", refresh)

        try:
            payload = jwt.decode(
                token, settings.project.TOKEN_SECRET_KEY, algorithms=[settings.project.ALGORITHM]
            )

            self._logger.debug("Decoded payload: %s", payload)

            if refresh and payload.get("token") != "refresh":
                raise BackendException(error=self._errors.Token.BAD_REFRESH_TOKEN)
            elif not refresh and payload.get("token") != "access":
                raise BackendException(error=self._errors.Token.BAD_ACCESS_TOKEN)

            sid: str = payload.get("sub")
            permissions: list[str] = payload.get("permissions")

            if not sid:
                raise BackendException(error=self._errors.User.INCORRECT_CREDENTIALS)

            token_jti: str = payload.get("jti")
            redis_key = f"{sid}:{token_jti}"
            token_key_died = self._redis.get(f"{sid}:{token_jti}")

            self._logger.debug("Redis key check [%s]: %s", redis_key, token_key_died)

            if token_key_died != b"False":
                if refresh:
                    raise BackendException(error=self._errors.Token.BAD_REFRESH_TOKEN)
                raise BackendException(error=self._errors.Token.BAD_ACCESS_TOKEN)

            return TokenData(sid=sid, jti=token_jti, permissions=permissions)

        except jwt.JWTError as e:
            self._logger.error("JWT decode failed: %s", e)
            raise BackendException(error=self._errors.Token.INVALID_TOKEN, cause=str(e))

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Generate a pair of JWT tokens (access and refresh) with unique JTIs"
    )
    def create_token_pair(self, payload: dict) -> LoginToken:
        """
        Create access and refresh JWT token pair and register them in Redis.

        :param payload: User info to include in token (must contain 'sub').
        :return: LoginToken containing access and refresh tokens.
        """

        self._logger.debug("Creating token pair for payload: %s", payload)

        access_jti, refresh_jti = uuid.uuid4(), uuid.uuid4()

        access_token = self.create_token(
            data=payload,
            expires_delta=timedelta(seconds=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS),
            jti=access_jti,
            refresh=False,
        )
        refresh_token = self.create_token(
            data=payload,
            expires_delta=timedelta(seconds=settings.project.REFRESH_TOKEN_EXPIRE_SECONDS),
            jti=refresh_jti,
            refresh=True,
        )

        self._redis.setex(
            name=f"{payload.get('sub')}:{access_jti}",
            time=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            value="False",
        )
        self._redis.setex(
            name=f"{payload.get('sub')}:{refresh_jti}",
            time=settings.project.REFRESH_TOKEN_EXPIRE_SECONDS,
            value="False",
        )

        self._logger.debug(
            "Token pair created. Access JTI: %s, Refresh JTI: %s",
            access_jti, refresh_jti
        )

        return LoginToken(
            access_token=access_token,
            refresh_token=refresh_token
        )
