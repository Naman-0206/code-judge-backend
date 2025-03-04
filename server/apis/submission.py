import json
from uuid import UUID, uuid4
from fastapi import APIRouter, HTTPException, Query
from models import Submission, Submission_List_Pydantic, Submission_Pydantic, Question, SubmissionVerdict, Submission_PydanticIn
from models.pydantic_models import SubmissionEvent
from typing import Optional, List
from rabbitmq import rabbit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["submissions"])


@router.get("/{question_id}/submissions", response_model=List[Submission_List_Pydantic])
async def get_all_submissions(
    question_id: UUID,
    verdict: Optional[str] = Query(None, description="Filter by verdict (e.g., 'Accepted', 'Wrong Answer')"),
    sort_by: Optional[str] = Query("created_at", description="Sort by field (e.g., 'created_at', 'verdict')"),
    sort_order: Optional[str] = Query("desc", description="Sort order ('asc' or 'desc')")
):
    """
    Retrieve all submissions for a given question with filters and sorting.
    Returns only id, question, created_at, and verdict.
    """
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(
                status_code=404,
                detail=f"Question with ID {question_id} not found or you don't have access"
            )

        queryset = Submission.filter(question=question).exclude(verdict="Running...")

        if verdict:
            verdict = verdict.capitalize()
            if verdict not in SubmissionVerdict.__members__.values():
                raise HTTPException(status_code=400, detail=f"Invalid verdict: {verdict}")
            queryset = queryset.filter(verdict=verdict)

        # Sanitize sort_by and sort_order
        allowed_sort_fields = {"created_at", "verdict"}
        sort_by = sort_by.lower() if sort_by else "created_at"
        if sort_by not in allowed_sort_fields:
            raise HTTPException(status_code=400, detail=f"Invalid sort_by field: {sort_by}. Allowed: {allowed_sort_fields}")

        sort_order = sort_order.lower() if sort_order else "desc"
        if sort_order not in {"asc", "desc"}:
            raise HTTPException(status_code=400, detail=f"Invalid sort_order: {sort_order}. Allowed: 'asc', 'desc'")

        order_prefix = "" if sort_order == "asc" else "-"
        queryset = queryset.order_by(f"{order_prefix}{sort_by}")

        submissions = await Submission_List_Pydantic.from_queryset(queryset)
        return submissions

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching submissions for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{question_id}/submissions/{submission_id}", response_model=Submission_Pydantic)
async def get_submission(question_id: UUID, submission_id: UUID):
    """
    Retrieve details of a specific submission for a given question.
    """
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(
                status_code=404,
                detail=f"Question with ID {question_id} not found or you don't have access"
            )

        submission = await Submission.get_or_none(id=submission_id, question=question)
        if not submission:
            raise HTTPException(
                status_code=404,
                detail=f"Submission with ID {submission_id} not found for question {question_id}"
            )

        return await Submission_Pydantic.from_tortoise_orm(submission)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching submission {submission_id} for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
 
 
@router.post("/{question_id}/submit", response_model=Submission_Pydantic)
async def submit_code(question_id: UUID, submission: Submission_PydanticIn): # type: ignore
    
    question = await Question.get_or_none(id=question_id)
    # TODO: Check if user has access to this question
    if not question:
        raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")


    submission_data = submission.dict(exclude_unset=True)
    if "question_id" in submission_data:
        del submission_data["question_id"]


    submission: Submission = await Submission.create(question=question, **submission_data)

    job_id = submission.id

    message = json.dumps({
        "job_id": str(job_id), 
        "lang": submission.language,
        "source_code": submission.code,
        "question_id": str(question_id),
        "time_limit": 5, # in seconds
        "memory_limit": 512, # in MB
    })

    rabbit.publish("submission_queue", message)
    
    return await Submission_Pydantic.from_tortoise_orm(submission)