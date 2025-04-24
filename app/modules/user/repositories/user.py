import logging

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.consts import ErrorCodesEnums
from app.common.decorators.logger import LoggingFunctionInfo
from app.common.logger.dependencies import get_base_logger
from app.common.repositories import CrudRepository
from app.modules.user.contracts import IUserRepository
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserCreate, UserUpdate, UserInDBBase


class UserRepository(CrudRepository[UserModel, UserCreate, UserUpdate], IUserRepository):
    """
    Repository class for user-specific database operations.
    """

    def __init__(
            self,
            db: AsyncSession,
            errors: ErrorCodesEnums,
            logger: logging.Logger
    ):
        """
        Initializes the UserRepository with required dependencies.

        This constructor sets up the repository with access to the database session,
        error code enums for structured exception handling, and a password helper for
        secure password hashing and verification.

        :param db: Async SQLAlchemy session used for database operations.
        :param errors: Enum container for application-specific error codes.
        :param logger: Logger instance for tracking authentication operations.
        """

        super().__init__(
            db=db,
            model=UserModel,
            errors=errors,
            logger=logger
        )
        self._errors = errors
        self._logger = logger

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Fetch user by email address from the database."
    )
    async def get_by_email(
        self, email: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserInDBBase | None:
        """
        Retrieve a user by their email address.

        :param email: Email of the user.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: UserModel instance or None.
        """

        query = await self._apply_options(
            query=select(self._model).where(self._model.email == email),
            options=custom_options
        )

        self._logger.debug(f"Retrieved user by email: {email}")
        return await self._get_single_result(query)
