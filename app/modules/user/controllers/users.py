from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.consts import RequestTypes
from app.common.dependencies.current_user import get_current_user
from ..consts import ControllerPath
from ..contracts import IUserControllers
from ..schemas import UserInDBBase


class UserControllers(IUserControllers):
    """
    Routing class for user-related API endpoints.

    This class encapsulates the setup and registration of user-specific
    HTTP routes within the application, such as retrieving the current user.
    """

    def __init__(self):
        """
        Initializes the UserRouters instance.

        Sets up an internal FastAPI APIRouter and binds all related routes.
        """

        self._controller = APIRouter()
        self._add_controllers()

    @property
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router instance with all registered user-related routes.

        This property provides access to the internal APIRouter configured with
        endpoints such as user profile retrieval, and can be used for route
        inclusion in the main application.

        :return: Configured APIRouter containing user routes.
        """

        return self._controller

    def _add_controllers(self):
        """
        Registers all user-related routes to the internal router instance.
        """

        self._controller.add_api_route(
            path=ControllerPath.me,
            endpoint=self.get_user_me,
            methods=[RequestTypes.GET],
            response_model=UserInDBBase,
        )

    @staticmethod
    async def get_user_me(
        current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    ) -> UserInDBBase:
        """
        Retrieve information about the currently authenticated user.

        :param current_user: The user object retrieved from the token/session.

        :return: A data model representing the current user.
        """
        return current_user
