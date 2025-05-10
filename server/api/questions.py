from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from uuid import UUID

from models.questions import Question
from core.db import get_session  
from schemas.questions import QuestionRead, QuestionCreate, QuestionUpdate
from core.auth import get_current_user
from models.users import User

router = APIRouter(tags=["questions"])

@router.get("/", response_model=list[QuestionRead])
def get_questions(session: Session = Depends(get_session)):
    # TODO: Add pagination
    questions = session.exec(select(Question)).all()
    return questions


@router.get("/{id}", response_model=QuestionRead)
def get_question(id: UUID, session: Session = Depends(get_session)):
    question = session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.post("/", response_model=QuestionRead)
def create_question(question: QuestionCreate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_question = Question(**question.model_dump(), creator_id=user.id)
    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


@router.put("/{id}", response_model=QuestionRead)
def update_question(id: UUID, question: QuestionUpdate, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_question = session.get(Question, id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    if db_question.creator_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to update this question")

    question_data = question.model_dump(exclude_unset=True)
    for key, value in question_data.items():
        setattr(db_question, key, value)

    session.add(db_question)
    session.commit()
    session.refresh(db_question)
    return db_question


@router.delete("/{id}")
def delete_question(id: UUID, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    db_question = session.get(Question, id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if db_question.creator_id != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this question")
    
    session.delete(db_question)
    session.commit()
    return {"message": "Question deleted successfully"}