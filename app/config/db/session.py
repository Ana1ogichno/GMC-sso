from redis import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, async_scoped_session

from app.config.contracts import IPostgresSessionProvider, IRedisSessionProvider
from app.config.db.postgres.contracts import IPostgresSessionContextManager
from app.config.db.postgres.core import psql_engine
from app.config.settings import settings


class PostgresSessionProvider(IPostgresSessionProvider):
    """
    PostgresSessionProvider is responsible for providing PostgreSQL database sessions.

    This class implements the IPostgresSessionProvider interface. It provides methods
    to create and return asynchronous sessions to interact with the PostgreSQL database.
    """

    def __init__(
            self,
            context_manager: IPostgresSessionContextManager
    ):
        """
        Initializes the PostgresSessionProvider with an async session factory.
        """

        self._session_factory = async_sessionmaker(
            bind=psql_engine,
            autocommit=False,
            autoflush=False,
        )
        self._context_manager = context_manager

    def get_session(self) -> async_scoped_session[AsyncSession]:
        """
        Creates and returns a new asynchronous session for PostgreSQL.

        :return: A new AsyncSession instance for PostgreSQL.
        """

        return async_scoped_session(
            session_factory=self._session_factory,
            scopefunc=self._context_manager.get_session_context,
        )


class RedisSessionProvider(IRedisSessionProvider):
    """
    RedisSessionProvider is responsible for providing Redis client connections.

    This class implements the IRedisSessionProvider interface. It provides methods
    to create and return Redis client connections for interacting with the Redis store.
    """

    def __init__(self):
        """
        Initializes the RedisSessionProvider with a Redis client instance.
        """

        self._client = Redis(
            host=settings.redis.REDIS_HOST,
            port=settings.redis.REDIS_PORT,
        )

    def get_client(self) -> Redis:
        """
        Returns the Redis client instance.

        :return: A Redis client instance to interact with Redis.
        """

        # Providing Redis client
        return self._client
