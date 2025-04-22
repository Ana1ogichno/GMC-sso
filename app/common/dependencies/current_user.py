from typing import Annotated

from fastapi import Depends

from app.common.consts import ErrorCodesEnums
from app.common.consts.dependencies import get_error_codes
from app.common.utils.dependencies import validate_access_token
from app.config.exception import BackendException
from app.common.schemas import TokenData
from app.modules.user.contracts import IUserRepository
from app.modules.user.models import UserModel
from app.modules.user.repositories.dependencies import get_user_repository


async def get_current_user(
    payload: Annotated[TokenData, Depends(validate_access_token)],
    error_codes: Annotated[ErrorCodesEnums, Depends(get_error_codes)],
    user_repository: Annotated[IUserRepository, Depends(get_user_repository)],
) -> UserModel:
    """
    Dependency provider for retrieving the currently authenticated user.

    This function uses the validated JWT token payload to look up the
    corresponding user in the database. If the user does not exist,
    an authentication-related exception is raised.

    :param payload: Decoded `TokenData` from a valid access token.
    :param error_codes: Enum provider with application-specific error codes.
    :param user_repository: Repository instance for accessing user data.
    :return: The `UserModel` representing the authenticated user.
    :raises BackendException: If no user is found for the given SID.
    """

    user = await user_repository.get_by_sid(sid=payload.sid)

    if user is None:
        raise BackendException(error=error_codes.User.INCORRECT_CREDENTIALS)

    return user
