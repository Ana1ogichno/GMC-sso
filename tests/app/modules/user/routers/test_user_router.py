import pytest

from datetime import datetime
from uuid import UUID

from app.modules.user.routers.users import get_user_me
from app.modules.user.schemas import UserInDBBase


class TestUserRouter:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "in_value, expected, result",
        [
            (
                UserInDBBase(
                    email="test@email.ru",
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50),
                ),
                UserInDBBase(
                    email="test@email.ru",
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50)
                ),
                True
            ),
            (
                UserInDBBase(
                    email="test@email.ru",
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50),
                ),
                UserInDBBase(
                    email="invalid@email.ru",
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50)
                ),
                False
            ),
        ],
        ids=[
            "valid_user",
            "invalid_user"
        ]
    )
    async def test_get_user_me(in_value, expected, result):
        out_value = await get_user_me(current_user=in_value)

        assert (out_value == expected) is result
