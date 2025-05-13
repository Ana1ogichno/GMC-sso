from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.dependencies.current_user import get_current_user
from ..consts import RoutersPath
from ..schemas import UserInDBBase

router = APIRouter()

# class UserRouters:
#     def __init__(self):
#         self.router = APIRouter()
#         self._add_routes()
#
#     def _add_routes(self):
#         self.router.add_api_route(
#             path=RoutersPath.me,
#             endpoint=self.get_user_me,
#             methods=["GET"],
#             response_model=UserInDBBase,
#         )
#
#     async def get_user_me(
#         self,
#         current_user: Annotated[UserInDBBase, Depends(get_current_user)],
#     ) -> UserInDBBase:
#         """
#         Get current user info.
#         """
#         return current_user


@router.get(path=RoutersPath.me, response_model=UserInDBBase)
async def get_user_me(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
) -> UserInDBBase:
    """
    Get current user info.
    """

    return current_user
