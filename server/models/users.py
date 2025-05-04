from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from .questions import Question
from .submissions import Submission

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(primary_key=True)
    name: str = Field(max_length=500)
    email: str = Field(max_length=500, unique=True)
    firebase_id: Optional[str] = Field(default=None, max_length=500, unique=True)
    created_at: datetime
    username: str = Field(max_length=15, unique=True)

    # Relationships
    questions: List["Question"] = Relationship(back_populates="creator")
    submissions: List["Submission"] = Relationship(back_populates="creator")
