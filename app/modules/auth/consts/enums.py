from enum import Enum
from typing import Type


class ControllersPath(str, Enum):
    """
    Enum defining the routing paths for authentication endpoints.

    Attributes:
        register: Path for user registration.
        register_by_code: Path for registration using an invitation or unique code.
        login: Path for user login.
        refresh: Path to refresh the JWT token.
        logout: Path for user logout.
    """

    register = "/register"
    register_by_code = "/{code}/register"
    login = "/login"
    refresh = "/refresh_token"
    logout = "/logout"


class AuthPayloadFields(str, Enum):
    """
    Enum representing the standard fields used in authentication token payloads.

    Attributes:
        SUB: Subject field, typically user ID.
        PERMISSIONS: List of permissions assigned to the user.
        JTI: Unique identifier for the JWT.
    """

    SUB = "sub"
    PERMISSIONS = "permissions"
    JTI = "jti"


class AuthUseCaseEnums:
    """
    Concrete implementation of IAuthServiceEnums.

    Provides access to enumerations used across the authentication service,
    such as standardized payload fields for JWT tokens.
    """

    PayloadFields: Type[AuthPayloadFields] = AuthPayloadFields
