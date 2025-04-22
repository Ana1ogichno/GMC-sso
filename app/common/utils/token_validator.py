import logging

from jose import JWTError

from app.common.consts import ErrorCodesEnums
from app.common.contracts import ITokenHelper
from app.common.contracts import ITokenValidator
from app.config.exception import BackendException
from app.common.schemas import TokenData


class TokenValidator(ITokenValidator):
    """
    TokenValidator is responsible for validating both access and refresh tokens.

    It uses a token helper to decode and verify JWT tokens and applies
    custom error codes in case of invalid or missing tokens.
    """

    def __init__(
        self,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        token_helper: ITokenHelper
    ):
        """
        Initialize the TokenValidator.

        :param errors: Enum providing standardized error codes.
        :param logger: Logger instance for logging events.
        :param token_helper: Helper class responsible for token decoding and validation.
        """

        self._errors = errors
        self._logger = logger
        self._token_helper = token_helper

    def validate_access_token(self, token: str) -> TokenData:
        """
        Validate the access token and return token payload.

        :param token: JWT access token.
        :return: TokenData object with extracted payload.
        :raises: BackendException with INCORRECT_CREDENTIALS if validation fails.
        """

        if not token:
            self._logger.debug("Access token is missing.")
            raise self._errors.User.INCORRECT_CREDENTIALS

        try:
            self._logger.debug("Validating access token.")
            return self._token_helper.token_payload(token=token, refresh=False)
        except (JWTError, BackendException) as e:
            self._logger.debug(f"Access token validation failed: {str(e)}")
            raise self._errors.User.INCORRECT_CREDENTIALS

    def validate_refresh_token(self, token: str) -> TokenData:
        """
        Validate the refresh token and return token payload.

        :param token: JWT refresh token.
        :return: TokenData object with extracted payload.
        :raises: BackendException with INCORRECT_CREDENTIALS if validation fails.
        """

        if not token:
            self._logger.debug("Refresh token is missing.")
            raise self._errors.User.INCORRECT_CREDENTIALS

        try:
            self._logger.debug("Validating refresh token.")
            return self._token_helper.token_payload(token=token, refresh=True)
        except JWTError as e:
            self._logger.debug(f"Refresh token validation failed: {str(e)}")
            raise self._errors.User.INCORRECT_CREDENTIALS
