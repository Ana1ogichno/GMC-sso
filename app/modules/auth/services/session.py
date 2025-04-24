import logging

from redis import Redis

from app.common.decorators.logger import LoggingFunctionInfo
from app.modules.auth.contracts import ISessionStorageService


class SessionStorageService(ISessionStorageService):
    """
    Service for managing user sessions in Redis.

    This class provides functionality for invalidating a specific session
    or all sessions for a user by interacting with the Redis database.
    It uses Redis to store session data and expiration times.

    Attributes:
        _redis: Redis client for interacting with the Redis database.
        _logger: Logger for recording operation logs.
    """

    def __init__(
        self,
        redis: Redis,
        logger: logging.Logger
    ):
        """
        Initializes the Redis session storage service.

        :param redis: Redis client for interacting with the database.
        :param logger: Logger for recording operation logs.
        """

        self._redis = redis
        self._logger = logger

    @LoggingFunctionInfo(
        description="Invalidates a specific session by setting its expiration in Redis."
    )
    async def invalidate_session(self, session_id: str, expire_seconds: int):
        """
        Invalidates a specific user session.

        Sets the session key in Redis with the given expiration time.

        :param session_id: The session ID.
        :param expire_seconds: The session's expiration time in seconds.
        """

        self._logger.debug(f"Invalidating session: {session_id} with expire time: {expire_seconds} seconds.")

        await self._redis.setex(
            name=session_id,
            time=expire_seconds,
            value="True",
        )

        self._logger.info(f"Session {session_id} invalidated successfully.")

    @LoggingFunctionInfo(
        description="Invalidates all sessions for a user by expiring their keys in Redis."
    )
    async def invalidate_all_sessions(self, user_id: str, expire_seconds: int):
        """
        Invalidates all sessions for a user.

        Applies session invalidation to all the user's sessions by deleting their keys from Redis.

        :param user_id: The user ID.
        :param expire_seconds: The expiration time for the sessions in seconds.
        """

        self._logger.debug(f"Invalidating all sessions for user: {user_id} with expire time: {expire_seconds} seconds.")

        keys = self._redis.keys(f"{user_id}:*")
        for key in keys:
            await self.invalidate_session(key, expire_seconds)

        self._logger.info(f"All sessions invalidated for user {user_id}.")
