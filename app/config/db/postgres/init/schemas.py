from uuid import UUID

from app.modules.user.schemas import UserCreate


class UserInit(UserCreate):
    sid: UUID
