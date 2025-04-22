from app.modules.auth.consts import AuthUseCaseEnums


def get_auth_usecase_enums() -> AuthUseCaseEnums:
    """
    Dependency provider for authentication-related enums.

    Returns an instance of AuthServiceEnums that encapsulates constants
    and error identifiers used throughout the authentication domain.

    :return: Instance implementing IAuthServiceEnums.
    """

    return AuthUseCaseEnums()
