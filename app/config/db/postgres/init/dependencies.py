from sqlalchemy.ext.asyncio import AsyncSession

from app.common.consts.dependencies import get_logger_config, get_error_codes
from app.common.logger.dependencies import get_user_logger
from app.common.logger.dependencies.logger import get_logger_manager
from app.common.utils.dependencies import get_password_helper
from app.config.db.postgres.init.init_db import PostgresInitializer
from app.modules.user.repositories.dependencies import get_user_repository
from app.modules.user.services.dependencies import get_user_service


async def get_psql_initializer(
    db: AsyncSession,
) -> PostgresInitializer:
    """
    Provides a fully initialized PostgresInitializer instance with all dependencies.

    This factory function assembles all necessary components for database initialization,
    including logging, error handling, password utilities, and user services, then
    returns a configured PostgresInitializer instance.

    :param db: Async database session provided by the PostgresSessionProvider.
             This session will be used for all database operations during initialization.
    :return: Fully configured PostgresInitializer instance ready for database initialization tasks.
    """

    # Initialize logging components
    config = get_logger_config()
    manager = get_logger_manager(config)
    logger = get_user_logger(manager)

    # Load error codes for consistent error handling
    error_codes = get_error_codes()

    # Get password helper for secure password operations
    password_helper = get_password_helper()

    # Initialize user repository with database access and utilities
    user_repository = await get_user_repository(
        db=db,
        logger=logger,
        error_codes=error_codes,
    )

    # Create user service with business logic capabilities
    user_service = await get_user_service(
        logger=logger,
        error_codes=error_codes,
        password_helper=password_helper,
        user_repository=user_repository
    )

    # Return fully configured database initializer
    return PostgresInitializer(db=db, user_service=user_service)
