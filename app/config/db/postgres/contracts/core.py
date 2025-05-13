from abc import ABC, abstractmethod


class IPostgresSessionContextManager(ABC):
    """
    Abstract interface for managing the PostgreSQL session context.

    This interface defines methods to set, retrieve, and clear the session ID
    from the current execution context. It is useful for propagating session
    information across different layers of the application in a decoupled way,
    improving testability and adherence to the Dependency Inversion Principle.
    """

    @staticmethod
    @abstractmethod
    def get_session_context() -> int:
        """
        Retrieve the current session ID from the context.

        :return: Session ID as an integer.
        :raises ValueError: If no session is currently set.
        """
        ...

    @staticmethod
    @abstractmethod
    def set_session_context(session_id: int) -> None:
        """
        Set the session ID into the current execution context.

        :param session_id: The session ID to associate with the context.
        """
        ...

    @staticmethod
    @abstractmethod
    def remove_session_context() -> None:
        """
        Remove the session ID from the current execution context.

        This effectively resets the context to an empty state.
        """
        ...
