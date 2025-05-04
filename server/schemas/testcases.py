from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime

class TestcaseBase(SQLModel):
    input_url: str
    output_url: str
    time_limit: Optional[int] = None
    memory_limit: Optional[int] = None
    name: Optional[str] = None
    is_sample: bool = False

class TestcaseCreate(TestcaseBase):
    pass


class TestcaseRead(TestcaseBase):
    id: int
    created_at: datetime
    question_id: UUID

    # class Config:
    #     from_attributes = True  # if using SQLModel >=0.0.8


class TestcaseUpdate(SQLModel):
    input_url: Optional[str] = None
    output_url: Optional[str] = None
    time_limit: Optional[int] = None
    memory_limit: Optional[int] = None
    name: Optional[str] = None
    is_sample: Optional[bool] = None