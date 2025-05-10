from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from .mixins import TimeStampMixin

if TYPE_CHECKING:
    from .users import User
    from .testcases import Testcase
    from .submissions import Submission


class Question(TimeStampMixin, SQLModel, table=True):
    __tablename__ = "questions"

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    title: str
    body: str
    time_limit: Optional[int] = Field(default=10)
    memory_limit: Optional[int] = Field(default=512)

    # One-to-many relationship: One Question has many Testcases
    testcases: List["Testcase"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # One-to-many relationship: One Question has many Submissions
    submissions: List["Submission"] = Relationship(back_populates="question")

    creator_id: str = Field(foreign_key="users.id")
    creator: Optional["User"] = Relationship(back_populates="questions")
