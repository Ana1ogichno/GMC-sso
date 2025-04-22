from fastapi import APIRouter

from app.modules.auth.routers import auth_router
from app.modules.user.routers import users_router


api_router = APIRouter()

api_router.include_router(auth_router, tags=["Auth"], prefix="/auth")
api_router.include_router(users_router, tags=["User"], prefix="/user")
