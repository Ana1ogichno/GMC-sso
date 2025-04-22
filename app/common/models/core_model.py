from typing import Any

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase, declared_attr, Mapped, mapped_column,
)

from app.common.utils import CustomDateTime


class CoreModel(DeclarativeBase):
    sid: Any

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=CustomDateTime.get_datetime
    )
    
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=CustomDateTime.get_datetime,
        onupdate=CustomDateTime.get_datetime,
    )

    @declared_attr  # SomeTableModel -> some_table
    def __tablename__(cls) -> str:
        name = cls.__name__.replace('Model', '')
        res = [name[0].lower()]
        for c in name[1:]:
            if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
                res.append('_')
                res.append(c.lower())
            else:
                res.append(c)
        cls.__name__ = ''.join(res)
        return cls.__name__
