from abc import ABC, abstractmethod

from fastapi.security import OAuth2PasswordRequestForm

from app.common.schemas import LoginToken, RefreshToken, Msg
from app.modules.user.schemas import UserInDBBase


class IAuthUseCase(ABC):
    """
    Interface for the authentication service.

    Defines a contract for implementing authentication logic,
    token generation and refresh, as well as token invalidation (logout).
    """

    @abstractmethod
    async def get_token_pair(self, form_data: OAuth2PasswordRequestForm) -> LoginToken:
        """
        Authenticates a user and returns a new pair of access and refresh tokens.

        :param form_data: User credentials submitted via OAuth2 password flow.
        :return: A pair of access and refresh tokens.
        """
        ...

    @abstractmethod
    async def update_access_token(self, refresh_token: RefreshToken) -> LoginToken:
        """
        Validates a refresh token and issues a new pair of tokens.

        :param refresh_token: The refresh token provided by the client.
        :return: A new pair of access and refresh tokens.
        """
        ...

    @abstractmethod
    async def delete_tokens(self, token: str, user: UserInDBBase, everywhere: bool) -> Msg:
        """
        Invalidates tokens to log the user out.

        :param token: The access or refresh token to invalidate.
        :param user: The user requesting logout.
        :param everywhere: If True, invalidates all sessions; otherwise, only the current one.
        :return: A message indicating successful logout.
        """
        ...
