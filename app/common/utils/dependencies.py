import logging
from typing import Annotated

from fastapi import Depends
from redis import Redis

from app.common.consts import ErrorCodesEnums
from app.common.consts.dependencies import get_error_codes
from app.common.contracts import IPasswordHelper, ITokenHelper, ICustomDateTime, ITokenValidator
from app.common.dependencies import (
    get_redis_client,
    oauth2_scheme
)
from app.common.logger.dependencies import get_base_logger, get_user_logger
from app.common.schemas import TokenData
from app.common.utils import PasswordHelper, TokenHelper, CustomDateTime, TokenValidator


def get_custom_datetime(
) -> ICustomDateTime:
    """
    Dependency provider for ICustomDateTime.

    This function provides an instance of the `CustomDateTime` class,
    which offers methods for retrieving the current datetime either in a naive
    (timezone-unaware) form or in a timezone-aware form based on the application configuration.

    :return: An instance of `CustomDateTime` that implements `ICustomDateTime`.
    """

    return CustomDateTime()


def get_password_helper() -> IPasswordHelper:
    """
    Dependency provider for password hashing utility.

    Returns an instance of PasswordHelper that implements the IPasswordHelper
    interface, used for securely hashing and verifying passwords.

    :return: Instance of PasswordHelper implementing IPasswordHelper.
    """

    return PasswordHelper()


def get_token_helper(
    redis: Annotated[Redis, Depends(get_redis_client)],
    logger: Annotated[logging.Logger, Depends(get_base_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    custom_datetime: Annotated[ICustomDateTime, Depends(get_custom_datetime)],
) -> ITokenHelper:
    """
    Dependency provider for token management helper.

    Returns an instance of TokenHelper configured with Redis, error enums,
    and a logger. This helper provides functionality to create, decode,
    and validate JWT tokens (access and refresh) with blacklist support via Redis.

    :param redis: Redis client used to store token states and support revocation.
    :param logger: Logger instance for tracking token-related operations.
    :param error_codes: Enum container for structured error handling.
    :param custom_datetime: Instance of ICustomDateTime for time-based operations like token expiry.
    :return: Instance of TokenHelper implementing ITokenHelper.
    """

    return TokenHelper(
        redis=redis,
        errors=error_codes,
        logger=logger,
        custom_datetime=custom_datetime
    )


def get_token_validator(
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    token_helper: Annotated[ITokenHelper, Depends(get_token_helper)],
) -> ITokenValidator:
    """
    Dependency provider for ITokenValidator.

    This function returns an instance of the `TokenValidator` class,
    responsible for validating access and refresh tokens using the provided
    logger, error codes, and token helper implementation.

    :param logger: Logger instance used for logging validation events.
    :param error_codes: Error code enums to raise appropriate domain errors.
    :param token_helper: TokenHelper used for decoding and verifying tokens.
    :return: An instance of `TokenValidator` implementing `ITokenValidator`.
    """

    return TokenValidator(
        errors=error_codes,
        logger=logger,
        token_helper=token_helper
    )


def validate_access_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    validator: Annotated[ITokenValidator, Depends(get_token_validator)],
) -> TokenData:
    """
    Validates the provided access token using the `TokenValidator`.

    This function is used as a FastAPI dependency to decode and validate
    the access token, ensuring it's structurally valid, not blacklisted, and
    of the correct type.

    :param token: JWT access token string extracted from the request.
    :param validator: TokenValidator instance injected by dependency.
    :return: A valid `TokenData` object decoded from the token.
    :raises BackendException: If the token is invalid, expired, or of wrong type.
    """

    return validator.validate_access_token(token)


def validate_refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    validator: Annotated[ITokenValidator, Depends(get_token_validator)],
) -> TokenData:
    """
    Validates the provided refresh token using the `TokenValidator`.

    This function decodes and verifies the refresh token for validity,
    correctness of type, and blacklist status. Intended for use in
    refresh-token-based auth flows.

    :param token: JWT refresh token string extracted from the request.
    :param validator: TokenValidator instance injected by dependency.
    :return: A valid `TokenData` object decoded from the token.
    :raises BackendException: If the token is invalid, expired, or of wrong type.
    """

    return validator.validate_refresh_token(token)
