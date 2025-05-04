from typing import Optional, TYPE_CHECKING
from uuid import UUID
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import JSON, Column

if TYPE_CHECKING:
    from .users import User
    from .questions import Question


class Submission(SQLModel, table=True):
    __tablename__ = "submissions"

    id: int = Field(primary_key=True)
    creator_id: UUID = Field(foreign_key="users.id")
    question_id: Optional[UUID] = Field(
        foreign_key="questions.id", sa_column_kwargs={"on_delete": "SET NULL"}
    )
    verdict: str
    score: int

    result: dict = Field(
        default_factory=dict,
        sa_column=Column(JSON)
    )

    # Relationships
    creator: Optional["User"] = Relationship(back_populates="submissions")
    question: Optional["Question"] = Relationship(back_populates="submissions")
