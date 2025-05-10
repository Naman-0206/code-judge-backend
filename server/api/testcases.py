from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from uuid import UUID
import logging

from models.testcases import Testcase
from schemas.testcases import TestcaseCreate, TestcaseRead, TestcaseUpdate
from core.db import get_session
from models.questions import Question
from core.auth import get_current_user
from models.users import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["testcases"])


@router.get("/{question_id}/sample_testcases", response_model=List[TestcaseRead])
async def get_sample_testcases(question_id: UUID, session: Session = Depends(get_session)):
    try:
        testcases = session.exec(
            select(Testcase).where(Testcase.question_id == question_id, Testcase.is_sample == True)
        ).all()
        return testcases
    except SQLAlchemyError as e:
        logger.exception(f"Database error while retrieving sample testcases for question {question_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{question_id}/testcases", response_model=List[TestcaseRead])
async def get_testcases(question_id: UUID, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    # TODO: Add pagination
    try:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        if question.creator_id != user.id:
            testcases = session.exec(
                select(Testcase).where(Testcase.question_id == question_id | Testcase.is_sample == True)
            ).all()
            return testcases

        testcases = session.exec(
            select(Testcase).where(Testcase.question_id == question_id)
        ).all()
        return testcases
    
    except SQLAlchemyError as e:
        logger.exception(f"Database error while retrieving testcases for question {question_id}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/{question_id}/testcases", response_model=TestcaseRead)
async def create_testcase(question_id: UUID, testcase: TestcaseCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        
        if question.creator_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to create testcases for this question")

        db_testcase = Testcase(**testcase.model_dump(), question_id=question_id)
        session.add(db_testcase)
        session.commit()
        session.refresh(db_testcase)
        return db_testcase
    except SQLAlchemyError as e:
        logger.exception(f"Error creating testcase for question {question_id}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Could not create testcase")


@router.get("/{question_id}/testcases/{id}", response_model=TestcaseRead)
async def get_testcase(question_id: UUID, id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        testcase = session.get(Testcase, id)
        if not testcase or testcase.question_id != question_id:
            raise HTTPException(status_code=404, detail="Testcase not found for this question.")
        
        if testcase.is_sample:
            return testcase
    
        if testcase.question.creator_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to retrieve this testcase")
        
        return testcase
    except SQLAlchemyError as e:
        logger.exception(f"Error retrieving testcase {id} for question {question_id}")
        raise HTTPException(status_code=500, detail="Could not retrieve testcase")


@router.put("/{question_id}/testcases/{id}", response_model=TestcaseRead)
async def update_testcase(question_id: UUID, id: int, testcase: TestcaseUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        db_testcase = session.get(Testcase, id)
        if not db_testcase or db_testcase.question_id != question_id:
            raise HTTPException(status_code=404, detail="Testcase not found for this question.")

        if db_testcase.question.creator_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this testcase")

        testcase_data = testcase.model_dump(exclude_unset=True)
        for key, value in testcase_data.items():
            setattr(db_testcase, key, value)

        session.add(db_testcase)
        session.commit()
        session.refresh(db_testcase)
        return db_testcase
    except SQLAlchemyError as e:
        logger.exception(f"Error updating testcase {id} for question {question_id}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Could not update testcase")


@router.delete("/{question_id}/testcases/{id}")
async def delete_testcase(question_id: UUID, id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    try:
        testcase = session.get(Testcase, id)
        if not testcase or testcase.question_id != question_id:
            raise HTTPException(status_code=404, detail="Testcase not found for this question.")

        if testcase.question.creator_id != user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to delete this testcase")
        
        session.delete(testcase)
        session.commit()
        return {"detail": "Testcase deleted successfully"}
    except SQLAlchemyError as e:
        logger.exception(f"Error deleting testcase {id} for question {question_id}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Could not delete testcase")
