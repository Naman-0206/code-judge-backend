import json
from typing import Literal
from pydantic import BaseModel
from core.rabbitmq import rabbit
from models.submissions import Submission
from config._redis import redis_client
import logging

logger = logging.getLogger(__name__)


class SubmissionEvent(BaseModel):
    submission_id: int
    language: Literal["c", "cpp", "python"]
    source_code: str
    time_limit: int
    memory_limit: int
    question_id: str


def submit_code(submission: Submission):

    question = submission.question
    event = SubmissionEvent(
        submission_id=submission.id,
        language=submission.language,
        source_code=submission.source_code,
        time_limit=question.time_limit,
        memory_limit=question.memory_limit,
        question_id=str(question.id)
    )
    redis_client.set(f"submission_{submission.id}",
                     json.dumps({"status": "In Queue"}),
                     ex=5*60)
    rabbit.publish("submission_queue", event.model_dump_json())


def check(submission_id: int):
    return redis_client.get(f"submission_{submission_id}")
