import logging
from enum import Enum

from fastapi import HTTPException
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.consts import ErrorCodesEnums
from app.config.contracts import IExceptionHandler, IExceptionMiddleware, IValidationExceptionHandler


class BackendException(HTTPException):
    cause: str = ""

    def __init__(
        self,
        error: Enum,
        *,
        cause: str = ""
    ):
        if not isinstance(error, Enum):
            raise ValueError("The provided error must be an instance of Enum")

        self.error_code = error.value[0]
        self.status_code = error.value[1]
        self.description = error.value[2]
        self.cause = cause


class BackendExceptionHandler(IExceptionHandler):
    """
    Handles BackendException errors by formatting the error response.

    This class is responsible for catching and formatting the exception
    into a structured response with error details.
    """

    @staticmethod
    async def handle(request: Request, exc: BackendException) -> JSONResponse:
        """
        Handles the BackendException and formats the error response.

        :param request: The HTTP request that triggered the exception.
        :param exc: The BackendException that needs to be handled.
        :return: A JSONResponse with the formatted error message and status code.
        """

        message = {"code": exc.error_code, "detail": exc.description, "cause": exc.cause}
        return JSONResponse(message, status_code=exc.status_code)


class ExceptionMiddleware(IExceptionMiddleware):
    """
    Middleware for handling unhandled exceptions globally in the application.

    This middleware catches any uncaught exceptions during the request processing
    and logs them while returning a structured error response with error details.
    """

    def __init__(
        self,
        logger: logging.Logger,
        errors: ErrorCodesEnums
    ):
        """
        Initialize the middleware with a logger and error codes.

        :param logger: The logger used for logging exceptions.
        :param errors: An instance of IErrorCodesEnums to retrieve error codes.
        """

        self._logger = logger
        self._errors = errors

    async def __call__(self, request: Request, call_next):
        """
        Process the request and handle any unhandled exceptions globally.

        :param request: The incoming HTTP request.
        :param call_next: The next handler to process the request.
        :return: A JSONResponse with error details in case of an unhandled exception.
        """

        try:
            return await call_next(request)
        except Exception as error:
            self._logger.warning(f"{error}")
            undefined_error = BackendException(self._errors.Common.UNDEFINED)

            return JSONResponse(
                content={
                    "code": undefined_error.error_code,
                    "detail": undefined_error.description,
                },
                status_code=undefined_error.status_code,
            )


class ValidationExceptionHandler(IValidationExceptionHandler):
    """
    Handles validation errors, such as those caused by RequestValidationError.

    This class formats the validation exception into a structured JSON response,
    including error details and additional validation error data.
    """

    def __init__(
        self,
        logger,
        errors: ErrorCodesEnums
    ):
        """
        Initialize the validation exception handler with a logger and error codes.

        :param logger: The logger used for logging validation errors.
        :param errors: An instance of IErrorCodesEnums to retrieve error codes.
        """

        self._logger = logger
        self._errors = errors

    async def handle(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        """
        Handle validation exception and format the error response.

        :param request: The HTTP request that caused the validation error.
        :param exc: The RequestValidationError to handle.
        :return: A JSONResponse with validation error details and additional data.
        """

        unprocessable_entity_error = BackendException(self._errors.Common.UNPROCESSABLE_ENTITY)
        exc_str = f"{exc}".replace("   ", " ")
        self._logger.error(f"{request}: {exc_str}")
        content = {
            "status_code": unprocessable_entity_error.status_code,
            "message": unprocessable_entity_error.description,
            "data": exc.__dict__.get("_errors", []),
        }
        return JSONResponse(content=content, status_code=unprocessable_entity_error.status_code)
