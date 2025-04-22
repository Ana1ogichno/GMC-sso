from abc import ABC, abstractmethod
from typing import Tuple
from sqlalchemy.sql.base import ExecutableOption

from app.common.contracts import ICrudRepository
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserCreate, UserUpdate, UserInDBBase


class IUserRepository(ICrudRepository[UserModel, UserCreate, UserUpdate], ABC):
    """
    Abstract interface for user-specific repository operations.

    Extends the generic ICrudRepository to include user-specific behavior,
    such as authentication, email-based lookups, and creation with password hashing.

    This interface abstracts the data access layer for UserModel, promoting
    loose coupling and enabling easy substitution or mocking in tests.
    """

    @abstractmethod
    async def get_by_email(
        self,
        email: str,
        custom_options: Tuple[ExecutableOption, ...] = None
    ) -> UserInDBBase | None:
        """
        Retrieve a user by email address.

        :param email: Email of the user to find.
        :param custom_options: Optional SQLAlchemy query options (e.g., joinedload).
        :return: UserModel instance if found, otherwise None.
        """
        ...

    @abstractmethod
    async def create_with_hashed_password(
        self,
        obj_in: UserCreate,
        with_commit:
        bool = True
    ) -> UserModel:
        """
        Create a new user with a hashed password.

        :param obj_in: User creation schema containing raw password and user data.
        :param with_commit: Whether to commit the transaction after creation.
        :return: The newly created UserModel instance.
        """
        ...

    @abstractmethod
    async def authenticate(
            self, email: str, password: str, custom_options: Tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        """
        Authenticate a user by verifying email and password.

        :param email: Email used for authentication.
        :param password: Plaintext password to verify.
        :param custom_options: Optional SQLAlchemy query options.
        :return: UserModel instance if authentication succeeds, otherwise None.
        """
        ...
