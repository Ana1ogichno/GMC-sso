import logging
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.common.consts import ErrorCodesEnums
from app.common.consts.dependencies import get_error_codes
from app.common.dependencies import get_db
from app.common.logger.dependencies import get_user_logger
from app.modules.user.contracts import IUserRepository
from app.modules.user.repositories import UserRepository


async def get_user_repository(
    db: Annotated[async_scoped_session[AsyncSession], Depends(get_db)],
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
) -> IUserRepository:
    """
    Dependency provider for IUserRepository implementation.

    Constructs a UserRepository with injected dependencies for database session
    and password hashing utilities. This repository handles all user-related
    persistence operations, such as user creation, authentication, and retrieval.

    :param db: Async SQLAlchemy session used for database interactions.
    :param logger: Logger instance for capturing authentication-related logs.
    :param error_codes: Centralized enumeration of error codes for exception handling.
    :return: An instance of IUserRepository implemented by UserRepository.
    """

    return UserRepository(
        db=db,
        errors=error_codes,
        logger=logger
    )
