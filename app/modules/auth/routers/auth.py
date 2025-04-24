from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import JSONResponse

from app.common.dependencies import oauth2_scheme
from app.common.dependencies.current_user import get_current_user
from app.common.schemas import LoginToken, RefreshToken, Msg

from ..consts import RoutersPath
from ..contracts import IAuthUseCase
from ..usecases.dependencies import get_auth_usecase
from ...user.contracts import IUserUseCase
from ...user.schemas import UserInDBBase, UserCreate
from ...user.usecases.dependencies import get_user_usecase

router = APIRouter()


@router.post(path=RoutersPath.login, response_model=LoginToken)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[IAuthUseCase, Depends(get_auth_usecase)],
) -> LoginToken:
    """
    Login method (Create JWT access and refresh tokens)
    """

    return await auth_service.get_token_pair(form_data=form_data)


@router.post(path=RoutersPath.refresh, response_model=LoginToken)
async def update_access_token(
    refresh_token: Annotated[RefreshToken, Depends()],
    auth_service: Annotated[IAuthUseCase, Depends(get_auth_usecase)],
) -> LoginToken:
    """
    Method for update JWT access token
    """

    return await auth_service.update_access_token(refresh_token)


@router.post(path=RoutersPath.logout, response_model=Msg)
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    auth_service: Annotated[IAuthUseCase, Depends(get_auth_usecase)],
    everywhere: bool = Query(False, description="Log out from all devices"),
) -> JSONResponse:
    """
    Method for logout.
    """

    return JSONResponse(
        content=await auth_service.delete_tokens(
            token=token,
            user=current_user,
            everywhere=everywhere
        ),
        status_code=status.HTTP_200_OK,
    )


@router.post(path=RoutersPath.register, response_model=UserInDBBase)
async def register(
    user_in: UserCreate,
    user_usecase: Annotated[IUserUseCase, Depends(get_user_usecase)],
):
    """
    User registering.
    """

    return await user_usecase.create_user(user_in=user_in)
