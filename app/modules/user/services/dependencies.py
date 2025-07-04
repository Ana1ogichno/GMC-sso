import logging
from typing import Annotated

from fastapi import Depends

from app.common.consts import ErrorCodesEnums
from app.common.consts.dependencies import get_error_codes
from app.common.logger.dependencies import get_user_logger
from app.modules.user.contracts import IUserRepository, IUserService
from app.modules.user.repositories.dependencies import get_user_repository
from app.modules.user.services import UserService


async def get_user_service(
    logger: Annotated[logging.Logger, Depends(get_user_logger)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)]
) -> IUserService:
    return UserService(
        errors=error_codes,
        logger=logger,
        user_repository=user_repository,
    )
