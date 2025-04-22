from enum import Enum
from typing import Type


class CommonError(Enum):
    """Common system-level errors not specific to a single domain."""

    UNDEFINED = (0, 500, "Unknown error")
    NOT_UNIQUE = (1, 400, "Non-unique field(s) during creation")
    UNPROCESSABLE_ENTITY = (2, 422, "Unprocessable entity")


class TokenError(Enum):
    """Errors related to JWT access and refresh token handling."""

    BAD_REFRESH_TOKEN = (100, 401, "Invalid refresh token")
    BAD_ACCESS_TOKEN = (101, 401, "Invalid access token")
    INVALID_TOKEN = (102, 402, "Invalid token forma")


class UserError(Enum):
    """Errors related to user authentication and identity."""

    NOT_ALLOWED = (200, 403, "Access denied")
    INCORRECT_CREDENTIALS = (201, 401, "Incorrect login or password")
    USER_NOT_FOUND = (202, 404, "User not found")
    EMAIL_ALREADY_EXISTS = (203, 400, "A user with this email already exists")


class ErrorCodesEnums:
    """
    Centralized container for all grouped domain-specific error enums.
    """

    def __init__(self):
        self.Common = CommonError
        self.Token = TokenError
        self.User = UserError
