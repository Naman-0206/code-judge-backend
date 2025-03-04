from pydantic import BaseModel

class BaseEvent(BaseModel):
    # question_id: int
    lang: str
    source_code: str

class ExecutionEvent(BaseEvent):
    input: str

class SubmissionEvent(BaseEvent):
    input: str
    expected_output: str