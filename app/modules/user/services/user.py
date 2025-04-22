import logging
from uuid import UUID

from fastapi import Depends
from sqlalchemy.sql.base import ExecutableOption

from app.common.consts import ErrorCodesEnums
from app.common.decorators.logger import LoggingFunctionInfo
from app.common.logger.dependencies import get_base_logger
from app.config.exception import BackendException
from app.modules.user.contracts import IUserRepository, IUserService
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserCreate, UserInDBBase


class UserService(IUserService):
    """
    Service for managing user-related operations.

    This service provides methods for retrieving users by email or session ID (SID),
    and creating new users. It uses the provided repository for interacting with the
    data layer and ensures that appropriate logging and error handling are in place
    for each operation.
    """

    def __init__(
        self,
        errors: ErrorCodesEnums,
        logger: logging.Logger,
        user_repository: IUserRepository
    ):
        """
        Initialize the UserService with required dependencies.

        :param errors: Enum container for application-specific error codes.
        :param logger: Logger instance for tracking user-related operations.
        :param user_repository: Repository for accessing and managing user data.
        """

        self._errors = errors
        self._logger = logger
        self._user_repository = user_repository

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Retrieving a user by email address."
    )
    async def get_user_by_email(
        self, email: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserInDBBase | None:
        """
        Retrieves a user by their email address.

        :param email: Email address of the user to retrieve.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: UserModel instance if user is found, otherwise None.
        """

        return await self._user_repository.get_by_email(
            email=email, custom_options=custom_options
        )

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Retrieving a user by their session ID (SID)."
    )
    async def get_user_by_sid(
        self, sid: UUID
    ) -> UserModel | None:
        """
        Retrieves a user by their session ID (SID).

        :param sid: Session ID of the user to retrieve.
        :return: UserModel instance if user is found, otherwise None.
        """

        return await self._user_repository.get_by_sid(sid=sid)

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Creates a new user. Checks if the email already exists. If not, the user is created."
    )
    async def create_user(self, user_in: UserCreate) -> UserModel:
        """
        Creates a new user.

        :param user_in: Data required to create the new user.
        :return: UserModel instance of the newly created user.
        :raises BackendException: If a user with the given email already exists.
        """

        user = await self._user_repository.get_by_email(email=user_in.email)

        if user:
            raise BackendException(self._errors.User.EMAIL_ALREADY_EXISTS)

        user = await self._user_repository.create(obj_in=user_in, with_commit=False)

        return user
