from uuid import UUID
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Relationship, func
from typing import Optional, Literal
import datetime



class SubmissionEvent(BaseModel):
    submission_id: int
    language: Literal["c", "cpp", "python"]
    source_code: str
    time_limit: int
    memory_limit: int
    question_id: str



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

class Testcase(TimeStampMixin, SQLModel, table=True):
    __tablename__ = "testcases"

    id: int = Field(primary_key=True)
    input: str
    output: str
    name: Optional[str] = Field(default=None, max_length=500)
    is_sample: bool = Field(default=False)

    question_id: UUID = Field(foreign_key="questions.id")

    # Many-to-one relationship: Each Testcase belongs to one Question
    # question = Relationship(back_populates="testcases")