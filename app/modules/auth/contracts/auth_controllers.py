from abc import ABC, abstractmethod

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from app.common.schemas import LoginToken, RefreshToken
from app.modules.user.contracts import IUserUseCase
from app.modules.user.schemas import UserInDBBase, UserCreate
from ..contracts import IAuthUseCase


class IAuthControllers(ABC):
    """
    Interface for authentication-related route definitions.

    This abstract base class defines the contract for authentication routers,
    ensuring consistent implementation of auth-related endpoints across different
    authentication providers or implementations.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router with all registered authentication endpoints.

        :return: Configured APIRouter instance containing auth routes.
        """
        ...

    @staticmethod
    @abstractmethod
    async def login(
        form_data: OAuth2PasswordRequestForm,
        auth_service: IAuthUseCase,
    ) -> LoginToken:
        """
        Authenticate user using form credentials and return a token pair.

        :param form_data: Login form data (username and password).
        :param auth_service: Authentication use case instance.
        :return: JWT access and refresh tokens.
        """
        ...

    @staticmethod
    @abstractmethod
    async def update_access_token(
        refresh_token: RefreshToken,
        auth_service: IAuthUseCase,
    ) -> LoginToken:
        """
        Refresh access token using a valid refresh token.

        :param refresh_token: Refresh token from the client.
        :param auth_service: Authentication use case instance.
        :return: New access and refresh tokens.
        """
        ...

    @staticmethod
    @abstractmethod
    async def logout(
        token: str,
        current_user: UserInDBBase,
        auth_service: IAuthUseCase,
        everywhere: bool = False,
    ) -> JSONResponse:
        """
        Invalidate tokens and log the user out.

        :param token: Access token from the request header.
        :param current_user: Authenticated user from the session.
        :param auth_service: Authentication use case instance.
        :param everywhere: Flag to log out from all devices.
        :return: Success message as JSONResponse with status 200.
        """
        ...

    @staticmethod
    @abstractmethod
    async def register(
        user_in: UserCreate,
        user_usecase: IUserUseCase,
    ) -> UserInDBBase:
        """
        Register a new user in the system.

        :param user_in: Data required to create a new user.
        :param user_usecase: User use case instance.
        :return: Created user data.
        """
        ...
