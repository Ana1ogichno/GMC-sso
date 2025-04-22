from redis import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.config.contracts import IPostgresSessionProvider, IRedisSessionProvider
from app.config.db.postgres.engine import db_engine
from app.config.settings import settings


class PostgresSessionProvider(IPostgresSessionProvider):
    """
    PostgresSessionProvider is responsible for providing PostgreSQL database sessions.

    This class implements the IPostgresSessionProvider interface. It provides methods
    to create and return asynchronous sessions to interact with the PostgreSQL database.
    """

    def __init__(self):
        """
        Initializes the PostgresSessionProvider with an async session factory.
        """

        self._session_factory = async_sessionmaker(
            bind=db_engine,
            autocommit=False,
            autoflush=False,
        )

    def get_session(self) -> AsyncSession:
        """
        Creates and returns a new asynchronous session for PostgreSQL.

        :return: A new AsyncSession instance for PostgreSQL.
        """

        # Creating a new PostgreSQL session
        return self._session_factory()


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
