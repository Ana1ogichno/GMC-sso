from app.config.db.postgres.contracts import IPostgresSessionContextManager
from app.server.consts import session_context


class PostgresSessionContextManager(IPostgresSessionContextManager):
    """
    Concrete implementation of IPostgresSessionContextManager for managing session IDs
    within the current execution context.

    This class uses a thread-local or context-local variable (`session_context`)
    to store a PostgreSQL session identifier. It provides static methods to set,
    retrieve, and clear the session ID. This mechanism allows different components
    to access the current session context without directly passing the session ID
    through function arguments.
    """

    @staticmethod
    def get_session_context() -> int:
        """
        Retrieve the current PostgreSQL session ID from the context.

        :return: The current session ID as an integer.
        :raises ValueError: If no session ID is currently set in the context.
        """

        session_id = session_context.get()

        if not session_id:
            raise ValueError("Currently no session is available")

        return session_id

    @staticmethod
    def set_session_context(session_id: int) -> None:
        """
        Set the PostgreSQL session ID into the current execution context.

        :param session_id: The session ID to store.
        """

        session_context.set(session_id)

    @staticmethod
    def remove_session_context() -> None:
        """
        Remove the session ID from the current execution context.
        """

        session_context.set(None)
