from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from uuid import UUID

from models.questions import Question
from db import get_session  
from schemas.questions import QuestionRead, QuestionCreate, QuestionUpdate

router = APIRouter(tags=["questions"])

@router.get("/", response_model=list[QuestionRead])
def get_questions(session: Session = Depends(get_session)):
    questions = session.exec(select(Question)).all()
    return questions


@router.get("/{id}", response_model=QuestionRead)
def get_question(id: UUID, session: Session = Depends(get_session)):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/", response_model=QuestionRead)
def create_question(question: QuestionCreate, session: Session = Depends(get_session)):
    db_question = Question(**question.model_dump())
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


@router.put("/{id}", response_model=QuestionRead)
def update_question(id: UUID, question: QuestionUpdate, session: Session = Depends(get_session)):
    db_question = session.get(Question, id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    question_data = question.model_dump(exclude_unset=True)
    for key, value in question_data.items():
        setattr(db_question, key, value)

    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


@router.delete("/{id}")
def delete_question(id: UUID, session: Session = Depends(get_session)):
    db_question = session.get(Question, id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    session.delete(db_question)
    session.commit()
    return {"message": "Question deleted successfully"}