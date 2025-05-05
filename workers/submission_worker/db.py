from sqlmodel import Session, create_engine, func, select
from .models import Testcase as TestCase
from uuid import UUID
from typing import Generator
import os

def get_testcases_by_question_id(
    session: Session,
    question_id: UUID
) -> Generator[TestCase, None, None]:
    statement = (
        select(TestCase)
        .where(TestCase.question_id == question_id)
        .order_by(TestCase.id)
    )

    result = session.exec(statement)
    for testcase in result:
        yield testcase

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)


def count_testcases_by_question_id(
    session: Session,
    question_id: UUID
) -> int:
    statement = select(func.count()).where(TestCase.question_id == question_id)
    return session.exec(statement).one()