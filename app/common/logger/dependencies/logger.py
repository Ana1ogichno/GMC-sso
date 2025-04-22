import logging
from typing import Annotated

from fastapi import Depends

from app.common.consts import LoggerConfigEnums
from app.common.consts.dependencies import get_logger_config
from app.common.contracts import ILoggerManager
from app.common.logger import LoggerManager


def get_logger_manager(
    config: Annotated[LoggerConfigEnums, Depends(get_logger_config)],
) -> LoggerManager:
    """
    Dependency provider for LoggerManager with injected configuration.

    :param config: Logger configuration enums.
    :return: Initialized LoggerManager instance.
    """
    return LoggerManager(config)


def get_base_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Retrieve the base logger instance.

    :param manager: LoggerManager instance.
    :return: Configured base logger.
    """
    return manager.get_base_logger()


def get_crud_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Retrieve the CRUD logger instance.

    :param manager: LoggerManager instance.
    :return: Configured CRUD logger.
    """
    return manager.get_crud_logger()


def get_auth_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Retrieve the authentication logger instance.

    :param manager: LoggerManager instance.
    :return: Configured authentication logger.
    """
    return manager.get_auth_logger()


def get_user_logger(
    manager: Annotated[ILoggerManager, Depends(get_logger_manager)],
) -> logging.Logger:
    """
    Retrieve the user logger instance.

    :param manager: LoggerManager instance.
    :return: Configured user logger.
    """
    return manager.get_user_logger()
