from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

from .questions import Question
from .submissions import Submission
from .mixins import TimeStampMixin

class User(TimeStampMixin, SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=500)
    email: str = Field(max_length=500, unique=True)
    firebase_id: Optional[str] = Field(default=None, max_length=500, unique=True)
    username: str = Field(max_length=15, unique=True)
    password: str = Field(max_length=100)

    # Relationships
    questions: List["Question"] = Relationship(back_populates="creator")
    submissions: List["Submission"] = Relationship(back_populates="creator")
