from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import DateTime, Field, SQLModel, Relationship, Column, func

if TYPE_CHECKING:
    from .users import User
    from .testcases import Testcase
    from .submissions import Submission


class Question(SQLModel, table=True):
    __tablename__ = "questions"

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    title: str
    body: str
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    )

    # One-to-many relationship: One Question has many Testcases
    testcases: List["Testcase"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # One-to-many relationship: One Question has many Submissions
    submissions: List["Submission"] = Relationship(back_populates="question")

    creator_id: UUID = Field(foreign_key="users.id")
    creator: Optional["User"] = Relationship(back_populates="questions")
