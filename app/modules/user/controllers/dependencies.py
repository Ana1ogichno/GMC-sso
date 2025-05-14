from app.modules.user.contracts import IUserControllers
from app.modules.user.controllers.users import UserControllers


def get_user_controllers() -> IUserControllers:
    """
    Dependency provider for user-related API router.

    This function returns an instance of a class that implements the IUserRouters interface.
    It is intended to be used as a FastAPI dependency or for manual injection into the
    application routing layer.

    :return: Instance of IUserRouters containing configured user API routes.
    """

    return UserControllers()
