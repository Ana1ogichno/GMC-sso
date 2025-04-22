from app.common.consts import ErrorCodesEnums
from app.config.contracts import IErrorTableFormatter


class ErrorTableMarkdownFormatter(IErrorTableFormatter):
    """
    Generates a Markdown-formatted table of error codes for API documentation.

    This class accepts a centralized container of grouped error enums (e.g., user, token, common)
    and produces a Markdown table that can be embedded in API descriptions or docs.
    """

    def __init__(
            self,
            errors: ErrorCodesEnums,
    ):
        """
        Initialize the formatter with a centralized error enumeration container.

        :param errors: An implementation of IErrorCodesEnums that contains grouped error enums.
        """

        self._errors = errors

    def generate_table(self) -> str:
        """
        Generate a Markdown table of error codes from the provided error enums.

        :return: A string representing the Markdown table of error codes.
        """

        rows = []

        for attr_name, attr_value in vars(self._errors).items():
            for error in attr_value:
                rows.append(f"| {error.value[0]} | {error.value[1]} | {error.value[2]}")

        return "\n".join(rows)
