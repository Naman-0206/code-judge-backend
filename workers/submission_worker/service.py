import os
import json
from uuid import UUID
import redis
from .models import SubmissionEvent
from .db import count_testcases_by_question_id, engine, Session, get_testcases_by_question_id, update_submission_verdict_and_result
from .executor.executors import lang_runners
from .constants import exit_codes
import time
from submission_worker import working_dir

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=os.getenv("REDIS_PORT", 6379),
    password=os.getenv("REDIS_PASSWORD", None),
    username=os.getenv("REDIS_USER", None),
    ssl=True,
    decode_responses=True
    )

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
    source_file_path = os.path.join(working_dir, f"main{file_extension}")
    with open(source_file_path, "w") as source_file:
        source_file.write(event.source_code)

    input_file_path = os.path.join(working_dir, "input.txt")
    output_file_path = os.path.join(working_dir, "output.txt")
    error_file_path = os.path.join(working_dir, "error.txt")

    with Session(engine) as session:
        total_testcases = count_testcases_by_question_id(
            session, UUID(event.question_id))
        passed_testcases = 0
        total_runtime = 0
        for testcase in get_testcases_by_question_id(session, UUID(event.question_id)):
            r.set(f"submission_{event.submission_id}", json.dumps(
                {"status": f"{passed_testcases}/{total_testcases}"}), ex=5*60)

            with open(input_file_path, "w") as input_file:
                input_file.write(testcase.input)

            open(output_file_path, "w").close()
            open(error_file_path, "w").close()

            starttime = time.time()
            exit_code = execute_code(event.language, source_file_path, input_file_path,
                                     output_file_path, error_file_path, event.time_limit, event.memory_limit)
            runtime_s = time.time() - starttime
            runtime = round(runtime_s*100, 2) # in ms
            total_runtime += runtime

            if exit_code != 0:
                break

            with open(output_file_path, "r") as output_file:
                if output_file.read().strip() == testcase.output.strip():
                    passed_testcases += 1
                else:
                    exit_code = 400
                    break

        verdict = exit_codes[exit_code]
        total_runtime = round(total_runtime)
        if exit_code == 0:
            verdict = "Accepted"
            r.set(f"submission_{event.submission_id}",
                  json.dumps({"verdict": verdict,
                              "testcases_passed": passed_testcases,
                              "total_testcases": total_testcases,
                              "runtime": total_runtime,
                              }), ex=5*60)
        else:
            r.set(f"submission_{event.submission_id}", json.dumps({
                "verdict":  verdict,
                "testcases_passed": passed_testcases,
                "total_testcases": total_testcases,
                "input": testcase.input,
                "expected_output": testcase.output,
                "output": open(output_file_path, "r").read(),
                "error": open(error_file_path, "r").read(),
                "runtime": total_runtime
            }), ex=5*60)

        update_submission_verdict_and_result(
            session, event.submission_id, verdict, {
                "testcases_passed": passed_testcases,
                "total_testcases": total_testcases,
                "runtime": total_runtime,
            })

    os.remove(source_file_path)
    os.remove(input_file_path)
    os.remove(output_file_path)
    os.remove(error_file_path)

    ch.basic_ack(delivery_tag=method.delivery_tag)