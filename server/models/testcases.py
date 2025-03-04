from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from models.questions import Question
from enum import Enum

class TestcaseType(str, Enum):
    public = "Public"
    private = "Private"
    sample = "Sample"

class Testcase(models.Model):
    id = fields.UUIDField(pk=True)
    question = fields.ForeignKeyField("models.Question", related_name="testcases", on_delete=fields.CASCADE)
    input_url = fields.CharField(max_length=511)
    output_url = fields.CharField(max_length=511)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    type = fields.CharEnumField(TestcaseType, default=TestcaseType.sample, max_length=7)

    def __str__(self):
        return f"Testcase {self.id} for Question {self.question}"
    
    class Meta:
        table = "testcases"

# Pydantic Models for Serialization
Testcase_Pydantic = pydantic_model_creator(Testcase, name="Testcase")
Testcase_PydanticIn = pydantic_model_creator(Testcase, name="TestcaseIn", exclude_readonly=True)
Testcase_List_Pydantic = pydantic_model_creator(Testcase, name="TestcaseList", exclude=("question",), include=("id", "created_at", "updated_at", "type"))