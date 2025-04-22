from typing import Generic, TypeVar, Any, Sequence, Tuple, Dict
from abc import ABC, abstractmethod
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy.sql.base import ExecutableOption

ModelType = TypeVar("ModelType", bound="CoreModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class ICrudRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    """
    Abstract interface for generic CRUD operations on a SQLAlchemy model.
    """

    @abstractmethod
    async def get_by_sid(
        self,
        sid: Any,
        custom_options: Tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        """
        Retrieve a single record by its unique SID.

        :param sid: Unique identifier.
        :param custom_options: Optional SQLAlchemy loader options.
        :return: A single model instance or None.
        """
        ...

    @abstractmethod
    async def get_all(
        self,
        custom_options: Tuple[ExecutableOption, ...] = None
    ) -> Sequence[ModelType]:
        """
        Retrieve all records of the model.

        :param custom_options: Optional SQLAlchemy loader options.
        :return: A sequence of model instances.
        """
        ...

    @abstractmethod
    async def create(
        self,
        obj_in: CreateSchemaType,
        with_commit: bool = True
    ) -> ModelType:
        """
        Create a new record in the database.

        :param obj_in: Input schema instance.
        :param with_commit: Whether to immediately commit the transaction.
        :return: The newly created model instance.
        """
        ...

    @abstractmethod
    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any],
        with_commit: bool = True
    ) -> ModelType:
        """
        Update an existing record with new data.

        :param db_obj: The current persisted model instance.
        :param obj_in: Updated data as dict or schema.
        :param with_commit: Whether to commit the transaction.
        :return: Updated model instance.
        """
        ...

    @abstractmethod
    async def delete(
        self,
        sid: Any,
        with_commit: bool = True
    ) -> ModelType | None:
        """
        Delete a record by its unique SID.

        :param sid: Unique identifier of the object to delete.
        :param with_commit: Whether to commit the transaction after deletion.
        :return: The deleted model instance or None.
        """
        ...
