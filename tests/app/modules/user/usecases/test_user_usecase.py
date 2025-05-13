from datetime import datetime
from uuid import UUID

import pytest

from app.modules.user.models import UserModel
from app.modules.user.schemas import ClientUserCreate
from app.modules.user.usecases import UserUseCase


class TestUserUseCase:

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "in_value, service_out_value, expected, result",
        [
            # Success testcase
            (
                ClientUserCreate(
                    email="test@email.ru",
                    password="test_password",
                ),
                UserModel(
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    email="test@email.ru",
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50),
                ),
                UserModel(
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    email="test@email.ru",
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50),
                ),
                True
            ),

            # Unsuccessful testcase
            (
                ClientUserCreate(
                    email="test@email.ru",
                    password="test_password",
                ),
                UserModel(
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    email="invalid@email.ru",
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50),
                ),
                UserModel(
                    sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    email="test@email.ru",
                    hashed_password="test_hashed_password",
                    created_at=datetime(2025, 5, 12, 15, 52, 50),
                    updated_at=datetime(2025, 5, 12, 15, 52, 50),
                ),
                False
            ),
        ],
        ids=[
            "valid_create_user",
            "invalid_create_user"
        ]
    )
    async def test_create_user(in_value, service_out_value, expected, result, user_service_mock):

        user_service_mock.create_user.return_value = service_out_value

        user_usecase = UserUseCase(user_service=user_service_mock)

        out_value = await user_usecase.create_user(user_in=in_value)

        assert (out_value.email == expected.email) is result

