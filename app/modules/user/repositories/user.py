import logging

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.consts import ErrorCodesEnums
from app.common.contracts import IPasswordHelper
from app.common.decorators.logger import LoggingFunctionInfo
from app.common.logger.dependencies import get_base_logger
from app.common.repositories import CrudRepository
from app.config.exception import BackendException
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
            logger: logging.Logger,
            password_helper: IPasswordHelper
    ):
        """
        Initializes the UserRepository with required dependencies.

        This constructor sets up the repository with access to the database session,
        error code enums for structured exception handling, and a password helper for
        secure password hashing and verification.

        :param db: Async SQLAlchemy session used for database operations.
        :param errors: Enum container for application-specific error codes.
        :param logger: Logger instance for tracking authentication operations.
        :param password_helper: Utility for securely hashing and verifying passwords.
        """

        super().__init__(
            db=db,
            model=UserModel,
            errors=errors,
            logger=logger
        )
        self._errors = errors
        self._logger = logger
        self._password_helper = password_helper

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

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Create new user with hashed password and handle possible conflicts."
    )
    async def create_with_hashed_password(self, obj_in: UserCreate, with_commit: bool = True) -> UserModel:
        """
        Create a new user, hashing their password before storing.

        :param obj_in: User creation schema.
        :param with_commit: Whether to commit after creation.
        :return: Created UserModel instance.
        """

        try:
            obj = obj_in.model_dump()
            obj["hashed_password"] = self._password_helper.get_password_hash(obj_in.password)
            obj.pop("password")

            db_obj = self._model(**obj)
            self._db.add(db_obj)

            await self._commit_and_refresh(db_obj, with_commit)

            self._logger.debug(f"User created with email: {obj_in.email}")
            return db_obj
        except IntegrityError as e:
            self._logger.debug(f"IntegrityError during user creation: {e}")
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e

    @LoggingFunctionInfo(
        logger=Depends(get_base_logger),
        description="Authenticate user using email and password."
    )
    async def authenticate(
        self,
        email: str,
        password: str,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> UserInDBBase | None:
        """
        Authenticate a user by email and password.

        :param email: Email used for login.
        :param password: Plain-text password.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: UserModel if credentials are valid, else None.
        """

        user = await self.get_by_email(email=email, custom_options=custom_options)

        if not user:
            self._logger.debug(f"Authentication failed: user with email {email} not found.")
            return None

        if not self._password_helper.verify_password(password, user.hashed_password):
            self._logger.debug(f"Authentication failed: invalid password for user {email}.")
            return None

        self._logger.debug(f"User authenticated successfully: {email}")
        return user
