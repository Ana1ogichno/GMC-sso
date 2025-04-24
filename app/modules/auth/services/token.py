import logging

from jose import jwt

from app.common.contracts.utils import ITokenHelper
from app.common.decorators.logger import LoggingFunctionInfo
from app.common.schemas import LoginToken
from app.config.settings import settings
from app.modules.auth.contracts import ITokenService


class TokenService(ITokenService):
    """
    Service for handling token-related business logic.

    Responsibilities:
    - Generate token pairs using TokenHelper.
    - Decode and validate JWT tokens.
    """

    def __init__(
        self,
        logger: logging.Logger,
        token_helper: ITokenHelper
    ):
        """
        Initialize TokenService.

        :param logger: Logger instance for structured logging.
        :param token_helper: Token helper instance that encapsulates token logic.
        """

        self._logger = logger
        self._token_helper = token_helper

    @LoggingFunctionInfo(
        description="Generate a pair of access and refresh JWT tokens"
    )
    async def create_token_pair(self, payload: dict) -> LoginToken:
        """
        Create access and refresh token pair using the provided payload.

        :param payload: Dictionary containing user identification and permissions.
        :return: LoginToken object with access and refresh tokens.
        """

        self._logger.debug("Request to create token pair. Payload: %s", payload)

        return self._token_helper.create_token_pair(payload)

    @LoggingFunctionInfo(
        description="Decode and validate JWT token using project secret and algorithm"
    )
    async def validate_token(self, token: str) -> dict:
        """
        Decode a JWT token and return its payload.

        :param token: Encoded JWT token.
        :return: Decoded payload as dictionary.
        """

        self._logger.debug("Validating token: %s", token)

        return jwt.decode(
            token,
            settings.project.TOKEN_SECRET_KEY,
            algorithms=[settings.project.ALGORITHM]
        )
