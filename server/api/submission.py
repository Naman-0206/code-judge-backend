from fastapi import APIRouter, Query, Depends, HTTPException
from uuid import UUID
from typing import Literal, Optional, List
from sqlmodel import Session, select
from sqlalchemy import desc, asc
from core.db import get_session
from models.submissions import Submission
from models.questions import Question
from schemas.submissions import SubmissionRead, SubmissionCreate
import logging



router = APIRouter(tags=["submissions"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def paginate(query, skip: int, limit: int):
    return query.offset(skip).limit(limit)

@router.get("/{question_id}/submissions", response_model=List[SubmissionRead])
def get_all_submissions(
    question_id: UUID,
    verdict: Optional[str] = Query(None),
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Literal["asc", "desc"] = Query("desc"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    session: Session = Depends(get_session)
):
    try:
        query = select(Submission).where(Submission.question_id == question_id)

        if verdict:
            query = query.where(Submission.verdict == verdict)

        if sort_order == "asc":
            query = query.order_by(asc(sort_by))
        elif sort_order == "desc":
            query = query.order_by(desc(sort_by))
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_order. Use 'asc' or 'desc'.")

        paginated_query = paginate(query, skip, limit)
        
        submissions = session.exec(paginated_query).all()

        if not submissions:
            raise HTTPException(status_code=404, detail="No submissions found for this question or filter.")
        
        return submissions

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving submissions for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving submissions.")

@router.get("/{question_id}/submissions/{submission_id}", response_model=SubmissionRead)
def get_submission(
    question_id: UUID,
    submission_id: int,
    session: Session = Depends(get_session)
):
    try:
        submission = session.get(Submission, submission_id)

        if not submission:
            raise HTTPException(status_code=404, detail="Submission not found.")

        if submission.question_id != question_id:
            raise HTTPException(status_code=404, detail="Submission does not belong to this question.")

        return submission

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error retrieving submission {submission_id} for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while retrieving submission.")


@router.post("/{question_id}/submit", response_model=SubmissionRead)
def submit_code(
    question_id: UUID,
    submission: SubmissionCreate,
    session: Session = Depends(get_session)
):
    try:
        question = session.get(Question, question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found.")

        db_submission = Submission(
            language=submission.language,
            source_code=submission.source_code,
            creator_id=submission.creator_id,
            question_id=question_id,
            verdict="In Queue",
            score=None,  # You can calculate score later based on the code evaluation
            result={},  # Initial empty result or a default value
        )

        # Step 3: Add the submission to the session and commit
        session.add(db_submission)
        session.commit()
        session.refresh(db_submission)

        # TODO: Add the submission to the queue
        # Step 4: add the submission to the queue
        # ...

        return db_submission

    except HTTPException as e:
        # Handle HTTP exceptions (like Question not found)
        raise e
    except Exception as e:
        logger.error(f"Error submitting code for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error while submitting code.")