import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.common.decorators.logger import LoggingFunctionInfo
from app.common.logger.dependencies import get_base_logger
from app.common.schemas import LoginToken, RefreshToken, Msg
from app.config.settings import settings
from app.modules.auth.consts import AuthUseCaseEnums
from app.modules.auth.contracts import (
    IAuthManagerService,
    ITokenService,
    ISessionStorageService,
    IAuthUseCase
)
from app.modules.user.schemas import UserInDBBase


class AuthUseCase(IAuthUseCase):
    """
    UseCase responsible for handling authentication, including token generation,
    token refreshing, and token invalidation. This service interacts with
    the authentication manager, token provider, and session storage.

    Attributes:
        _auth_manager: The manager responsible for authenticating users.
        _token_provider: The service responsible for generating and validating tokens.
        _session_storage: The service responsible for handling user sessions.
        _logger: Logger for logging activities within the service.
        _enums: The enums used in the authentication service (e.g., payload fields).
    """

    def __init__(
        self,
        auth_manager: IAuthManagerService,
        token_provider: ITokenService,
        session_storage: ISessionStorageService,
        logger: logging.Logger,
        enums: AuthUseCaseEnums
    ):
        """
        Initializes the AuthUseCase with necessary dependencies.

        :param auth_manager: The manager that handles user authentication.
        :param token_provider: The provider that handles token creation and validation.
        :param session_storage: The storage responsible for handling user sessions.
        :param logger: Logger instance for logging service activities.
        :param enums: Enum class for accessing common payload fields.
        """

        self._auth_manager = auth_manager
        self._token_provider = token_provider
        self._session_storage = session_storage
        self._logger = logger
        self._enums = enums

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="This function is responsible for generating a pair of access and refresh tokens for the user."
    )
    async def get_token_pair(
        self, form_data: OAuth2PasswordRequestForm
    ) -> LoginToken:
        """
        Generates a pair of access and refresh tokens for the user based on provided credentials.

        :param form_data: The form data containing the username and password.
        :return: A LoginToken instance containing the generated tokens.
        """

        self._logger.debug("Authenticate the user")
        user = await self._auth_manager.authenticate(form_data)

        self._logger.debug("Prepare payload for the token")
        payload = {
            self._enums.PayloadFields.SUB.value: str(user.sid),
            self._enums.PayloadFields.PERMISSIONS.value: ["777"],
        }

        self._logger.debug(f"Generating token pair for user {user.sid}.")
        return await self._token_provider.create_token_pair(payload)

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="This function refreshes the access token using the provided refresh token."
    )
    async def update_access_token(
        self, refresh_token: RefreshToken
    ) -> LoginToken:
        """
        Refreshes the access token using the provided refresh token.

        :param refresh_token: The refresh token to be used for generating a new access token.
        :return: A new LoginToken instance with the updated access token.
        """

        self._logger.debug("Validate the refresh token")
        payload = await self._token_provider.validate_token(refresh_token.refresh_token)

        self._logger.debug("Invalidate the old session")
        await self._session_storage.invalidate_session(
            session_id=f"{payload[self._enums.PayloadFields.SUB.value]}:{payload[self._enums.PayloadFields.JTI.value]}",
            expire_seconds=settings.project.REFRESH_TOKEN_EXPIRE_SECONDS
        )

        self._logger.debug(f"Refreshing access token for user {payload[self._enums.PayloadFields.SUB.value]}.")
        return await self._token_provider.create_token_pair(
            {
                self._enums.PayloadFields.SUB.value: payload[self._enums.PayloadFields.SUB.value],
                self._enums.PayloadFields.PERMISSIONS.value: payload[self._enums.PayloadFields.PERMISSIONS.value]
            }
        )

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="This function invalidates user tokens, either globally or for a specific session."
    )
    async def delete_tokens(
        self, token: str, user: UserInDBBase, everywhere: bool
    ) -> Msg:
        """
        Invalidates user tokens, either globally or for a specific session.

        :param token: The access token to be invalidated.
        :param user: The user whose tokens will be invalidated.
        :param everywhere: Flag indicating whether to invalidate tokens everywhere (all sessions).
        :return: A message indicating the result of the operation.
        """

        if everywhere:
            self._logger.debug("Invalidate all session")
            await self._session_storage.invalidate_all_sessions(
                user_id=str(user.sid),
                expire_seconds=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS
            )
            self._logger.info(f"All sessions invalidated for user {user.sid}.")
        else:
            self._logger.info("Invalidate a specific session")
            payload = await self._token_provider.validate_token(token)
            await self._session_storage.invalidate_session(
                session_id=f"{str(user.sid)}:{payload['jti']}",
                expire_seconds=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS
            )
            self._logger.info(f"Session invalidated for user {user.sid}, token {token}.")
        return Msg(msg="Successfully logged out.")
