from dataclasses import dataclass
from enum import Enum
from typing import Type


class StringEnum(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


@dataclass(frozen=True)
class LoggerConfig:
    name: str
    level: str
    format: str


class LoggerFormatEnum(StringEnum):
    """Defines different formats for logging."""

    BASE = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) %(message)s"


class LoggerLevelEnum(StringEnum):
    """Defines the available log levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerNameEnum(StringEnum):
    """Defines predefined logger names."""

    AUTH = "AUTH"
    CRUD = "CRUD"
    BASE = "BASE"
    USER = "USER"


class LoggerConfigEnum(Enum):
    """Centralized container for logger configuration presets."""
    BASE = LoggerConfig(LoggerNameEnum.BASE, LoggerLevelEnum.INFO, LoggerFormatEnum.BASE)
    AUTH = LoggerConfig(LoggerNameEnum.AUTH, LoggerLevelEnum.INFO, LoggerFormatEnum.BASE)
    CRUD = LoggerConfig(LoggerNameEnum.CRUD, LoggerLevelEnum.INFO, LoggerFormatEnum.BASE)
    USER = LoggerConfig(LoggerNameEnum.USER, LoggerLevelEnum.INFO, LoggerFormatEnum.BASE)


class LoggerConfigEnums:
    """
    Centralized container for all grouped logger-related enums.
    """

    Format: Type[LoggerFormatEnum] = LoggerFormatEnum
    Level: Type[LoggerLevelEnum] = LoggerLevelEnum
    Name: Type[LoggerNameEnum] = LoggerNameEnum
    Config: Type[LoggerConfigEnum] = LoggerConfigEnum


class RequestTypes(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"
    TRACE = "TRACE"
    CONNECT = "CONNECT"
