import json
from fastapi import APIRouter, HTTPException
from models.pydantic_models import ExecutionEvent
from rabbitmq import rabbit
from uuid import uuid4
from redis_client import r

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

    # channel.basic_publish(
    #     exchange='',
    #     routing_key=execution_queue,
    #     body=message,
    #     properties=pika.BasicProperties(
    #         delivery_mode=2,  # Make the message persistent
    #     )
    # )
    rabbit.publish("execution_queue", message)

    return {"job_id": job_id}


@router.get("/{job_id}/check")
async def get_job_status(job_id: str):
    res = r.get(job_id)
    if res:
        return json.loads(res)
    return HTTPException(status_code=404, detail="Job not found")
