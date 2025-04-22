from abc import ABC, abstractmethod
from fastapi.security import OAuth2PasswordRequestForm
from app.common.schemas import LoginToken, Msg, RefreshToken
from app.modules.user.schemas import UserInDBBase


class IAuthManagerService(ABC):
    """
    Interface for authentication management.

    This interface defines methods for authenticating users based on provided credentials
    and returning user data upon successful authentication. Implementations should handle
    authentication logic, such as verifying credentials and fetching user details.
    """

    @abstractmethod
    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> UserInDBBase:
        """
        Authenticate a user based on the provided credentials.

        :param credentials: The login credentials containing username (email) and password.
        :return: An instance of UserInDBBase with user information if authentication is successful.
        :raises BackendException: If authentication fails (e.g., incorrect credentials).
        """
        ...


class ISessionStorageService(ABC):
    """
    Abstract interface for session storage services.

    This interface defines the contract for managing user sessions.
    Concrete implementations of this interface should provide mechanisms
    for invalidating individual sessions as well as all sessions for a user.
    """

    @abstractmethod
    async def invalidate_session(self, session_id: str, expire_seconds: int):
        """
        Invalidates a specific user session.

        :param session_id: The session ID to invalidate.
        :param expire_seconds: The expiration time for the session in seconds.
        """
        ...

    @abstractmethod
    async def invalidate_all_sessions(self, user_id: str, expire_seconds: int):
        """
        Invalidates all sessions for a user.

        :param user_id: The user ID whose sessions should be invalidated.
        :param expire_seconds: The expiration time for the sessions in seconds.
        """
        ...


class ITokenService(ABC):
    """
    Abstract interface for token service.

    This interface defines the contract for working with JWT tokens.
    Implementations must provide logic for generating access/refresh token pairs
    and validating existing tokens.
    """

    @abstractmethod
    async def create_token_pair(self, payload: dict) -> LoginToken:
        """
        Generates a pair of access and refresh tokens for a given payload.

        :param payload: Dictionary containing user information to encode in the token.
        :return: LoginToken object with access and refresh tokens.
        """
        ...

    @abstractmethod
    async def validate_token(self, token: str) -> dict:
        """
        Validates the given token and returns its decoded payload.

        :param token: JWT token string to validate.
        :return: Dictionary representing the decoded token payload.
        """
        ...
