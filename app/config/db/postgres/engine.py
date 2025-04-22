from sqlalchemy.ext.asyncio import create_async_engine

from app.config.settings import settings

db_engine = create_async_engine(
    url=settings.postgres.POSTGRES_DATABASE_URL.unicode_string(),
    pool_pre_ping=True,
    pool_size=settings.postgres.POOL_SIZE,
    max_overflow=0,
)
