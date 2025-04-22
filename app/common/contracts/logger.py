from abc import ABC, abstractmethod
import logging


class ILoggerManager(ABC):
    """
    Interface for a logger manager that provides access to various
    loggers used throughout the application.

    Each logger should be configured according to the project’s
    logging standards (level, format, handlers, etc.).
    """

    @abstractmethod
    def get_base_logger(self) -> logging.Logger:
        """Returns the base application logger (general-purpose logging)."""
        ...

    @abstractmethod
    def get_crud_logger(self) -> logging.Logger:
        """Returns the logger used for logging CRUD operations."""
        ...

    @abstractmethod
    def get_auth_logger(self) -> logging.Logger:
        """Returns the logger used for authentication and authorization logic."""
        ...

    @abstractmethod
    def get_user_logger(self) -> logging.Logger:
        """Returns the logger used for user-related domain logic."""
        ...
