from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "questions" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "content" TEXT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "submissions" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "verdict" VARCHAR(21) NOT NULL DEFAULT 'Running...' /* AC: Accepted\nWA: Wrong Answer\nTLE: Time Limit Exceeded\nMLE: Memory Limit Exceeded\nCE: Compilation Error\nRE: Runtime Error\nSE: Segmentation Fault\nOLE: Output Limit Exceeded\nPE: Presentation Error\nIE: Internal Error\nRUN: Running... */,
    "language" VARCHAR(6) NOT NULL /* C: C\nCPP: CPP\nPYTHON: PYTHON */,
    "code" TEXT NOT NULL,
    "question_id" CHAR(36) NOT NULL REFERENCES "questions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "testcases" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "input_url" VARCHAR(511) NOT NULL,
    "output_url" VARCHAR(511) NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "type" VARCHAR(7) NOT NULL DEFAULT 'Sample' /* public: Public\nprivate: Private\nsample: Sample */,
    "question_id" CHAR(36) NOT NULL REFERENCES "questions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
