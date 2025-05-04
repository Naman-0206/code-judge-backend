import json
from fastapi import APIRouter, HTTPException
from schemas.pydantic_models import ExecutionEvent
from config.rabbitmq import rabbit
from uuid import uuid4
from config._redis import redis_client

router = APIRouter(tags=["execute"])


@router.post("")
async def execute_code(event: ExecutionEvent):

    job_id = str(uuid4())
    message = json.dumps({
        "job_id": job_id,
        "lang": event.lang,
        "source_code": event.source_code,
        "time_limit": 5,  # in seconds
        "memory_limit": 512,  # in MB
        "input": event.input,
    })

    rabbit.publish("execution_queue", message)

    redis_client.set(job_id, json.dumps({
        "job_id": job_id,
        "status": "Running..."
    }), ex=5*60)

    return {"job_id": job_id}


@router.get("/{job_id}/check")
async def get_job_status(job_id: str):
    res = redis_client.get(job_id)
    if res:
        return json.loads(res)
    return HTTPException(status_code=404, detail="Job not found")
