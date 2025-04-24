import logging

from fastapi.security import OAuth2PasswordRequestForm

from app.common.consts import ErrorCodesEnums
from app.common.contracts import IPasswordHelper
from app.common.decorators.logger import LoggingFunctionInfo
from app.config.exception import BackendException
from app.modules.auth.contracts import IAuthManagerService
from app.modules.user.contracts import IUserRepository
from app.modules.user.schemas import UserInDBBase


class AuthManagerService(IAuthManagerService):
    """
    AuthManager is responsible for handling user authentication logic.

    This class uses a user repository to validate the provided credentials
    and returns a user if authentication is successful. Otherwise, it raises
    an authentication-related exception.
    """

    def __init__(
            self,
            errors: ErrorCodesEnums,
            logger: logging.Logger,
            password_helper: IPasswordHelper,
            user_repository: IUserRepository
    ):
        """
        Initialize AuthManager with a user repository dependency.

        :param errors: Enum provider containing error codes.
        :param logger: Logger instance for tracking authentication operations.
        :param password_helper: Utility for securely hashing and verifying passwords.
        :param user_repository: An instance of IUserRepository to manage user data access.
        """

        self._errors = errors
        self._logger = logger
        self._password_helper = password_helper
        self._user_repository = user_repository

    @LoggingFunctionInfo(
        description="Authenticates a user using the provided credentials (email and password)."
    )
    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> UserInDBBase:
        """
        Authenticate the user using provided credentials.

        :param credentials: OAuth2 form credentials (username = email, password).
        :return: The authenticated user.
        :raises BackendException: If authentication fails.
        """

        self._logger.debug(f"Authenticating user: {credentials.username}")

        user = await self._user_repository.get_by_email(email=credentials.username)

        if not user:
            self._logger.debug(f"Authentication failed: user with email {credentials.username} not found.")
            raise BackendException(self._errors.User.INCORRECT_CREDENTIALS)

        if not self._password_helper.verify_password(credentials.password, user.hashed_password):
            self._logger.debug(f"Authentication failed: invalid password for user {credentials.username}.")
            raise BackendException(self._errors.User.INCORRECT_CREDENTIALS)

        self._logger.info(f"User authenticated successfully: {user.email}")
        return user
