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
