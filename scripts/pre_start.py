import asyncio
import logging
import sys

from sqlalchemy.sql import text
from tenacity import (
    after_log,
    before_log,
    retry,
    stop_after_attempt,
    wait_fixed
)

sys.path = ["", ".."] + sys.path[1:]

from app.common.dependencies.db import get_db_session_provider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
async def init() -> None:
    try:
        session_provider = await get_db_session_provider()
        db = session_provider.get_session()
        # Try to create session to check if DB is awake
        response = await db.execute(text("SELECT 1"))
        logger.info(f"Response value: {response.first()}")
        await db.close()
    except Exception as e:
        logger.error(e)
        raise e


async def main() -> None:
    logger.info("Ping DB")
    await init()
    logger.info("DB pong'ed")


if __name__ == "__main__":
    asyncio.run(main())
