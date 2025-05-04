from fastapi import FastAPI
from apis.execute import router as execution_router
# from apis.submission import router as submission_router
from apis.questions import router as questions_router
from apis.testcases import router as testcases_router
from db import create_db_and_tables
from models.users import User
from models.submissions import Submission

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(execution_router, prefix="/execute")
# app.include_router(submission_router, prefix="/submit")
app.include_router(questions_router, prefix="/questions")
app.include_router(testcases_router, prefix="/testcases")

