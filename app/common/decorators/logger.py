import logging
from functools import wraps
from typing import Annotated

from fastapi import Depends

from app.common.logger.dependencies import get_base_logger


class LoggingFunctionInfo:
    """
    Decorator class for logging the start of an asynchronous function's execution.

    Designed for use in FastAPI dependencies or service methods. Logs function name
    and optional description when execution begins. Useful for tracing and debugging.
    """

    def __init__(
            self,
            logger: Annotated[logging.Logger, Depends(get_base_logger)],
            description: str | None = None
    ):
        """
        Initialize the LoggingFunctionInfo decorator.

        :param logger: Logger instance used for emitting debug logs.
        :param description: Optional human-readable description of the function.
        """

        self._description = description
        self._logger = logger

    def __call__(self, func):
        """
        Decorate an asynchronous function to log its invocation details.

        :param func: The async function to decorate.
        :return: Wrapped async function with logging.
        """

        @wraps(func)
        async def wrapper(*args, **kwargs):
            log_message = f"Start: {func.__name__}"
            if self._description:
                log_message += f", description: {self._description}"

            self._logger.debug(log_message)

            # Execute the original function
            result = await func(*args, **kwargs)

            return result

        return wrapper
