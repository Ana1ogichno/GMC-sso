from abc import ABC, abstractmethod
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class IExceptionHandler(ABC):
    """
        Interface for handling exceptions in a structured way.

        This interface defines the contract for any exception handler class.
        The handler should catch an exception, process it, and return a structured
        JSONResponse with appropriate error details and status code.
    """

    @staticmethod
    @abstractmethod
    async def handle(request: Request, exc: Exception) -> JSONResponse:
        """
        Abstract method to handle exceptions and format error responses.

        :param request: The HTTP request that triggered the exception.
        :param exc: The exception that needs to be handled.
        :return: A structured JSONResponse with the error details.
        """
        ...


class IExceptionMiddleware(ABC):
    """
    Interface for middleware that handles unhandled exceptions globally.

    All middleware that handles exceptions should implement this interface.
    """

    @abstractmethod
    async def __call__(self, request: Request, call_next):
        """
        Handles unhandled exceptions and processes the request accordingly.

        :param request: The incoming HTTP request.
        :param call_next: The next handler to process the request.
        :return: A JSONResponse with error details if an exception occurs.
        """
        ...


class IValidationExceptionHandler(ABC):
    """
    Interface for handling validation exceptions, such as RequestValidationError.

    All classes handling validation errors should implement this interface.
    """

    @abstractmethod
    async def handle(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        Handles validation exceptions and formats the error response.

        :param request: The HTTP request that triggered the validation error.
        :param exc: The RequestValidationError to handle.
        :return: A structured JSONResponse with validation error details.
        """
        ...
