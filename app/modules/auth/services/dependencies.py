import logging
from typing import Annotated

from fastapi import Depends
from redis import Redis

from app.common.consts import ErrorCodesEnums
from app.common.consts.dependencies import get_error_codes
from app.common.contracts import ITokenHelper, IPasswordHelper
from app.common.dependencies import get_redis_client
from app.common.logger.dependencies import get_auth_logger
from app.common.utils.dependencies import get_token_helper, get_password_helper
from app.modules.auth.contracts import (
    IAuthManagerService,
    ITokenService,
    ISessionStorageService,
)
from app.modules.auth.services import AuthManagerService, SessionStorageService, TokenService
from app.modules.user.contracts import IUserRepository
from app.modules.user.repositories.dependencies import get_user_repository


async def get_auth_manager_service(
    logger: Annotated[logging.Logger, Depends(get_auth_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    password_helper: Annotated[IPasswordHelper, Depends(get_password_helper)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)]
) -> IAuthManagerService:
    """
    Dependency provider for IAuthManagerService implementation.

    Initializes and returns an instance of AuthManagerService, which handles
    user authentication logic such as credential validation and user lookup.

    :param logger: Logger instance for capturing authentication-related logs.
    :param error_codes: Centralized enumeration of error codes for exception handling.
    :param password_helper: Utility for securely hashing and verifying passwords.
    :param user_repository: Repository interface for interacting with user data in the database.
    :return: Instance of AuthManagerService implementing IAuthManagerService.
    """

    return AuthManagerService(
        errors=error_codes,
        logger=logger,
        password_helper=password_helper,
        user_repository=user_repository
    )


async def get_session_storage_service(
    redis: Annotated[Redis, Depends(get_redis_client)],
    logger: Annotated[logging.Logger, Depends(get_auth_logger)],
) -> ISessionStorageService:
    """
    Dependency provider for ISessionStorageService implementation.

    Sets up session storage with Redis backend for tracking token/session state.

    :param redis: Redis client for token/session storage.
    :param logger: Logger for structured logging.
    :return: Instance of SessionStorageService implementing ISessionStorageService.
    """

    return SessionStorageService(
        redis=redis,
        logger=logger
    )


async def get_token_service(
    logger: Annotated[logging.Logger, Depends(get_auth_logger)],
    token_helper: Annotated[ITokenHelper, Depends(get_token_helper)],
) -> ITokenService:
    """
    Dependency provider for ITokenService implementation.

    Provides a TokenService instance, which is responsible for generating
    and validating JWT tokens using the TokenHelper.

    :param logger: Logger for structured logging.
    :param token_helper: Helper utility for creating and parsing tokens.
    :return: Instance of TokenService implementing ITokenService.
    """

    return TokenService(
        logger=logger,
        token_helper=token_helper
    )
