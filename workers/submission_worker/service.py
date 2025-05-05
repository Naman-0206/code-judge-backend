import os
import json
from uuid import UUID
import redis
from .models import SubmissionEvent
from .db import count_testcases_by_question_id, engine, Session, get_testcases_by_question_id
from .executor.executors import lang_runners
from .constants import exit_codes


r = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv(
    "REDIS_PORT"), decode_responses=True)

file_extensions = {
    "c": ".c",
    "cpp": ".cpp",
    "python": ".py"
}


def execute_code(language, code_file_path, input_file_path, output_file_path, error_file_path, time_limit, memory_limit):
    return lang_runners[language](code_file_path, input_file_path, output_file_path, error_file_path, time_limit, memory_limit)


def event_callback(ch, method, properties, body):
    # TODO: add error handling
    event = SubmissionEvent.model_validate_json(body.decode())

    print("Received: ", event.submission_id)

    r.set(f"submission_{event.submission_id}",
          json.dumps({"status": "Running..."}), ex=5*60)

    file_extension = file_extensions[event.language]
    source_file_path = os.path.join(os.getcwd(), f"main{file_extension}")
    with open(source_file_path, "w") as source_file:
        source_file.write(event.source_code)

    input_file_path = os.path.join(os.getcwd(), "input.txt")
    output_file_path = os.path.join(os.getcwd(), "output.txt")
    error_file_path = os.path.join(os.getcwd(), "error.txt")

    with Session(engine) as session:
        total_testcases = count_testcases_by_question_id(
            session, UUID(event.question_id))
        passed_testcases = 0
        for testcase in get_testcases_by_question_id(session, UUID(event.question_id)):
            r.set(f"submission_{event.submission_id}", json.dumps(
                {"status": f"{passed_testcases}/{total_testcases}"}), ex=5*60)

            with open(input_file_path, "w") as input_file:
                input_file.write(testcase.input)

            open(output_file_path, "w").close()
            open(error_file_path, "w").close()

            exit_code = execute_code(event.language, source_file_path, input_file_path,
                                     output_file_path, error_file_path, event.time_limit, event.memory_limit)

            if exit_code != 0:
                break

            with open(output_file_path, "r") as output_file:
                if output_file.read().strip() == testcase.output.strip():
                    passed_testcases += 1
                else:
                    exit_code = 400
                    break

        ch.basic_ack(delivery_tag=method.delivery_tag)
        if exit_code == 0:
            r.set(f"submission_{event.submission_id}",
                  json.dumps({"verdict": f"Accepted"}), ex=5*60)
            # TODO: set status to "Accepted" in db
            return

        verdict = exit_codes[exit_code]
        r.set(f"submission_{event.submission_id}", json.dumps({
            "verdict":  verdict,
            "testcases_passed": passed_testcases,
            "total_testcases": total_testcases,
            "input": testcase.input,
            "expected_output": testcase.output,
            "output": open(output_file_path, "r").read(),
            "error": open(error_file_path, "r").read()}), ex=5*60)

        # TODO: set status to "Rejected" in db
