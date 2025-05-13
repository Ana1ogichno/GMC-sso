from enum import Enum

from fastapi import HTTPException


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
