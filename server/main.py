import json
from fastapi import FastAPI, HTTPException, Body
from apis.execute import router as execution_router
from apis.submission import router as submission_router
from apis.questions import router as questions_router
from apis.testcases import router as testcases_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},  # SQLite for simplicity
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],  # Adjust if models are in submodules
            "default_connection": "default",
        }
    }
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,  # Use with caution; prefer migrations for production
    add_exception_handlers=True,
)



app.include_router(execution_router, prefix="/execute")
app.include_router(submission_router, prefix="/submit")
app.include_router(questions_router, prefix="/questions")
app.include_router(testcases_router, prefix="/questions")

