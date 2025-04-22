from abc import ABC, abstractmethod
from typing import List, Dict


class IErrorTableFormatter(ABC):
    """
    Interface for a class that formats application error codes
    into a string representation (e.g., Markdown) for documentation.
    """

    @abstractmethod
    def generate_table(self) -> str:
        """
        Generate a formatted table of error codes.

        :return: A string containing the formatted table (e.g., Markdown).
        """
        ...


class IAppDescriptionBuilder(ABC):
    """
    Interface for the application description builder.

    This interface defines the structure for building an app description
    that includes an error codes section, generated as a Markdown table.
    """

    def build_description(self) -> str:
        """
        Builds the complete application description with the error codes section.

        :return: A string representing the full application description, including the error codes in Markdown format.
        """
        ...


class IOpenApiTagsMetadata(ABC):
    """
    Interface for obtaining route group metadata for OpenAPI documentation.
    """

    @staticmethod
    @abstractmethod
    def get_tags_metadata() -> List[Dict[str, str]]:
        """
        Retrieves metadata for route groups in OpenAPI.

        :return: A list of dictionaries, each representing a route tag with its name and description.
        """
        ...
