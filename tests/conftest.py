import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import logging

import pytest

from app.common.consts.dependencies import get_error_codes
from app.common.contracts import IPasswordHelper
from app.modules.user.contracts import IUserService, IUserRepository


@pytest.fixture()
def logger_mock(mocker):
    return mocker.Mock(logging.Logger)


@pytest.fixture()
def error_codes():
    return get_error_codes()


@pytest.fixture
def user_service_mock(mocker):
    return mocker.Mock(IUserService)


@pytest.fixture
def password_helper_mock(mocker):
    return mocker.Mock(IPasswordHelper)


@pytest.fixture
def user_repository_mock(mocker):
    return mocker.Mock(IUserRepository)

