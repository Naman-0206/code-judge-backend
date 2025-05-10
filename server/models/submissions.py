from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID
from sqlmodel import DateTime, SQLModel, Field, Relationship, func
from sqlalchemy import JSON, Column, ForeignKey
import datetime as dt

if TYPE_CHECKING:
    from .users import User
    from .questions import Question


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    id: int = Field(primary_key=True)
    creator_id: UUID = Field(foreign_key="users.id")
    question_id: Optional[UUID] = Field(
        sa_column=Column(ForeignKey(
            "questions.id", ondelete="SET NULL"), nullable=True)
    )
    verdict: Optional[str]
    score: Optional[int]
    language: str
    source_code: str

    result: Optional[dict] = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(dt.timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )

    # Relationships
    creator: Optional["User"] = Relationship(back_populates="submissions")
    question: Optional["Question"] = Relationship(back_populates="submissions")
