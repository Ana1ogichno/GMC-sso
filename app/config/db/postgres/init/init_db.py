import logging

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.config.settings import settings
from app.modules.user.contracts import IUserService
from app.modules.user.schemas import UserCreate

# Configure logging
logging.basicConfig(level=logging.INFO)


class PostgresInitializer:
    """
    Handles database initialization including creation of initial data like superusers.

    This class provides methods to initialize database state and ensure required system data exists.
    """

    def __init__(
        self,
        db: AsyncSession,
        user_service: IUserService
    ):
        """
        Initializes the database initializer with required dependencies.

        :param db: Async database session provided by the PostgresSessionProvider
        :param user_service: Service instance for user management operations
        """

        self._db = db
        self._user_service = user_service
        self._logger = logging.getLogger(__name__)

    async def _check_superuser_exists(self, email: EmailStr) -> bool:
        """
        Checks if a superuser with given email already exists in the database.

        :param email: Email address to check for existing superuser
        :return: True if user exists, False otherwise
        """

        existing_user = await self._user_service.get_user_by_email(email=email)
        return existing_user is not None

    async def _create_superuser(self, email: EmailStr, password: str) -> None:
        """
        Creates a new superuser with provided credentials in the database.

        :param email: Email address for the new superuser
        :param password: Password for the new superuser
        """

        user_in = UserCreate(
            email=email,
            password=password,
        )
        await self._user_service.create_user(user_in=user_in)
        self._logger.info(f"Superuser created: {email}")

    async def _init_superuser(self) -> None:
        """Initializes the default superuser account if it doesn't exist."""
        email = settings.project.FIRST_SUPERUSER_LOGIN
        password = settings.project.FIRST_SUPERUSER_PASSWORD

        self._logger.info("Starting superuser initialization")

        if not await self._check_superuser_exists(email):
            await self._create_superuser(email, password)
            await self._db.commit()
            self._logger.info("Superuser successfully created")
        else:
            self._logger.info("Superuser already exists - skipping creation")

        self._logger.info("Completed superuser initialization")

    async def init_db(self) -> None:
        """
        Performs all database initialization tasks.

        Note:
            Tables should normally be created via Alembic migrations.
        """

        await self._init_superuser()
