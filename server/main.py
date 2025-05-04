from fastapi import FastAPI
from api.execute import router as execution_router
from api.submission import router as submission_router
from api.questions import router as questions_router
from api.testcases import router as testcases_router
from models.users import User

from core.db import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(execution_router, prefix="/execute")
app.include_router(questions_router, prefix="/questions")
app.include_router(testcases_router, prefix="/questions")
app.include_router(submission_router, prefix="/questions")