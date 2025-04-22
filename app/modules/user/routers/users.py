from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.dependencies.current_user import get_current_user
from ..consts import RoutersPath
from ..schemas import UserInDBBase

router = APIRouter()


@router.get(path=RoutersPath.me, response_model=UserInDBBase)
async def get_user_me(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
) -> UserInDBBase:
    """
    Get current user info.
    """

    return current_user
