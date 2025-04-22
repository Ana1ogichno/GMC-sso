from .postgres_settings import PostgresSettings
from .project_settings import ProjectSettings
from .redis_settings import RedisSettings


class Settings:
    project: ProjectSettings = ProjectSettings()
    postgres: PostgresSettings = PostgresSettings()
    redis: RedisSettings = RedisSettings()


settings: Settings = Settings()
