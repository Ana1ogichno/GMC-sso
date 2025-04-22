import logging
from typing import Annotated

from fastapi import Depends

from app.common.logger.dependencies import get_auth_logger
from app.modules.auth.consts.dependencies import get_auth_usecase_enums
from app.modules.auth.consts.enums import AuthUseCaseEnums
from app.modules.auth.contracts import (
    IAuthManagerService,
    ITokenService,
    ISessionStorageService,
    IAuthUseCase
)
from app.modules.auth.services.dependencies import (
    get_auth_manager_service,
    get_token_service,
    get_session_storage_service
)
from app.modules.auth.usecases.auth import AuthUseCase


async def get_auth_usecase(
    logger: Annotated[logging.Logger, Depends(get_auth_logger)],
    auth_enums: Annotated[AuthUseCaseEnums, Depends(get_auth_usecase_enums)],
    auth_manager: Annotated[IAuthManagerService, Depends(get_auth_manager_service)],
    token_service: Annotated[ITokenService, Depends(get_token_service)],
    session_storage_service: Annotated[ISessionStorageService, Depends(get_session_storage_service)]
) -> IAuthUseCase:
    """
    Dependency provider for IAuthService implementation.

    Coordinates user authentication flow by injecting dependencies:
    manager for user logic, token provider for JWT operations,
    session storage for managing active sessions and token invalidation.

    :param logger: Logger for structured logging.
    :param auth_enums: Error codes and enums specific to the Auth domain.
    :param auth_manager: AuthManager handling business logic for auth.
    :param token_service: TokenService handling JWT creation and validation.
    :param session_storage_service: Service for managing session state (e.g., Redis).
    :return: Instance of AuthService implementing IAuthService.
    """

    return AuthUseCase(
        auth_manager=auth_manager,
        token_provider=token_service,
        session_storage=session_storage_service,
        logger=logger,
        enums=auth_enums,
    )
