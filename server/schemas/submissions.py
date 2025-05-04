from typing import Literal, Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel

class SubmissionBase(BaseModel):
    verdict: Optional[str] = None
    score: Optional[int] = None
    language: Literal["c", "cpp", "python"]
    source_code: str
    result: Optional[dict] = {}

class SubmissionCreate(SQLModel):
    language: Literal["c", "cpp", "python"]
    source_code: str
    creator_id: UUID

class SubmissionRead(SubmissionBase):
    id: int
    creator_id: UUID
    question_id: Optional[UUID]
    created_at: datetime

    class Config:
        from_attributes = True  # To use SQLModel's from_attributes feature
