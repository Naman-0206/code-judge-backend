from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from models.questions import Question
from enum import Enum

class SubmissionVerdict(str, Enum):
    AC = "Accepted"
    WA = "Wrong Answer"
    TLE = "Time Limit Exceeded"
    MLE = "Memory Limit Exceeded"
    CE = "Compilation Error"
    RE = "Runtime Error"
    SE = "Segmentation Fault"
    OLE = "Output Limit Exceeded"
    PE = "Presentation Error"
    IE = "Internal Error"
    RUN = "Running..."

class SubmissionLanguage(str, Enum):
    C = "C"
    CPP = "CPP"
    PYTHON = "PYTHON"


class Submission(models.Model):
    id = fields.UUIDField(pk=True)
    question = fields.ForeignKeyField("models.Question", related_name="submissions", on_delete=fields.CASCADE)
    created_at = fields.DatetimeField(auto_now_add=True)
    verdict = fields.CharEnumField(SubmissionVerdict, default=SubmissionVerdict.RUN, max_length=21)
    language = fields.CharEnumField(SubmissionLanguage, max_length=6)
    code = fields.TextField()

    # creator = fields.ForeignKeyField("models.User", related_name="submissions", on_delete=fields.CASCADE)

    def __str__(self):
        return f"Submission {self.id} for Question {self.question}"
    
    class Meta:
        table = "submissions"

# Pydantic Models for Serialization
Submission_Pydantic = pydantic_model_creator(Submission, name="Submission")
Submission_PydanticIn = pydantic_model_creator(Submission, name="SubmissionIn", include=("code", "language"), exclude_readonly=True)
Submission_List_Pydantic = pydantic_model_creator(
    Submission,
    name="SubmissionList",
    include=("id", "question", "created_at", "verdict", "language")  # Only these fields for list endpoint
)