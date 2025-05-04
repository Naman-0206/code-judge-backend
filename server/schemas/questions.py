from typing import Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel


class QuestionBase(SQLModel):
    title: str
    body: str
    creator_id: UUID


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(SQLModel):
    title: Optional[str] = None
    body: Optional[str] = None


class QuestionRead(QuestionBase):
    id: UUID
    created_at: datetime
    # updated_at: datetime
