import json
from fastapi import FastAPI, HTTPException, Body
from redis_client import r
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

@app.get("/submission/{job_id}/check")
async def get_job_status(job_id: int):
    res = r.get(job_id)
    if res:
        return json.loads(res)
    return HTTPException(status_code=404, detail="Job not found")


app.include_router(execution_router)
app.include_router(submission_router)
app.include_router(questions_router, prefix="/questions")
app.include_router(testcases_router, prefix="/questions")

