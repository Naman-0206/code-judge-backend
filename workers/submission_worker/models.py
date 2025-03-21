from dataclasses import dataclass, asdict, field
from enum import Enum
import json
from typing import List, TypedDict


def get_supported_lang() -> List[str]:
    from workers.executor.executors import file_extensions
    return file_extensions


class TestCase(TypedDict):
    input_url: str
    output_url: str


@dataclass()
class Event:
    job_id: str
    lang: str
    source_code: str
    question_id: str
    time_limit: int = field(default=5)  # Default to 5 seconds
    memory_limit: int = field(default=512)  # Default to 512 MB

    def __post_init__(self):
        if not isinstance(self.job_id, str):
            raise TypeError(f"job_id must be an int, got {type(self.job_id).__name__}")
        if not isinstance(self.lang, str):
            raise TypeError(f"lang must be a str, got {type(self.lang).__name__}")
        if not isinstance(self.source_code, str):
            raise TypeError(f"source_code must be a str, got {type(self.source_code).__name__}")
        if not isinstance(self.time_limit, int):
            raise TypeError(f"time_limit must be an int, got {type(self.time_limit).__name__}")
        if not isinstance(self.memory_limit, int):
            raise TypeError(f"memory_limit must be an int, got {type(self.memory_limit).__name__}")
        if not isinstance(self.question_id, str):
            raise TypeError(f"question_id must be an str, got {type(self.question_id).__name__}")
    
        if self.lang not in get_supported_lang():   
            raise ValueError(f"Invalid language: {self.lang}")
        
        self.file_extension = get_supported_lang()[self.lang]

    @staticmethod
    def from_json(json_str: str) -> 'Event':
        """Deserialize JSON string to a Event instance."""
        data = json.loads(json_str)
        return Event(**data)

    def to_json(self) -> str:
        """Serialize the Event instance to a JSON string."""
        return json.dumps(asdict(self), indent=4)


class ExitCode(Enum):
    SUCCESS = 200
    ACCEPTED = 200
    WRONG_ANSWER = 400
    PRESENTATION_ERROR = 201
    FILE_NOT_FOUND = 401
    TIME_LIMIT_EXCEEDED = 124
    MEMORY_LIMIT_EXCEEDED = 137
    SEGMENTATION_FAULT = 139
    TERMINATED_BY_SIGNAL = 143
    COMMAND_NOT_FOUND = 127
    COMPILATION_ERROR = 125
    GENERIC_ERROR = 1
    INVALID_USAGE = 2