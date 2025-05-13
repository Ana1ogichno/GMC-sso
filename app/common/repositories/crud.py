import logging
from typing import TypeVar, Type, Any, Sequence

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import select, Select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.sql.base import ExecutableOption

from app.common.consts import ErrorCodesEnums
from app.common.contracts import ICrudRepository
from app.common.decorators.logger import LoggingFunctionInfo
from app.common.models import CoreModel
from app.server.middleware.exception import BackendException

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class CrudRepository(ICrudRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic asynchronous CRUD repository for SQLAlchemy models.

    Provides base methods for retrieving, creating, updating, and deleting records.
    Designed for reuse and consistency across multiple domain entities.
    """

    def __init__(
        self,
        db: async_scoped_session[AsyncSession],
        model: Type[ModelType],
        errors: ErrorCodesEnums,
        logger: logging.Logger,
    ):
        """
        Initialize the CRUD repository with model, database session, error handler, and logger.

        :param db: SQLAlchemy asynchronous session for database operations.
        :param model: SQLAlchemy ORM model class to operate on.
        :param errors: Error enumerations to raise domain-specific exceptions.
        :param logger: Logger instance used for logging internal actions.
        """

        self._db = db
        self._model = model
        self._errors = errors
        self._logger = logger

    @staticmethod
    async def _apply_options(
            query: Select, options: tuple[ExecutableOption, ...] | None
    ) -> Select:
        """
        Apply SQLAlchemy query options if any.

        :param query: SQLAlchemy Select query.
        :param options: Tuple of ExecutableOptions to apply.
        :return: Query with applied options.
        """

        if options:
            query = query.options(*options)
        return query

    async def _get_single_result(self, query: Select) -> ModelType | None:
        """
        Execute the query and return a single result.

        :param query: SQLAlchemy Select query.
        :return: Single result or None.
        """

        result: Result = await self._db.execute(query)
        return result.scalars().first()

    async def _get_all_results(self, query: Select) -> Sequence[ModelType]:
        """
        Execute the query and return all results.

        :param query: SQLAlchemy Select query.
        :return: Sequence of results.
        """

        result: Result = await self._db.execute(query)
        return result.scalars().all()

    async def _commit_and_refresh(self, db_obj: ModelType, with_commit: bool) -> None:
        """
        Helper method to commit and refresh the database object.

        :param db_obj: The database object to commit and refresh.
        :param with_commit: Whether to commit the transaction (True) or just flush (False).
        """

        if with_commit:
            await self._db.commit()
            await self._db.refresh(db_obj)
            self._logger.debug(f"{self._model.__name__} created and committed")
        else:
            await self._db.flush()
            self._logger.debug(f"{self._model.__name__} created and flushed")

    @LoggingFunctionInfo(
        description="Fetch a single record by its SID from the database"
    )
    async def get_by_sid(
        self, sid: Any, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        """
        Retrieve a single object by its SID.

        :param sid: Unique identifier of the model.
        :param custom_options: Optional SQLAlchemy query options.
        :return: Found model or None.
        """

        query = await self._apply_options(
            query=select(self._model).where(self._model.sid == sid),    # noqa
            options=custom_options
        )

        self._logger.debug(f"Fetching {self._model.__name__} by SID: {sid}")
        return await self._get_single_result(query)

    @LoggingFunctionInfo(
        description="Retrieve all records of the model from the database"
    )
    async def get_all(
        self, custom_options: tuple[ExecutableOption, ...] = None
    ) -> Sequence[ModelType]:
        """
        Retrieve all records for the model.

        :param custom_options: Optional SQLAlchemy query options.
        :return: List of all model instances.
        """

        query = await self._apply_options(
            query=select(self._model),
            options=custom_options
        )

        self._logger.debug(f"Fetching all {self._model.__name__} records")
        return await self._get_all_results(query)

    @LoggingFunctionInfo(
        description="Create a new record in the database"
    )
    async def create(
        self, *, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        """
        Create a new record in the database.

        :param obj_in: Input data for creation.
        :param with_commit: Whether to commit the transaction immediately.
        :return: Created model instance.
        """

        try:
            db_obj = self._model(**obj_in.model_dump())
            self._db.add(db_obj)

            await self._commit_and_refresh(db_obj, with_commit)

            return db_obj
        except IntegrityError as e:
            self._logger.debug(f"Failed to create {self._model.__name__} due to IntegrityError")
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e

    @LoggingFunctionInfo(
        description="Update an existing record in the database"
    )
    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """
        Update an existing record in the database.

        :param db_obj: The current database model instance.
        :param obj_in: Input data as dict or UpdateSchemaType.
        :return: Updated model instance.
        """

        try:
            update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            self._db.add(db_obj)
            await self._db.commit()
            await self._db.refresh(db_obj)

            self._logger.debug(f"{self._model.__name__} with SID={getattr(db_obj, 'sid', '?')} updated")

            return db_obj
        except IntegrityError as e:
            self._logger.debug(f"Failed to update {self._model.__name__} due to IntegrityError")
            raise BackendException(error=self._errors.Common.NOT_UNIQUE) from e

    @LoggingFunctionInfo(
        description="Delete a record from the database by its SID"
    )
    async def delete(self, *, sid: Any, with_commit: bool = True) -> ModelType | None:
        """
        Delete a record by its SID.

        :param sid: Unique identifier of the model to delete.
        :param with_commit: Whether to commit the transaction immediately.
        :return: Deleted model instance or None if not found.
        """

        obj = await self.get_by_sid(sid)
        if obj is None:
            self._logger.debug(f"{self._model.__name__} with SID={sid} not found for deletion")
            return None

        await self._db.delete(obj)

        if with_commit:
            await self._db.commit()
            self._logger.debug(f"{self._model.__name__} with SID={sid} deleted and committed")
        else:
            await self._db.flush()
            self._logger.debug(f"{self._model.__name__} with SID={sid} deleted and flushed")

        return obj
