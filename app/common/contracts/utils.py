from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from uuid import UUID

from app.common.schemas import TokenData, LoginToken


class IPasswordHelper(ABC):
    """
   Interface for password hashing and verification operations.

   This abstraction allows different implementations of password handling logic
   (e.g., using bcrypt, Argon2, etc.) while following the Dependency Inversion Principle.
   """

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify whether a plain password matches the hashed password.

        :param plain_password: The raw password provided by the user.
        :param hashed_password: The stored hashed password to compare against.
        :return: True if the password matches, False otherwise.
        """
        ...

    @abstractmethod
    def get_password_hash(self, password: str | None) -> str | None:
        """
        Hash a plain password for secure storage.

        :param password: The raw password to hash.
        :return: A hashed representation of the password, or None if input is None.
        """
        ...


class ITokenHelper(ABC):
    """
    Interface for Token Helper, responsible for token generation, validation,
    and token pair creation in a secure manner.
    """

    @abstractmethod
    def create_token(
        self,
        data: dict,
        expires_delta: timedelta | None,
        jti: UUID,
        refresh: bool = False,
    ) -> str:
        """
        Generates a JWT token based on provided data.

        :param data: The data to be encoded in the token.
        :param expires_delta: The expiration time for the token.
        :param jti: The unique identifier for the token.
        :param refresh: Flag indicating whether the token is a refresh token.
        :return: The generated JWT token as a string.
        """
        ...

    @abstractmethod
    def token_payload(self, token: str, refresh: bool) -> TokenData:
        """
        Decodes the token and validates it, checking if it matches the expected type.

        :param token: The JWT token to be validated.
        :param refresh: Flag indicating whether to check for a refresh token.
        :return: TokenData instance containing the payload information.
        :raises BackendException: If the token is invalid or expired.
        """
        ...

    @abstractmethod
    def create_token_pair(self, payload: dict) -> LoginToken:
        """
        Creates a pair of access and refresh tokens.

        :param payload: The data to encode in the tokens.
        :return: A tuple containing the access and refresh JWT tokens.
        """
        ...


class ICustomDateTime(ABC):
    """
    Interface for datetime utilities.

    Provides methods to obtain the current datetime in either naive
    (timezone-unaware) or timezone-aware form, depending on application requirements.
    """

    @staticmethod
    @abstractmethod
    def get_datetime() -> datetime:
        """
        Get the current UTC datetime without microseconds.

        :return: Naive datetime object (without timezone).
        """
        ...

    @staticmethod
    @abstractmethod
    def get_datetime_w_timezone() -> datetime:
        """
        Get the current datetime with timezone awareness based on application settings.

        :return: Aware datetime object localized to the configured timezone.
        """
        ...


class ITokenValidator(ABC):
    """
    Interface for token validation operations.
    """

    @abstractmethod
    def validate_access_token(self, token: str) -> TokenData:
        """
        Validate an access token and return the decoded payload.

        :param token: JWT access token string.
        :return: TokenData object with decoded payload.
        :raises: BackendException or JWTError
        """
        ...

    @abstractmethod
    def validate_refresh_token(self, token: str) -> TokenData:
        """
        Validate a refresh token and return the decoded payload.

        :param token: JWT refresh token string.
        :return: TokenData object with decoded payload.
        :raises: BackendException or JWTError
        """
        ...
