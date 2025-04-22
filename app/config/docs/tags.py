from typing import List, Dict

from app.config.contracts import IOpenApiTagsMetadata


class OpenApiTagsMetadata(IOpenApiTagsMetadata):
    """
    Holds route group metadata for OpenAPI docs.
    """

    @staticmethod
    def get_tags_metadata() -> List[Dict[str, str]]:
        return [
            {"name": "User", "description": "User logic"},
            {"name": "Auth", "description": "Basic login/logout logic"},
            # ...extend here as needed
        ]
