import json
from fastapi import FastAPI, HTTPException, Body
import pika
from pydantic import BaseModel
from rabbitmq import channel, submit_queue, execution_queue
from redis_client import r

app = FastAPI()

class BaseEvent(BaseModel):
    # question_id: int
    lang: str
    source_code: str

class ExecutionEvent(BaseEvent):
    input: str

class SubmissionEvent(BaseEvent):
    input: str
    expected_output: str


global job_id_counter
job_id_counter = 1

@app.post("/process-code/")
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

    channel.basic_publish(
            exchange='',
            routing_key=submit_queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )
    
    return {"job_id": job_id}


@app.get("/job-status/{job_id}")
async def get_job_status(job_id: int):
    res = r.get(job_id)
    if res:
        return json.loads(res)
    return HTTPException(status_code=404, detail="Job not found")


@app.get("/execute/")
async def execute_code(event: ExecutionEvent):
    
    global job_id_counter
    
    job_id_counter += 1

    message = json.dumps({
        "job_id": job_id_counter,
        "lang": event.lang,
        "source_code": event.source_code,
        "time_limit": 5, # in seconds
        "memory_limit": 512, # in MB
        "input": event.input,
    })

    channel.basic_publish(
            exchange='',
            routing_key=execution_queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )
    
    return {"job_id": job_id_counter}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)