from app.common.consts.dependencies import get_logger_config, get_error_codes
from app.common.logger.dependencies.logger import get_logger_manager, get_base_logger
from app.config.contracts import IExceptionHandler, IExceptionMiddleware, IValidationExceptionHandler
from app.config.exception import BackendExceptionHandler, ExceptionMiddleware, ValidationExceptionHandler


def get_exception_handler() -> IExceptionHandler:
    """
    Returns an instance of BackendExceptionHandler.

    This function provides the exception handler to be used by FastAPI.
    It is responsible for handling `BackendException` errors by returning
    a structured JSON response with error details.

    :return: An instance of `BackendExceptionHandler`, which handles BackendException errors.
    """
    return BackendExceptionHandler()


def get_exception_middleware() -> IExceptionMiddleware:
    """
    Returns an instance of ExceptionMiddleware.

    This function provides the middleware that handles any uncaught exceptions
    during the request-response cycle. It logs the exception and returns a default
    error response when an unhandled error occurs.

    :return: An instance of `ExceptionMiddleware`, which handles uncaught exceptions in FastAPI.
    """

    config = get_logger_config()
    manager = get_logger_manager(config)
    logger = get_base_logger(manager)
    error_codes = get_error_codes()

    return ExceptionMiddleware(
        logger=logger,
        errors=error_codes
    )


def get_validation_exception_handler() -> IValidationExceptionHandler:
    """
    Returns an instance of ValidationExceptionHandler.

    This function provides the exception handler specifically for validation errors.
    It catches validation errors raised during request parsing and returns a structured
    JSON response with the error details.

    :return: An instance of `ValidationExceptionHandler`, which handles validation errors in FastAPI.
    """

    config = get_logger_config()
    manager = get_logger_manager(config)
    logger = get_base_logger(manager)
    error_codes = get_error_codes()

    return ValidationExceptionHandler(
        logger=logger,
        errors=error_codes
    )

