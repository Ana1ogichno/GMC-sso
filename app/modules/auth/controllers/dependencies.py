from app.modules.auth.contracts.auth_controllers import IAuthControllers
from app.modules.auth.controllers.auth import AuthControllers


def get_auth_controllers() -> IAuthControllers:
    """
    Create and return authentication router instance.

    This factory function provides the configured authentication router
    with all registered auth endpoints.

    :return: Initialized auth router implementing IAuthRouters interface
    """

    return AuthControllers()
