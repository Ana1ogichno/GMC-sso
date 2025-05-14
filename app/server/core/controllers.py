from fastapi import APIRouter

from app.modules.auth.controllers.dependencies import get_auth_controllers
from app.modules.user.controllers.dependencies import get_user_controllers

api_controller = APIRouter()

api_controller.include_router(get_auth_controllers().controller, tags=["Auth"], prefix="/auth")
api_controller.include_router(get_user_controllers().controller, tags=["User"], prefix="/user")
