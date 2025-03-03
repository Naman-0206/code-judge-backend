from fastapi import APIRouter, HTTPException
from models import Question_Pydantic, Question, Question_PydanticIn
from uuid import UUID

router = APIRouter(tags=["questions"])

@router.get("", response_model=list[Question_Pydantic])
async def get_questions():
    return await Question_Pydantic.from_queryset(Question.all())

@router.get("/{id}", response_model=Question_Pydantic)
async def get_question(id: UUID):
    question = await Question.filter(id=id).first()
    if question:
        return await Question_Pydantic.from_tortoise_orm(question)
    raise HTTPException(status_code=404, detail="Question not found")

@router.post("", response_model=Question_Pydantic)
async def create_question(question: Question_PydanticIn):
    obj = await Question.create(**question.dict(exclude_unset=True)) 
    return await Question_Pydantic.from_tortoise_orm(obj)

@router.put("/{id}", response_model=Question_Pydantic)
async def update_question(id: UUID, question: Question_PydanticIn):
    obj = await Question.filter(id=id).first() 
    if obj:
        obj.update_from_dict(question.dict(exclude_unset=True)) 
        await obj.save() 
        return await Question_Pydantic.from_tortoise_orm(obj)
    raise HTTPException(status_code=404, detail="Question not found")

@router.delete("/{id}")
async def delete_question(id: UUID):
    obj = await Question.filter(id=id).first() 
    if obj:
        await obj.delete()
        return {"message": "Question deleted successfully"}
    raise HTTPException(status_code=404, detail="Question not found")


