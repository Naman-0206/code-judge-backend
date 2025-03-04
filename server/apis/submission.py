import json
import pika
from fastapi import APIRouter
from models.pydantic_models import SubmissionEvent
# from rabbitmq import channel, submit_queue


router = APIRouter(tags=["submission"])
job_id_counter = 1

@router.post("/submit/")
async def process_code(event: SubmissionEvent):
    global job_id_counter
    
    job_id = job_id_counter
    job_id_counter += 1

    message = json.dumps({
        "job_id": job_id, 
        "lang": event.lang,
        "source_code": event.source_code,
        "time_limit": 5, # in seconds
        "memory_limit": 512, # in MB
        "input": event.input,
        "expected_output": event.expected_output,
    })

    # channel.basic_publish(
    #         exchange='',
    #         routing_key=submit_queue,
    #         body=message,
    #         properties=pika.BasicProperties(
    #             delivery_mode=2,  # Make the message persistent
    #         )
    #     )
    
    return {"job_id": job_id}