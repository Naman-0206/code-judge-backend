from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime
from .questions import Question
from .mixins import TimeStampMixin

class Testcase(TimeStampMixin, SQLModel, table=True):
    __tablename__ = "testcases"

    id: int = Field(primary_key=True)
    input_url: str
    output_url: str
    time_limit: Optional[int] = Field(default=None)
    memory_limit: Optional[int] = Field(default=None)
    name: Optional[str] = Field(default=None, max_length=500)
    is_sample: bool = Field(default=False)

    question_id: UUID = Field(foreign_key="questions.id")

    # Many-to-one relationship: Each Testcase belongs to one Question
    question: Optional[Question] = Relationship(back_populates="testcases")