from typing import AsyncGenerator

from fastapi import Depends
from redis import Redis

from app.config.contracts import IPostgresSessionProvider
from app.config.db import PostgresSessionProvider
from app.config.db.session import RedisSessionProvider


async def get_db_session_provider() -> IPostgresSessionProvider:
    """
    Returns an instance of the PostgresSessionProvider.

    This provider is responsible for creating and managing PostgreSQL session instances.

    :return: An instance of PostgresSessionProvider.
    """

    return PostgresSessionProvider()


async def get_db(
    session_provider: IPostgresSessionProvider = Depends(get_db_session_provider)
) -> AsyncGenerator:
    """
    Provides a PostgreSQL database session.

    This dependency can be used to inject a PostgreSQL database session into FastAPI routes
    or services that need to interact with the database.

    The session is automatically closed after the request lifecycle.

    :param session_provider: The provider responsible for providing PostgreSQL sessions.
    :return: A PostgreSQL database session instance.
    """

    db = session_provider.get_session()
    try:
        yield db
    finally:
        await db.close()


async def get_redis_session_provider() -> RedisSessionProvider:
    """
    Returns an instance of the RedisSessionProvider.

    This provider is responsible for creating and managing Redis client sessions.

    :return: An instance of RedisSessionProvider.
    """

    return RedisSessionProvider()


async def get_redis_client(
    session_provider: RedisSessionProvider = Depends(get_redis_session_provider)
) -> AsyncGenerator[Redis, None]:
    """
    Provides a Redis client session.

    This dependency can be used to inject a Redis client into FastAPI routes
    or services that need to interact with Redis.

    Redis clients are typically long-lived, and this dependency ensures that the client
    is available throughout the request lifecycle.

    :param session_provider: The provider responsible for providing Redis client sessions.
    :return: A Redis client instance.
    """

    redis_client = session_provider.get_client()
    try:
        yield redis_client
    finally:
        pass
