import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import asyncio
import logging

from app.common.dependencies.db import get_db_session_provider
from app.config.db.postgres.init.dependencies import get_psql_initializer


class DatabasesInitializer:
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    @staticmethod
    async def _init_psql() -> None:
        """Initialize PostgreSQL database"""
        session_provider = await get_db_session_provider()
        db = session_provider.get_session()

        psql_initializer = await get_psql_initializer(db=db)

        await psql_initializer.init_db()
        await db.close()

    async def _initialize(self) -> None:
        """Main initialization method"""

        self._logger.info("Creating initial data")
        await self._init_psql()
        self._logger.info("Initial data created")

    @classmethod
    async def run(cls):
        """Class method to run the initialization"""
        initializer = cls()
        await initializer._initialize()


if __name__ == "__main__":
    asyncio.run(DatabasesInitializer.run())
