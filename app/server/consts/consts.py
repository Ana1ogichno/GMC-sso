from contextvars import ContextVar
from typing import Optional


session_context: ContextVar[Optional[int]] = ContextVar(
    "session_context", default=None
)
