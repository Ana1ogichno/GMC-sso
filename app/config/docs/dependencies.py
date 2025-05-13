from app.common.consts.dependencies import get_error_codes
from app.config.contracts import IErrorTableFormatter, IAppDescriptionBuilder, IOpenApiTagsMetadata
from app.config.docs import ErrorTableMarkdownFormatter, AppDescriptionBuilder, OpenApiTagsMetadata


def get_error_formatter() -> IErrorTableFormatter:
    """
    Dependency provider for obtaining an error table formatter.

    This function retrieves an instance of `ErrorTableMarkdownFormatter`,
    initialized with the provided error codes enumeration, to generate
    Markdown-formatted tables of error codes for documentation purposes.

    :return: An instance of `IErrorTableFormatter` that can generate a Markdown
             table representation of the error codes.
    """

    return ErrorTableMarkdownFormatter(
        errors=get_error_codes()
    )


def get_app_description() -> IAppDescriptionBuilder:
    """
    Returns an instance of IAppDescriptionBuilder to generate the full app description.

    This function accepts an error formatter and uses it to instantiate
    the AppDescriptionBuilder, which is responsible for building the application
    description including a collapsible section for error codes.

    :return: An instance of IAppDescriptionBuilder that can be used to generate the app description.
    """

    return AppDescriptionBuilder(
        errors_formatter=get_error_formatter()
    )


def get_tags_metadata() -> IOpenApiTagsMetadata:
    """
    Retrieves the OpenAPI route group metadata.

    This function returns an instance of a class that implements the IOpenApiTagsMetadata interface.
    The returned object can then be used to access the metadata for the route groups,
    which is used for generating OpenAPI documentation.

    :return: An instance of a class implementing IOpenApiTagsMetadata containing route group metadata.
    """

    return OpenApiTagsMetadata()
