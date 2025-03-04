from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Question(models.Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # creator = fields.ForeignKeyField("models.User", related_name="questions")
    # modrators = fields.ManyToManyField("models.User", related_name="moderated_questions")

    # tags = fields.ManyToManyField("models.Tag", related_name="questions")
    # difficulty = fields.IntField(default=0)

    # timelimit = fields.IntField(default=5)
    # memorylimit = fields.IntField(default=512)

    def __str__(self):
        return f"{self.id} - {self.title}"
    
    class Meta:
        table = "questions"

# Pydantic Models for Serialization
Question_Pydantic = pydantic_model_creator(Question, name="Question")
Question_PydanticIn = pydantic_model_creator(Question, name="QuestionIn", exclude_readonly=True)
