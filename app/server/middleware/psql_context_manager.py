from typing import Callable, Awaitable

from starlette.requests import Request
from starlette.responses import Response

from app.common.consts import ErrorCodesEnums
from app.config.contracts import IPostgresSessionProvider
from app.config.db.postgres.contracts import IPostgresSessionContextManager
from app.server.contracts.middleware import IPostgresContextSessionMiddleware


class PostgresContextSessionMiddleware(IPostgresContextSessionMiddleware):
    """
    ASGI middleware that manages PostgreSQL session context per request.

    This middleware is responsible for:
    - Setting a unique session context identifier (based on the request hash).
    - Ensuring that database session resources are properly initialized and disposed.
    - Handling unexpected errors gracefully with standardized error responses.

    It integrates with a session provider and a context manager to make the session
    lifecycle transparent to downstream application components, improving separation of concerns
    and enabling consistent error handling.
    """

    def __init__(
        self,
        errors: ErrorCodesEnums,
        postgres_session_provider: IPostgresSessionProvider,
        postgres_session_context_manager: IPostgresSessionContextManager
    ):
        """
        Initialize the middleware with dependencies for error handling and session management.

        :param errors: Enum class containing standardized error codes and status codes.
        :param postgres_session_provider: Provider responsible for returning the current DB session.
        :param postgres_session_context_manager: Manages the current session context identifier.
        """

        self._errors = errors
        self._postgres_session_provider = postgres_session_provider
        self._postgres_session_context_manager = postgres_session_context_manager

    async def __call__(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process an incoming HTTP request.

        Sets a unique session context ID based on the request hash, invokes the next handler,
        and ensures cleanup of session resources regardless of success or failure.

        :param request: Incoming HTTP request.
        :param call_next: The next handler in the ASGI middleware stack.
        :return: HTTP response from the next handler or a generic error response.
        """

        try:
            self._postgres_session_context_manager.set_session_context(session_id=hash(request))
            response = await call_next(request)
            return response
        except Exception:
            return Response(
                "Internal server error", status_code=self._errors.Common.UNDEFINED
            )
        finally:
            await self._postgres_session_provider.get_session().remove()
            self._postgres_session_context_manager.remove_session_context()
