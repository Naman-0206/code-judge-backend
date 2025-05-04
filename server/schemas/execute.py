from typing import Literal
from pydantic import BaseModel

class BaseEvent(BaseModel):
    lang: Literal["c", "cpp", "python"]
    source_code: str

class ExecutionEvent(BaseEvent):
    input: str
