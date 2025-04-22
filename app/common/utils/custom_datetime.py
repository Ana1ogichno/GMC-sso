from datetime import datetime

import pytz

from app.common.contracts.utils import ICustomDateTime
from app.config.settings import settings


class CustomDateTime(ICustomDateTime):
    """
    A utility class for working with datetime objects.

    Provides methods to retrieve the current datetime either in a naive
    (timezone-unaware) form or in a timezone-aware form based on the application's configuration.
    """

    @staticmethod
    def get_datetime() -> datetime:
        """
        Get the current UTC datetime without microseconds.

        This method returns the current datetime in the system's local timezone,
        without including the microsecond part.

        :return: A naive datetime object representing the current time (no timezone).
        """

        return datetime.now().replace(microsecond=0)

    @staticmethod
    def get_datetime_w_timezone() -> datetime:
        """
        Get the current datetime with timezone awareness.

        This method returns the current datetime localized to the timezone
        specified in the application's settings. The timezone is based on the
        `settings.postgres.TZ` configuration.

        :return: A timezone-aware datetime object.
        """

        return (
            datetime.now()
            .replace(microsecond=0)
            .astimezone(pytz.timezone(settings.postgres.TZ))
        )
