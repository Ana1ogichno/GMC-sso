from abc import ABC, abstractmethod

from fastapi import APIRouter

from app.modules.user.schemas import UserInDBBase


class IUserControllers(ABC):
    """
    Interface for user-related route definitions.
    """

    @property
    @abstractmethod
    def controller(self) -> APIRouter:
        """
        Returns the FastAPI router with registered user routes.

        :return: Configured APIRouter instance.
        """
        pass

    @staticmethod
    @abstractmethod
    async def get_user_me(current_user: UserInDBBase) -> UserInDBBase:
        """
        Retrieve information about the currently authenticated user.

        :param current_user: The user object retrieved from the request context.
        :return: A data model representing the current user.
        """
        ...
