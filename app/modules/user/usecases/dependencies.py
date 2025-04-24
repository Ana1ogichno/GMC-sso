from typing import Annotated

from fastapi import Depends

from app.modules.user.contracts import IUserService, IUserUseCase
from app.modules.user.services.dependencies import get_user_service
from app.modules.user.usecases import UserUseCase


async def get_user_usecase(
    user_service: Annotated[IUserService, Depends(get_user_service)]
) -> IUserUseCase:
    """
    Dependency provider for IAuthService implementation.

    Coordinates user authentication flow by injecting dependencies:
    manager for user logic, token provider for JWT operations,
    session storage for managing active sessions and token invalidation.

    :param user_service: Service for accessing and managing the user repository.
    :return: Instance of AuthService implementing IAuthService.
    """

    return UserUseCase(
        user_service=user_service
    )
