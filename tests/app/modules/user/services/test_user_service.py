from datetime import datetime
from uuid import UUID

import pytest

from app.config.exception import BackendException
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserInDBBase, ClientUserCreate
from app.modules.user.services import UserService


class TestUserService:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "in_value, repository_out_value, expected, result",
        [
            # Success testcase
            (
                    {
                        "email": "test@email.ru",
                        "custom_options": None
                    },
                    UserInDBBase(
                        sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                        email="test@email.ru",
                        hashed_password="test_hashed_password",
                        created_at=datetime(2025, 5, 12, 15, 52, 50),
                        updated_at=datetime(2025, 5, 12, 15, 52, 50),
                    ),
                    UserInDBBase(
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
                    {
                        "email": "test@email.ru",
                        "custom_options": None
                    },
                    UserInDBBase(
                        sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                        email="invalid@email.ru",
                        hashed_password="test_hashed_password",
                        created_at=datetime(2025, 5, 12, 15, 52, 50),
                        updated_at=datetime(2025, 5, 12, 15, 52, 50),
                    ),
                    UserInDBBase(
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
            "valid_get_user_by_email",
            "invalid_get_user_by_email"
        ]
    )
    async def test_get_user_by_email(
            in_value,
            repository_out_value,
            expected,
            result,
            error_codes,
            logger_mock,
            password_helper_mock,
            user_repository_mock
    ):
        user_repository_mock.get_by_email.return_value = repository_out_value

        user_service = UserService(
            errors=error_codes,
            logger=logger_mock,
            password_helper=password_helper_mock,
            user_repository=user_repository_mock
        )

        out_value = await user_service.get_user_by_email(
            email=in_value["email"],
            custom_options=in_value["custom_options"]
        )

        assert (out_value.email == expected.email) is result

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "in_sid, repository_out_value, expected, result",
        [
            # Success testcase
            (
                    UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
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
                    UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                    UserModel(
                        sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                        email="test@email.ru",
                        hashed_password="test_hashed_password",
                        created_at=datetime(2025, 5, 12, 15, 52, 50),
                        updated_at=datetime(2025, 5, 12, 15, 52, 50),
                    ),
                    UserModel(
                        sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a1'),
                        email="test@email.ru",
                        hashed_password="test_hashed_password",
                        created_at=datetime(2025, 5, 12, 15, 52, 50),
                        updated_at=datetime(2025, 5, 12, 15, 52, 50),
                    ),
                    False
            ),
        ],
        ids=[
            "valid_get_user_by_sid",
            "invalid_get_user_by_sid"
        ]
    )
    async def test_get_user_by_sid(
            in_sid,
            repository_out_value,
            expected,
            result,
            error_codes,
            logger_mock,
            password_helper_mock,
            user_repository_mock
    ):
        user_repository_mock.get_by_sid.return_value = repository_out_value

        user_service = UserService(
            errors=error_codes,
            logger=logger_mock,
            password_helper=password_helper_mock,
            user_repository=user_repository_mock
        )

        out_value = await user_service.get_user_by_sid(sid=in_sid)

        assert (out_value.sid == expected.sid) is result

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "in_value, repository_get_out_value, password_hash, repository_create_out_value, expected, result, raise_type",
        [
            # Success testcase
            (
                    ClientUserCreate(
                        email="test@email.ru",
                        password="test_password"
                    ),
                    None,
                    "test_password_hash",
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
                    True,
                    None
            ),

            # Unsuccessful testcase
            (
                    ClientUserCreate(
                        email="test@email.ru",
                        password="test_password"
                    ),
                    UserModel(
                        sid=UUID('b84c93b1-a765-4a12-8e1d-428910af75a5'),
                        email="test@email.ru",
                        hashed_password="test_hashed_password",
                        created_at=datetime(2025, 5, 12, 15, 52, 50),
                        updated_at=datetime(2025, 5, 12, 15, 52, 50),
                    ),
                    None,
                    None,
                    None,
                    None,
                    "email_already_exist"
            ),
        ],
        ids=[
            "valid_create_user",
            "user_already_exist"
        ]
    )
    async def test_create_user(
            in_value,
            repository_get_out_value,
            password_hash,
            repository_create_out_value,
            expected,
            result,
            raise_type,
            error_codes,
            logger_mock,
            password_helper_mock,
            user_repository_mock
    ):
        user_repository_mock.get_by_email.return_value = repository_get_out_value
        user_repository_mock.create.return_value = repository_create_out_value
        password_helper_mock.get_password_hash.return_value = password_hash

        user_service = UserService(
            errors=error_codes,
            logger=logger_mock,
            password_helper=password_helper_mock,
            user_repository=user_repository_mock
        )

        if raise_type == "email_already_exist":
            with pytest.raises(BackendException) as exc_info:
                await user_service.create_user(user_in=in_value)

            assert exc_info.value.error_code == error_codes.User.EMAIL_ALREADY_EXISTS.value[0]
            assert exc_info.value.status_code == error_codes.User.EMAIL_ALREADY_EXISTS.value[1]
            assert exc_info.value.description == error_codes.User.EMAIL_ALREADY_EXISTS.value[2]

        else:
            out_value = await user_service.create_user(user_in=in_value)
            assert (out_value.sid == expected.sid) is result
