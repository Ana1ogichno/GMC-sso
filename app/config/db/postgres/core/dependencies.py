from sqlalchemy.ext.asyncio import AsyncEngine

from app.config.db.postgres.contracts import IPostgresSessionContextManager
from app.config.db.postgres.core import PostgresSessionContextManager, psql_engine


def get_psql_engine() -> AsyncEngine:
    """
    Retrieve the application's global asynchronous PostgreSQL engine.

    This function returns the initialized instance of AsyncEngine, which is used
    for creating asynchronous sessions and executing queries against the PostgreSQL database.

    Typically used in dependency injection systems or session factories to access the
    core SQLAlchemy engine for database communication.

    :return: An instance of SQLAlchemy's AsyncEngine.
    """

    return psql_engine


def get_postgres_session_context_manager() -> IPostgresSessionContextManager:
    """
    Dependency provider function that returns an instance of PostgresSessionContextManager.

    This function is typically used in dependency injection containers (e.g., FastAPI)
    to provide a concrete implementation of IPostgresSessionContextManager wherever needed.

    :return: An instance of IPostgresSessionContextManager.
    """

    return PostgresSessionContextManager()
