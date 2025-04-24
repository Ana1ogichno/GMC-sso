from abc import ABC, abstractmethod
from uuid import UUID
from typing import Tuple, Optional

from app.modules.user.models import UserModel
from app.modules.user.schemas import ClientUserCreate
from sqlalchemy.sql.base import ExecutableOption


class IUserService(ABC):
    """
    Abstract interface for user management services.

    This interface defines the methods for user-related operations, including
    retrieving users by email or session ID, and creating new users.
    """

    @abstractmethod
    async def get_user_by_email(
        self, email: str, custom_options: Tuple[ExecutableOption, ...] = None
    ) -> Optional[UserModel]:
        """
        Retrieve a user by their email address.

        :param email: The email address of the user to retrieve.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: UserModel instance if user is found, otherwise None.
        """
        ...

    @abstractmethod
    async def get_user_by_sid(
        self, sid: UUID
    ) -> Optional[UserModel]:
        """
        Retrieve a user by their session ID (SID).

        :param sid: The session ID of the user to retrieve.
        :return: UserModel instance if user is found, otherwise None.
        """
        ...

    @abstractmethod
    async def create_user(self, user_in: ClientUserCreate) -> UserModel:
        """
        Create a new user.

        :param user_in: UserCreate schema containing the data for creating the new user.
        :raises BackendException: If a user with the same email already exists.
        :return: Created UserModel instance.
        """
        ...
