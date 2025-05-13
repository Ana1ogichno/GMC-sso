from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from redis import Redis


class IPostgresSessionProvider(ABC):
    """
    Abstract interface for providing PostgreSQL async sessions.

    Implementations of this interface must return an active AsyncSession instance,
    typically used within a request lifecycle or a transactional scope.

    This abstraction helps decouple database access logic from concrete session creation,
    supporting better testability and adherence to the Dependency Inversion Principle.
    """

    @abstractmethod
    def get_session(self) -> async_scoped_session[AsyncSession]:
        """
        Retrieve an active PostgreSQL async session.

        :return: Instance of AsyncSession for executing database operations.
        """
        ...


class IRedisSessionProvider(ABC):
    """
    Abstract interface for providing Redis client instances.

    Implementations of this interface must return a Redis client,
    which can be used to interact with Redis for caching, pub/sub,
    session storage, or token invalidation.

    This promotes flexibility and testability in components that rely on Redis.
    """

    @abstractmethod
    def get_client(self) -> Redis:
        """
        Retrieve an active Redis client instance.

        :return: Instance of Redis client for executing Redis operations.
        """
        ...
