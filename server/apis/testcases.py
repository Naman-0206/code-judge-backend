from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist, OperationalError
from models import Testcase, Testcase_Pydantic, Testcase_PydanticIn, Question, TestcaseType, Testcase_List_Pydantic
from uuid import UUID
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(tags=["testcases"])


@router.get("/{question_id}/sample_testcases", response_model=list[Testcase_Pydantic])
async def get_sample_testcases(question_id: UUID):
    # TODO: Sort by created_at
    """Retrieve all testcases for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")
        testcases = await Testcase_Pydantic.from_queryset(Testcase.filter(question=question, type = TestcaseType.sample))
        return testcases
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error fetching testcases for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{question_id}/public_testcases", response_model=list[Testcase_Pydantic])
async def get_public_testcases(question_id: UUID):
    # TODO: Sort by created_at
    """Retrieve all testcases for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")
        testcases = await Testcase_Pydantic.from_queryset(Testcase.filter(question=question, type = TestcaseType.public))
        return testcases
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error fetching testcases for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{question_id}/private_testcases", response_model=list[Testcase_Pydantic])
async def get_private_testcases(question_id: UUID):
    # TODO: Sort by created_at
    """Retrieve all testcases for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question and can view private testcases
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")
        testcases = await Testcase_Pydantic.from_queryset(Testcase.filter(question=question, type = TestcaseType.private))
        return testcases
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error fetching testcases for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{question_id}/testcases", response_model=List[Testcase_List_Pydantic])
async def get_testcases(question_id: UUID):
    """Retrieve all testcases for a given question."""
    # TODO: Sort by created_at
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")    
        testcases = await Testcase_List_Pydantic.from_queryset(Testcase.filter(question=question))
        return testcases
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Error fetching testcases for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/{question_id}/testcases", response_model=Testcase_Pydantic)
async def create_testcase(question_id: UUID, testcase: Testcase_PydanticIn): # type: ignore
    """Create a new testcase for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")

        # Remove question_id from testcase data if present, as it's provided in the path
        testcase_data = testcase.dict(exclude_unset=True)
        if "question_id" in testcase_data:
            del testcase_data["question_id"]  # Avoid duplicate assignment

        # Assign the question object directly to question_id
        obj = await Testcase.create(question=question, **testcase_data)
        return await Testcase_Pydantic.from_tortoise_orm(obj)
    except HTTPException:
        raise
    except OperationalError as e:
        logger.error(f"Database error creating testcase: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error creating testcase: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{question_id}/testcases/{id}", response_model=Testcase_Pydantic)
async def get_testcase(question_id: UUID, id: UUID):
    """Retrieve a specific testcase for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")

        obj = await Testcase.get_or_none(id=id, question=question)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Testcase with ID {id} not found for question {question_id}")
        return await Testcase_Pydantic.from_tortoise_orm(obj)
    except HTTPException:
        raise
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"Testcase with ID {id} not found")
    except Exception as e:
        logger.error(f"Error fetching testcase {id} for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{question_id}/testcases/{id}", response_model=Testcase_Pydantic)
async def update_testcase(question_id: UUID, id: int, testcase: Testcase_PydanticIn): # type: ignore
    """Update an existing testcase for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")

        obj = await Testcase.get_or_none(id=id, question=question)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Testcase with ID {id} not found for question {question_id}")

        # Remove question_id from update data if present (it's immutable in this context)
        update_data = testcase.dict(exclude_unset=True)
        if "question_id" in update_data:
            del update_data["question_id"]

        await obj.update_from_dict(update_data)
        await obj.save()
        return await Testcase_Pydantic.from_tortoise_orm(obj)
    except HTTPException:
        raise
    except OperationalError as e:
        logger.error(f"Database error updating testcase {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Error updating testcase {id} for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{question_id}/testcases/{id}")
async def delete_testcase(question_id: UUID, id: int):
    """Delete a specific testcase for a given question."""
    try:
        question = await Question.get_or_none(id=question_id)
        # TODO: Check if user has access to this question
        if not question:
            raise HTTPException(status_code=404, detail=f"Question with ID {question_id} not found or you don't have access")

        obj = await Testcase.get_or_none(id=id, question=question)
        if not obj:
            raise HTTPException(status_code=404, detail=f"Testcase with ID {id} not found for question {question_id}")

        await obj.delete()
        return {"detail": f"Testcase {id} deleted successfully"}
    except HTTPException:
        raise
    except OperationalError as e:
        logger.error(f"Database error deleting testcase {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Error deleting testcase {id} for question {question_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")