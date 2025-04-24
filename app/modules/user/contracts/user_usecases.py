from abc import ABC, abstractmethod

from app.modules.user.models import UserModel
from app.modules.user.schemas import UserCreate


class IUserUseCase(ABC):
    """
    Interface for user-related business logic operations.

    This interface defines the contract for use cases involving user management,
    such as creating a new user or retrieving user information. Implementations
    must handle all required logic and delegate data access to appropriate services.
    """

    @abstractmethod
    async def create_user(self, user_in: UserCreate) -> UserModel:
        """
        Create a new user in the system.

        :param user_in: Data required to create the user.
        :return: The created user model.
        :raises BackendException: If a user with the provided email already exists.
        """
        ...
