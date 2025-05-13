from app.config.contracts import IPostgresSessionProvider
from app.config.db import PostgresSessionProvider
from app.config.db.postgres.core.dependencies import get_postgres_session_context_manager


def get_postgres_session_provider() -> IPostgresSessionProvider:
    """
    Construct and return an instance of IPostgresSessionProvider.

    This function initializes a PostgresSessionProvider with a session context manager,
    allowing it to provide context-aware PostgreSQL sessions. Typically used as a dependency
    provider in FastAPI or other service layers to abstract session retrieval logic.

    :return: An instance of IPostgresSessionProvider implementation.
    """

    return PostgresSessionProvider(
        context_manager=get_postgres_session_context_manager()
    )
