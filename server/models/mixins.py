import datetime
from typing import Optional
from sqlmodel import DateTime, Field, Column, func, SQLModel


class TimeStampMixin(SQLModel):
    created_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        nullable=False
    )
    updated_at: Optional[datetime.datetime] = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc),
        sa_column_kwargs={"onupdate": func.now()},
        nullable=False
    )