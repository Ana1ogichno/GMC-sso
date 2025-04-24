from app.common.decorators.logger import LoggingFunctionInfo
from app.modules.user.contracts import IUserService, IUserUseCase
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserCreate


class UserUseCase(IUserUseCase):
    """
    Service for managing user-related operations.

    This service provides methods for retrieving users by email or session ID (SID),
    and creating new users. It uses the provided repository for interacting with the
    data layer and ensures that appropriate logging and error handling are in place
    for each operation.
    """

    def __init__(
        self,
        user_service: IUserService
    ):
        """
        Initialize the UserService with required dependencies.

        :param user_service: Service for accessing and managing the user repository.
        """

        self._user_service = user_service

    @LoggingFunctionInfo(
        description="Creates a new user. Checks if the email already exists. If not, the user is created."
    )
    async def create_user(self, user_in: UserCreate) -> UserModel:
        """
        Creates a new user.

        :param user_in: Data required to create the new user.
        :return: UserModel instance of the newly created user.
        :raises BackendException: If a user with the given email already exists.
        """

        return await self._user_service.create_user(user_in=user_in)
