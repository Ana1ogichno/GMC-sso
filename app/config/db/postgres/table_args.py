from app.config.db.postgres.schemas import Schemas


def table_args(schema: Schemas, comment: str | None = None):
    comment = comment if comment else f"{schema.value} module schema"

    return {
        "schema": schema.value,
        "comment": comment
    }
