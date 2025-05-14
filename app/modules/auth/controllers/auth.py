from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from app.common.consts import RequestTypes
from app.common.dependencies import oauth2_scheme
from app.common.dependencies.current_user import get_current_user
from app.common.schemas import LoginToken, RefreshToken, Msg

from ..consts import ControllersPath
from ..contracts import IAuthUseCase
from ..contracts.auth_controllers import IAuthControllers
from ..usecases.dependencies import get_auth_usecase
from ...user.contracts import IUserUseCase
from ...user.schemas import UserInDBBase, UserCreate
from ...user.usecases.dependencies import get_user_usecase


class AuthControllers(IAuthControllers):
    """
    Routing class for authentication-related API endpoints.

    This class is responsible for configuring and registering routes related
    to authentication workflows such as login, logout, token refresh, and user registration.
    """

    def __init__(self):
        """
        Initializes the AuthRouters instance.

        Sets up an internal FastAPI APIRouter and binds all authentication-related routes.
        """

        self._controller = APIRouter()
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router instance with all registered authentication endpoints.

        :return: Configured APIRouter for inclusion in the main FastAPI application.
        """

        return self._controller

    def _add_controllers(self):
        """
        Registers all authentication-related routes to the internal router instance.
        """

        self._controller.add_api_route(
            path=ControllersPath.login,
            endpoint=self.login,
            methods=[RequestTypes.POST],
            response_model=LoginToken,
        )

        self._controller.add_api_route(
            path=ControllersPath.refresh,
            endpoint=self.update_access_token,
            methods=[RequestTypes.POST],
            response_model=LoginToken,
        )

        self._controller.add_api_route(
            path=ControllersPath.logout,
            endpoint=self.logout,
            methods=[RequestTypes.POST],
            response_model=Msg,
        )

        self._controller.add_api_route(
            path=ControllersPath.register,
            endpoint=self.register,
            methods=[RequestTypes.POST],
            response_model=UserInDBBase,
        )

    @staticmethod
    async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_service: Annotated[IAuthUseCase, Depends(get_auth_usecase)],
    ) -> LoginToken:
        """
        Authenticate user using form credentials and return a token pair.

        :param form_data: Login form data (username and password).
        :param auth_service: Authentication use case instance.
        :return: JWT access and refresh tokens.
        """

        return await auth_service.get_token_pair(form_data=form_data)

    @staticmethod
    async def update_access_token(
        refresh_token: Annotated[RefreshToken, Depends()],
        auth_service: Annotated[IAuthUseCase, Depends(get_auth_usecase)],
    ) -> LoginToken:
        """
        Refresh access token using a valid refresh token.

        :param refresh_token: Refresh token from the client.
        :param auth_service: Authentication use case instance.
        :return: New access and refresh tokens.
        """

        return await auth_service.update_access_token(refresh_token)

    @staticmethod
    async def logout(
        token: Annotated[str, Depends(oauth2_scheme)],
        current_user: Annotated[UserInDBBase, Depends(get_current_user)],
        auth_service: Annotated[IAuthUseCase, Depends(get_auth_usecase)],
        everywhere: bool = Query(False, description="Log out from all devices"),
    ) -> JSONResponse:
        """
        Invalidate tokens and log the user out.

        :param token: Access token from the request header.
        :param current_user: Authenticated user from the session.
        :param auth_service: Authentication use case instance.
        :param everywhere: Flag to log out from all devices.
        :return: Success message as JSONResponse.
        """

        return JSONResponse(
            content=await auth_service.delete_tokens(
                token=token,
                user=current_user,
                everywhere=everywhere
            ),
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def register(
        user_in: UserCreate,
        user_usecase: Annotated[IUserUseCase, Depends(get_user_usecase)],
    ):
        """
        Register a new user in the system.

        :param user_in: Data required to create a new user.
        :param user_usecase: User use case instance.
        :return: Created user data.
        """

        return await user_usecase.create_user(user_in=user_in)
