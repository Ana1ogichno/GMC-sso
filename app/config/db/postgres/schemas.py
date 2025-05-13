from enum import Enum


class PostgresSchemas(str, Enum):
    DEFAULT = "default"
    USERS = "users"
